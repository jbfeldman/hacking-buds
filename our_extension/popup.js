
let button = document.getElementById('button');
let list = document.getElementById('word_list')

function update_list(new_word_list){
    //new_content is a list of JS objects
    new_html = '<ul>'
    for (i in new_word_list){
        new_html += '<li> Word: ' + new_word_list[i].word + '\n Reason: ' + new_word_list[i].reason + '</li>'
    }
    new_html += '</ul>'
    list.innerHTML=new_html
}
function doStuffWithDom(domContent) {
    //update_list('whatcha say about this new Dom shiiiiiiiiiiiiiiit')
    console.log('I received the following DOM content:\n' + domContent);
}

button.onclick = function(element) {
  update_list([{'word': 'sex', 'reason': "It's scary"}, {'word': 'Jathan', 'reason': 'Never really trusted him'}])
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {text: 'gimme_page'}, doStuffWithDom);
  });
};
