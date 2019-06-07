'use strict';


if (process.argv.length != 3) {
  console.log('Missing argument');
  return;
}
var folder = process.argv[2];
var num = "";

console.log('Looking for: /' + folder + num);

const compareImages = require("resemblejs/compareImages");
const fs = require("mz/fs");

async function getDiff() {
    const options = {
        output: {
            errorColor: {
                red: 255,
                green: 0,
                blue: 255
            },
            errorType: "movement",
            transparency: 0.3,
            largeImageThreshold: 0,
            useCrossOrigin: false,
            outputDiff: true
        },
        // scaleToSameSize: true,
        ignore: "antialiasing"
    };



    // The parameters can be Node Buffers
    // data is the same as usual with an additional getBuffer() function

    const data = await compareImages(
        await fs.readFile("./data-output/" + folder + num + "/before0000/image.png"),
        await fs.readFile("./data-output/" + folder + num + "/after0000/image.png"),
        options
    );
    const out1 = "./data-output/" + folder + num + "/after0000/resemble.png";
    const out11 = "./data-output/" + folder + num + "/resemble.png";

    await fs.writeFile(out1, data.getBuffer());
    console.log("File saved to %s", out1);

    await fs.writeFile(out11, data.getBuffer());
    console.log("File saved to %s", out11);
    
    const data2 = await compareImages(
        await fs.readFile("./data-output/" + folder + num + "/after0000/image.png"),
        await fs.readFile("./data-output/" + folder + num + "/before0000/image.png"),
        options
    );
    const out2 = "./data-output/" + folder + num + "/before0000/resemble.png"

    await fs.writeFile(out2, data2.getBuffer());
    console.log("File saved to %s", out2);

}

function parseNum(num) {
  num = Number(num);
  if (num < 10) {
    return "000" + num;
  } else if (num < 100) {
    return "00" + num;
  } else if (num < 1000) {
    return "0" + num;
  }
  return num + ""
}
getDiff();
