# Dream

### Configuration
`.env` or `config.yml`
- Define testing viewports
- Define url(s)
- Define delay

### Capture website
- `./capture.sh --tag=CoffeeIO-1.2.0`
- Output
  - Screenshot[]
  - DOM json[]
  - Summary json
    - List of all files in capture
    - Tag
    - Domain

### List captures
- `list.sh "{1.2 | coffeeio.com}"`
- ID
- Tag
- Url count
- Website domain
- Other info

### Compare snapshots
- `./compare.sh {id-before} {id-after}`

### Show visual comparison
- Website?

---

# Folder structure

- `/Excel` - Excel sheet for results and graphs
- `/ChromeExtension` - Chrome extension code
- `/src` - Source code of JavaScript module
- `/dist` - Compiled files of the JavaScript module
- `/TreeDistance`
  - `/domvrt` - Source code of the Python module
  - `/zss` - Source code of ZSS library with custom modifications
  - `/data-test` - Data input files for VRT tests
  - `/data-output` - Data output files for VRT tests
  - `/data-sample` - Data input for distance correctness tests
  - `/data-mutations` - Calls for the JavaScript handlers for each VRT test
  - `/distance-data` - Output files for tree distance tests

# Chrome extension

## Install:
Go to Chrome, settings, 'more tools', 'extensions', 'load unpacked' and select the 'ChromeExtension' folder.

## Run:

#### Extractor:

In the top right corner there is an icon for the Chrome extension, press this to extract a snapshot of the DOM.

To use the abstraction layer to create the set of expected changes; open the console, switch the JavaScript context to use the Chrome extension.
Now call the module functions under DomVRT.Differ.

# ResembleJS

## Install:
- node is required

## Run:

Run all tests in `data-output` folder.
```
node resembleAll.js
```

Run a single test in `data-output` folder.
```
node resembleTest.js {somefolder}
--- example
node resembleTest.js test0012
```

# Python

## Install:

- Python 3 is required.
- pip3 is required.


```
pip3 install selenium
pip3 install yattag
pip3 install six
pip3 install lorem
pip3 install image
pip3 install time
pip3 install requests

# Modify Treedistance/domvrt/node_tree.py:8
# Change path to the user specific path of the Treedistance folder.
```


## Run:

#### Tree edit distance (quality)


```
python3 test-distance-quality.py
```


#### Tree edit distance (speed)

```
./test-distance.sh
```

```
python3 test-distance-performance.py {tree size}
```

#### Visual regression test

Run with resource retrieval
```
python3 test-vrt.py
```

Run without resource retrieval.
Modify last parameter of `test-vrt.py:171` and `test-vrt.py:172` to `False`
```
python3 test-vrt.py
```

Get the summarize output of specific tests.
```
python3 summarize-output.py {somePattern}
--- example
python3 summarize-output.py zhang # returns the summary of zhang-shasha
python3 summarize-output.py insert--custom # returns the summary of custom on insert problems
```

#### Tree generator and mutator

Run generator and mutator on default settings.
Results are saved into `data-generator/state1.html` and `data-generator/state2.html`
```
python3 test-mutator.py
```

#### Resource retriever

Run resource generator on captured DOMs
```
python3 test-resource-retrieve.py
```


---
---
---



