
var dom1 = DomVRT.Extractor.extractCurrentAppAsJSON();

// document.querySelector('.user-info').style.color = 'blue';

var dom2 = DomVRT.Extractor.extractCurrentAppAsJSON();

var result = DomVRT.Differ.compareJSON(dom1, dom2);
