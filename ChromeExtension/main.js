console.log('Start');

var minify = false;
var save = true;
var mod = true;


var dom1 = DomVRT.Extractor.currentAppToJSON(minify);
if (save) DomVRT.Extractor.currentAppToFile(null, minify);
console.log(dom1);

if (mod) {
  // document.querySelector('#LC148').style.color = 'yellow';
  // document.querySelector('body').style.paddingTop = '10px';
  // document.querySelector('.footer .mr-3').style.color = 'yellow';
  // document.querySelector('.commit-tease .btn-link').style.color = 'yellow';
  // changeStyle('.commit-tease .btn-link', 'color', 'yellow');

  // Style
  changeStyle('.front-title', 'color', 'blue');

  // Remove
  elem = document.querySelector('.post-list-item-desc a');
  elem.parentNode.removeChild(elem);

  // Change content
  document.querySelector('.front-title').innerHTML = "CoffeeIO - change";

  // Add
  elem2 = document.querySelector('.post-list');
  elem2.innerHTML = elem2.innerHTML + "<div>Added content</div>";

  var dom2 = DomVRT.Extractor.currentAppToJSON(minify);

  if (save) DomVRT.Extractor.currentAppToFile(null, minify);
  console.log(dom2);
}



// var result = DomVRT.Differ.compareJSON(dom1, dom2);
//
// console.log(result);


function changeStyle(selector, prop, value) {
  var elem = document.querySelector(selector);
  if (elem != null) {
    elem.style.setProperty(prop, value);
  }
}
