/* global CustomEvent */

console.log('monkeyPack running')

let oldOpen = window.XMLHttpRequest.prototype.open
window.XMLHttpRequest.prototype.open = function () {
  oldOpen.apply(this, arguments)
  console.log('XHR open params: ', arguments)
  sendBackAjaxRequestData(arguments)
  console.log('----------------------分割线----------------------------------------')
}
//
//
let oldSetRequestHeader = window.XMLHttpRequest.prototype.setRequestHeader
window.XMLHttpRequest.prototype.setRequestHeader = function () {
  oldSetRequestHeader.apply(this, arguments)
  console.log('requestHeader params: ',arguments)
}
//


let oldSend =  window.XMLHttpRequest.prototype.send
window.XMLHttpRequest.prototype.send = function () {
  let self = this
  this.addEventListener('load', function() {
    console.log('XHR response Headers: ', self.getAllResponseHeaders())
    console.log('----------------------分割线---------------------------------')
    try {
      let data = JSON.parse(this.responseText)
      sendBackAjaxLoadData(data)
    } catch (error) {
      console.log('maybe jsonp')
      console.log('XHR response Content: ', this.responseText)
    }
    console.log('----------------------分割线-STRING--------------------------------')
    console.log('XHR response Content: ', this.responseText)
  });
  this.addEventListener('error', function(error) {
    console.error('error:', error)
  });
  oldSend.apply(this, arguments)
  console.log('send content: ', arguments)
}


function sendBackAjaxRequestData(data) {
  let event = new CustomEvent('ajaxRequestData', { 'detail': data });
  document.dispatchEvent(event)
}

function sendBackAjaxLoadData (data) {
  let event = new CustomEvent('ajaxDataBackEvent', { 'detail': data });
  document.dispatchEvent(event)
}
