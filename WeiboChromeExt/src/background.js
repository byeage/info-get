import 'whatwg-fetch'

/* global chrome */
/* global fetch */
console.log('background is runing')
let ajaxLoadURL = ['http://s.weibo.com/*', 'https://s.weibo.com/*']
const resourceUrl = chrome.extension.getURL('monkeyPack.js')
console.log(resourceUrl)

const actualCode = `
  console.log('monkey patch add success !');
  var s = document.createElement('script');
  s.setAttribute('id', 'chrome-plugins');
  s.src = '${resourceUrl}';
  s.onload = function() {
    this.remove();
  };
  (document.head || document.documentElement).appendChild(s);
`



// 注入js
function insertScript(tabId) {
  chrome.tabs.executeScript(tabId,
    {
      code: actualCode,
      runAt: 'document_end'},  (result) => {
        console.log('executeScript success')
  })
}


// 在页面打开时注入css 和 js
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  let hasMatched = ajaxLoadURL.some(d => {
    let reg = new RegExp(d)
    let url = tab.url
    return reg.test(url)
  })
  if (hasMatched) {
    insertScript(tabId)
  }
  console.log(tabId, changeInfo, tab)
});


chrome.tabs.onCreated.addListener(function(tab) {
  console.log('create tab')
  insertScript(tab.id)
})

chrome.tabs.query({
  active: true
}, function (tabArray) {
  tabArray.forEach(tab => {
    insertScript(tab.id)
  })
})

chrome.runtime.onMessage.addListener(function(request, sender, callback) {
  console.log(request, sender, callback)
  const url = 'http://127.0.0.1:5000/posts'
  if (request.type === 'WEIBO_SCRAPY') {

      chrome.storage.sync.get(['requestHeader'], (res) => {
        console.log(res)
        const header = res.requestHeader
        const message = Object.assign({}, request, {
          header: header
        })
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(message)
        })
      })
  }
})








chrome.webRequest.onBeforeSendHeaders.addListener(
  function(details) {
    const matches = 'https://s.weibo.com'
    console.log('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    console.log(details.requestHeaders)
    if(details.initiator === matches) {
      let headers = {}
      details.requestHeaders
      .filter(d => d.name !== 'Cookie')
      .forEach(d => {
        headers[d.name] = d.value
      })
      chrome.storage.sync.remove(['requestHeader'])
      chrome.storage.sync.set({requestHeader: headers}, function() {
         console.log('Header' , headers)
       });
    }

    return {
      cancle: true
    }
  },
  // filters
  {urls: ['<all_urls>']},
      ['requestHeaders']);
