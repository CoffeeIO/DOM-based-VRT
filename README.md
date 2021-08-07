# DOM-Based-VRT

### Install

- Python 3 is required
- Pip 3 is required
- Node is required
- NPM is required

```bash
npm install

pip3 install termtables
pip3 install requests
pip3 install yattag
pip3 install six
pip3 install lorem
pip3 install pillow
pip3 install selenium
pip3 install numpy
```

### Step 1: Capture website
- Define website to capture in `config.yml`.
  - Define testing viewports to capture.
  - Define url(s) to capture.
  - Define delay between captures.
- `scripts/capture-mutate.js` is executed before capture of website, allowing you to modify the website before capture.
- Run `scripts/capture.sh CoffeeIO-1.2.0` to perform capture.
  - First param is optional. It is just tag metadata to make it easier to identity later.
- Each capture produces 2 files in `/captures`.
  - A PNG screenshot of the website at the specific viewport.
  - A JSON file containing.
    - The whole DOM tree and styles at capture.
    - Some meta information about the capture.
- In `/capture-summaries` a file is produced that describe all the captures and meta information.
  - ```javascript
    {
      "files": [ /* Captures */
        {
          "file": "captures/2021-08-07--11-10-43--1--innovationsfonden.dk--1600",
          "viewport": 1600,
          "url": "https://innovationsfonden.dk/"
        },...
      ],
      "tag": "CoffeeIO-1.2.0", /* Optional tag for searching */
      "domain": "innovationsfonden.dk",
      "id": "77ugJzaV0J", /* UUID of capture */
      "datetime": "2021-08-07--11-10-43", /* Datetime of capture */
      "execution": "85s", /* Total execution time of all captures */
      "config": { /* Copy of config file at time of capture */
        "viewports": [
          1600,
          1200,
          ...
        ],
        "urls": [
          "https://innovationsfonden.dk/",
          "https://innovationsfonden.dk/da/om-innovationsfonden",
          ...
        ],
        "delay": 3000
      },
      "key": -783019585 /* Hash key for disallowing invalid comparisons in compare.sh */
    }
    ```

### Step 2: List captures
- `scripts/list.sh` to list all captures
- `scripts/list.sh "1.2"` or `scripts/list.sh "coffeeio.com"` to list captures containing specific tag
- From the list, the unique ids will be shown, these are used for the compare command.
- Note: only captures with identical hashes can be compared.


### Step 3: Compare snapshots
- `scripts/compare.sh {id} {id}`
  - First id defines the before state of website, second id is the after state of the website.
- This produces a folder in `comparisons/test{number}` containing:
  - Each comparision in this folder is numbered and has two folders
  - `before{number}` and `after{number}` to represent files relating to before or after state.
    - In each folder there is 4 files:
    -  `image.png` The original screenshot.
    -  `image-diff.png` The screenshot with diff highlights.
    -  `image-diff-highlight.png` The diff highlights without the screenshot.
    -  `output.json` A JSON description of all detected differences.

---

# Folder structure

- `/ChromeExtension` - Chrome extension code
- `/src` - Source code of JavaScript module for capturing website data.
- `/dist` - Compiled files of the JavaScript module
- `/TreeDistance`
  - `/domvrt` - Source code of the Python module for comparison.
  - `/zss` - Source code of ZSS library with custom modifications
- `/captures` - Data input files for VRT tests
- `/capture-summaries` - Data output files for VRT tests
- `/comparisons` - Data input for distance correctness tests

# Chrome extension - for local capture of websites

## Install:
Go to Chrome, settings, 'more tools', 'extensions', 'load unpacked' and select the 'ChromeExtension' folder.

## Run:

#### Extractor:

In the top right corner there is an icon for the Chrome extension, press this to extract a snapshot of the DOM.

To use the abstraction layer to create the set of expected changes; open the console, switch the JavaScript context to use the Chrome extension.
Now call the module functions under DomVRT.Differ.

# ResembleJS - comparision

```
node resembleAll.js
```

Run a single test in `comparisions` folder.
```
node resembleTest.js {somefolder}
--- example
node resembleTest.js test0012
```



