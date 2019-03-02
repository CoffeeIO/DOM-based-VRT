console.log('Start');

var minify = false;
var save = false;

var dom1 = DomVRT.Extractor.currentAppToJSON(minify);
if (save) DomVRT.Extractor.currentAppToFile(null, minify);

// document.querySelector('#LC148').style.color = 'yellow';
// document.querySelector('body').style.paddingTop = '10px';
// document.querySelector('.footer .mr-3').style.color = 'yellow';
// document.querySelector('.commit-tease .btn-link').style.color = 'yellow';
changeStyle('.commit-tease .btn-link', 'color', 'yellow');

var dom2 = DomVRT.Extractor.currentAppToJSON(minify);

console.log(dom1);
console.log(dom2);

if (save) DomVRT.Extractor.currentAppToFile(null, minify);

// var result = DomVRT.Differ.compareJSON(dom1, dom2);
//
// console.log(result);


function changeStyle(selector, prop, value) {
  var elem = document.querySelector(selector);
  if (elem != null) {
    elem.style.setProperty(prop, value);
  }
}
