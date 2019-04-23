chrome.runtime.onMessage.addListener(function(request, sender, callback) {
  var start = new Date()
  scroll(document.body.scrollWidth, document.body.scrollHeight); // Scroll to bottom
  setTimeout(function (){

  // Something you want delayed.
    scroll(0,0); // Scroll to top
    setTimeout(function (){

  // Something you want delayed.
      var dom1 = DomVRT.Extractor.currentAppToFile(null);
      console.log(dom1);

      var end = new Date() - start
      console.info('Execution time: %dms', end)
    }, 250);

  }, 250);

});

function coffeeio() {
  document.querySelector('.front-title').textContent = 'CoffeeIO hell world';
  document.querySelector('.post-list-item-desc h2').remove();
  document.querySelector('.post-list-item:nth-child(2) p').style.color = "green";
  document.querySelector('.post-list-item-display').style.color = "red";
  e1 = document.querySelector('.scrollreveal:last-child h2');
  console.log(e1.innerHtml);
  e1.innerHtml = e1.innerHtml + "<p>Added content</p>";
  console.log(e1.innerHtml);
  document.querySelector('.footer-social-icon img').style.marginRight = "1px";
}


(function() {
   DomVRT.Differ.index()
})();
