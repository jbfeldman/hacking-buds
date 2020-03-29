// Listen for messages

console.log('printing out random message')
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    console.log('received a message')
    // If the received message has the expected format...
    if (msg.text === 'gimme_page') {
        console.log('received gimme message')
        // Call the specified callback, passing
        // the web-page's DOM content as argument
        sendResponse(document.all[0].outerHTML);
    }
});
