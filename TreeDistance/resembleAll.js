'use strict';

const { lstatSync, readdirSync } = require('fs')
const { join } = require('path')
const compareImages = require("resemblejs/compareImages");
const fs = require("mz/fs");

const isDirectory = source => lstatSync(source).isDirectory()
const getDirectories = source =>
  readdirSync(source).map(name => join(source, name)).filter(isDirectory)


  async function getDiff(dir) {
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
          await fs.readFile(dir + "/before0000/image.png"),
          await fs.readFile(dir + "/after0000/image.png"),
          options
      );
      const out1 = dir + "/after0000/resemble.png";

      await fs.writeFile(out1, data.getBuffer());
      console.log("File saved to %s", out1);

      const data2 = await compareImages(
          await fs.readFile(dir + "/after0000/image.png"),
          await fs.readFile(dir + "/before0000/image.png"),
          options
      );
      const out2 = dir + "/before0000/resemble.png"

      await fs.writeFile(out2, data2.getBuffer());
      console.log("File saved to %s", out2);

  }

const dirs = getDirectories('./comparisons');
dirs.forEach(function (dir) {
  getDiff(dir);
});



// for (let j = 0; j < process.argv.length; j++) {
//     console.log(j + ' -> ' + ();
// }
