
let button = document.getElementById('button');
let list = document.getElementById('word_list')
active_tab_url = ''

function update_list(parser_content){
    this_page = parser_content.root_matches
    new_html = 'This Pages Score: ' + JSON.stringify(this_page.score)
   // new_html = 'Suspicious phrases on this page:\n';
    new_html += '<ul class="panel">';
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
        to_add = '<li> <b>' + entries[i][0] + '</b><ul> <li> Score: ' + entries[i][1].score + '</li>';
        to_add += '<li>' + 'terms'  + '<ul>';
        for (var j in entries[i][1].terms){
          to_add += '<li>' + entries[i][1].terms[j] + '</li>'
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
  fetch('http://localhost:5000/api'/*'http://chtc-uncalled-four.us-west-2.elasticbeanstalk.com/api'*/, {'method': 'POST', 'mode': 'cors',
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
