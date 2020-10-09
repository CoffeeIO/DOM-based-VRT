const puppeteer = require('puppeteer');
const moment = require('moment'); // require
const fs = require('fs');
const yaml = require('js-yaml');

let startTime = Math.floor(Date.now() / 1000);
let tag = '';
if (process.argv.length >= 3) {
    tag = process.argv[2];
}

const dataSource = 'data';

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
    let datetime = moment().format('YYYY-MM-DD--HH-mm-ss');

    let summary = {
        files: [],
        tag: tag,
        domain: "",
        id: await makeid(10),
        datetime: datetime,
        execution: '',
        config: config,
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

    // Loop urls.
    for (const url of config.urls) {

        // Loop viewport sizes.
        for (const viewport of config.viewports) {

            const page = await browser.newPage();

            // Set viewport and visit website and add module.
            await page.setViewport({width: viewport, height: 1000});
            await page.goto(url);

            let domain = await page.evaluate(function() {
                return window.location.host;
            });

            await page.addScriptTag({path: "./scripts/capture-mutate.js"});

            await page.addScriptTag({path: "./ChromeExtension/domvrt.js"});

            // Scroll to bottom and back up.
            // await autoScroll(page);
            await page.waitFor(config.delay);

            // Capture DOM and save
            let data = await page.evaluate(function() {
                return DomVRT.Extractor.currentAppToJSON();
            });

            let path = dataSource + '/' + datetime + '--' + count + '--' + domain + '--' + viewport;
            count += 1;

            let fileObj = {
                'file': path,
                'viewport': viewport,
                'url': url,
            };
            summary.files.push(fileObj);
            summary.domain = domain;

            fs.writeFileSync(path + '.json', JSON.stringify(data));

            console.log(viewport + " taking screenshot " + url);


            // Capture Screenshot.
            await page.screenshot({path: path + '.png', fullPage: true});
        }
    }

    summary.key = makeKey(config, summary);
    summary.execution = (Math.floor(Date.now() / 1000) - startTime) + 's'
    console.log(summary.key);
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
function makeKey(config, summary) {
    let key = '';

    for (const viewport of config.viewports) {
        key += viewport + '|';
    }
    for (const url of config.urls) {
        key += url + '|';
    }
    console.log(key);


    return hashCode(key);
}

function hashCode(str) {
    var hash = 0;
    if (str.length == 0) {
        return hash;
    }
    for (var i = 0; i < str.length; i++) {
        var char = str.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
}