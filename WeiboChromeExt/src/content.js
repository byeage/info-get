import React from 'react'
import ReactDOM from 'react-dom'
import css from './css/style.css'
import SendWeiboInformation from './SendWeiboInformation'
const wrapper = document.createElement('div')
wrapper.setAttribute('id', 'weibo-plugins')
const dom = document.querySelector('body').appendChild(wrapper)
console.log(css)
ReactDOM.render(
  <div className={css.weiboPlugins}>
    <SendWeiboInformation/>
  </div>,
  dom
)
