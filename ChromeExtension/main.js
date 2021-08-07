chrome.runtime.onMessage.addListener(function(request, sender, callback) {
  var urls = getUrls();
  var viewports = getViewports();
  var result = DomVRT.Extractor.processUrls(urls, viewports)
});

(function() {
  console.log('Running domvrt 2');

  window.addEventListener('load', (event) => {

    const urlParams = new URLSearchParams(window.location.search);
    const runDomVrt = urlParams.get('domVrtRun');

    console.log('page is fully loaded');
    if (runDomVrt) {
      setTimeout(function () {

        document.querySelector('body').style['overflow'] = 'hidden';

        // Scroll to bottom
        scroll(document.body.scrollWidth, document.body.scrollHeight);
        setTimeout(function () {

          // Scroll to top
          scroll(0,0);
          setTimeout(function () {

            setTimeout(function(){
              var dom1 = DomVRT.Extractor.currentAppToFile(null);

              setTimeout(function(){
                window.close();
              }, 10000);

            }, 3000);

          }, 10000);

        }, 10000);
      }, 5000);

    }

  });

})();