import React, {Component} from 'react'
import css from './css/style.css'
/* global chrome */

class SendWeiboInformation extends Component {

  constructor() {
    super()
    this.state = {
        response: '',
        header: {}
      }
  }
  convertCookie(cookies) {
    let tmp = {}
    cookies.split(';').forEach(d => {
      let [key, value] = d.split('=')
      tmp[key.trim()] = value
    })
    return tmp
  }
  onClick = () => {
    const cookie = this.convertCookie(document.cookie)
    const url = window.location.href
    const message = {
      type: 'WEIBO_SCRAPY',
      cookie,
      url
    }
    chrome.runtime.sendMessage(message, (response) => {
      this.setState({
        response: 'response'
      })
    })
  }
  render () {


    return (

      <div>
        <button className={css.button} onClick={() => this.onClick()}>Start</button>
        <div>{this.response}</div>
      </div>
    )
  }
}

export default SendWeiboInformation
