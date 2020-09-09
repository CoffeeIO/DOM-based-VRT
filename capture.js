const puppeteer = require('puppeteer');
const moment = require('moment'); // require
const fs = require('fs');
const yaml = require('js-yaml');

let tag = '';
process.argv.forEach(function (val, index, array) {
    console.log(index + ': ' + val);
});


(async () => {
    // Init
    const browser = await puppeteer.launch();

    let config = null;
    try {
        let fileContents = fs.readFileSync('./config.yml', 'utf8');
        config = yaml.safeLoad(fileContents);

        console.log(config);
    } catch (e) {
        console.log(e);
    }

    let summary = {
        files: [],
        tag: "",
        domain: "",
        id: await makeid(10),
    };

    if (!config.urls) {
        console.error('No urls specified.');
        return;
    }
    if (!config.viewports) {
        console.error('No viewports specified.');
        return;
    }

    let count = 1;

    let datetime = moment().format('YYYY-MM-DD--hh-mm-ss');

    for (const url of config.urls) {
        for (const viewport of config.viewports) {

            const page = await browser.newPage();

            // Set viewport and visit website and add module.
            await page.setViewport({width: viewport, height: 1000});
            await page.goto(url);

            let domain = await page.evaluate(function() {
                return window.location.host;
            });

            await page.addScriptTag({path: "./ChromeExtension/domvrt.js"});

            // Scroll to bottom and back up.
            await autoScroll(page);
            await page.waitFor(config.delay);

            // Capture DOM and save
            let data = await page.evaluate(function() {
                return DomVRT.Extractor.currentAppToJSON();
            });

            let path = 'data/' + datetime + '--' + count + '--' + domain + '--' + viewport;
            count += 1;

            summary.files.push(path);
            summary.domain = domain;

            fs.writeFileSync(path + '.json', JSON.stringify(data));

            console.log(viewport + " taking screenshot " + url);


            // Capture Screenshot.
            await page.screenshot({path: path + '.png', fullPage: true});
        }
    }

    fs.writeFileSync('data-summary/' + datetime + '--' + summary.domain + '.json', JSON.stringify(summary));

    await browser.close();
})();

async function autoScroll(page){
    await page.evaluate(async () => {
        await new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}

async function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
 }