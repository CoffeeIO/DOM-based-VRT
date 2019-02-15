console.log('Start');
var dom1 = DomVRT.Extractor.currentAppToJSON();

document.querySelector('#LC148').style.color = 'yellow';
// document.querySelector('body').style.paddingTop = '10px';
document.querySelector('.footer .mr-3').style.color = 'yellow';

var dom2 = DomVRT.Extractor.currentAppToJSON();

DomVRT.Extractor.currentAppToFile();

var result = DomVRT.Differ.compareJSON(dom1, dom2);

console.log(result);
