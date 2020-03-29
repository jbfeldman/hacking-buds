
let button = document.getElementById('button');
let list = document.getElementById('word_list')
active_tab_url = ''

function update_list(parser_content){
    //new_content is a list of JS objects
    new_html = 'Suspicious phrases on this page:\n';
    new_html = '<ul>';
    this_page = parser_content.root_matches
    for (var word in this_page){
      to_add = '<li> Phrase: ' + word + '\nReason: ' + this_page[word].reason + '\n';
      to_add += 'Risk: ' + this_page[word].risk + '\n Count: '+  this_page[word].count;
      to_add += '</li>';
      new_html+= to_add;
    }
    new_html += '</ul>';


    if (Object.keys(parser_content.link_matches).length != 0){
      other_pages = parser_content.link_mathces
      new_html += 'Suspicious phrases in links on this page'
      new_html += JSON.stringify(parser_content.link_matches)
    //   new_html += '<ul>';
    //   for (var new_word in other_pages){
    //     to_add = '<li> Phrase: ' + new_word + '\nReason: ' + other_pages[new_word].reason + '\n';
    //     to_add += 'Risk: ' + other_pages[new_word].risk + '\n Count: '+  other_pages[new_word].count;
    //     to_add += '\nurls: ' + JSON.stringify(other_pages[new_word].urls)
    //     to_add += '</li>';
    //     new_html += to_add;
    //   }
    }
    // new_html += '</ul>'

    list.innerHTML=new_html;
}
function doStuffWithDom(domContent) {
  list.innerHTML = 'Loading...'
  fetch('http://localhost:5000/api', {'method': 'POST', 'mode': 'cors',
                                      credentials: 'include',
                                      body: JSON.stringify({"html": String(domContent), 'url': active_tab_url}),
                                      headers: {
                                        'Content-Type': 'application/json'
                                      }
                                    })
    .then((response) => {
        return response.json();
      })
    .then((res) =>{
      update_list(res);
    });
}

button.onclick = function(element) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    active_tab_url = tabs[0].url
    chrome.tabs.sendMessage(tabs[0].id, {text: 'gimme_page'}, doStuffWithDom);
  });
};
