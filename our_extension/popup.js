
let button = document.getElementById('button');
let list = document.getElementById('word_list')

function update_list(new_word_list){
    //new_content is a list of JS objects
    new_html = '<ul>'
    for (i in new_word_list){
        new_html += '<li> Phrase: ' + new_word_list[i].phrase + '\n Reason: ' + new_word_list[i].reason + '</li>'
    }
    new_html += '</ul>'
    list.innerHTML=new_html
}
function doStuffWithDom(domContent) {
  fetch('http://localhost:5000/api', {'method': 'POST', 'mode': 'cors',
                                      credentials: 'include',
                                      body:'{"html": "domContent"}',
                                      headers: {
                                        'Content-Type': 'application/json'
                                      }
                                    })
    .then((response) => {
        return response.json();
      })
    .then((res) =>{
      update_list(res)
    });
}

button.onclick = function(element) {
  update_list([{'word': 'sex', 'reason': "It's scary"}, {'word': 'Jathan', 'reason': 'Never really trusted him'}])
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {text: 'gimme_page'}, doStuffWithDom);
  });
};
