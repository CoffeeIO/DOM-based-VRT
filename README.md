
# Chrome extension

## Install:

## Run:

#### Extractor:

In the top right corner there is an icon for the Chrome extension, press this to extract a snapshot of the DOM.

To use the abstraction layer to create the set of expected changes; open the console, switch the JavaScript context to use the Chrome extension.
Now call the module functions under DomVRT.Differ.

# ResembleJS

## Install:

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

```
setup.py
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
python3 test-distance-performance.py
```

#### Visual regression test

Run with resource retrieval

Run without resource retrieval
