
let button = document.getElementById('button');
let list = document.getElementById('word_list')
active_tab_url = ''

function update_list(parser_content){
    //new_content is a list of JS objects
    new_html = 'Suspicious phrases on this page:\n';
    new_html = '<ul class="panel">';
    this_page = parser_content.root_matches
    for (var word in this_page){
      to_add = '<li> <b>' + word + '</b><ul> <li> Reason: ' + this_page[word].reason + '</li>';
      to_add += '<li> Risk: ' + this_page[word].risk + '</li> \n<li> Count: '+  this_page[word].count;
      to_add += '</li> </ul> </li>';
      new_html+= to_add;
    }
    new_html += '</ul>';

    entries = Object.entries(parser_content.link_matches)
    if (entries.length != 0){
      new_html+= 'Suspicious Phrases on links on this page'
      new_html += '<ul class="panel">';
      for (var i in entries){
        to_add = '<li> <b>' + entries[i][0] + '</b><ul> <li> Reason: ' + entries[i][1].reason + '</li>';
        to_add += '<li> Risk: ' + entries[i][1].risk + '</li> \n<li> Count: '+  entries[i][1].count;
        to_add += '<li>' + 'URLS'  + '<ul>';
        for (var j in entries[i][1].urls){
          to_add += '<li>' + entries[i][1].urls[j] + '</li>'
        }
        to_add += '</li> </ul></li> </ul> </li>';
        new_html+= to_add;
      }

    }
    new_html += '</ul>'

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
