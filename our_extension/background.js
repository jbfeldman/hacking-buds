// Regex-pattern to check URLs against.
// It matches URLs like: http[s]://[...]stackoverflow.com[...]
// var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?[a-z]*\.com/;

// A function to use as callback
function doStuffWithDom(domContent) {
    console.log('I received the following DOM content:\n' + domContent);
}


fetch('http://localhost:5000/api', {'method': 'GET', 'mode': 'cors', credentials: 'include'})
  .then((response) => {
      return response.text();
    })
  .then((text) =>{
    console.log(text)
  });


// When the browser-action button is clicked...
chrome.browserAction.onClicked.addListener(function (tab) {
    // ...check the URL of the active tab against our pattern and...
    // if (urlRegex.test(tab.url)) {
      //  ...if it matches, send a message specifying a callback too
        chrome.tabs.sendMessage(tab.id, {text: 'gimme_page'}, doStuffWithDom);
    // }
});
