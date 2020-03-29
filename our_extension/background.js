// Regex-pattern to check URLs against.
// It matches URLs like: http[s]://[...]stackoverflow.com[...]
// var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?[a-z]*\.com/;

// A function to use as callback
function doStuffWithDom(domContent) {
    console.log('I received the following DOM content:\n' + domContent);
}


fetch('http://chtc-uncalled-four.us-west-2.elasticbeanstalk.com/api', {'method': 'POST', 'mode': 'cors',
                                    credentials: 'include',
                                    body:'{"html": "Some random html"}',
                                    headers: {
                                      'Content-Type': 'application/json'
                                    }
                                  })
  .then((response) => {
      return response.json();
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
