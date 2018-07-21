/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/monkeyPack.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/monkeyPack.js":
/*!***************************!*\
  !*** ./src/monkeyPack.js ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\n\n/* global CustomEvent */\n\nconsole.log('monkeyPack running');\n\nvar oldOpen = window.XMLHttpRequest.prototype.open;\nwindow.XMLHttpRequest.prototype.open = function () {\n  oldOpen.apply(this, arguments);\n  console.log('XHR open params: ', arguments);\n  sendBackAjaxRequestData(arguments);\n  console.log('----------------------分割线----------------------------------------');\n};\n//\n//\nvar oldSetRequestHeader = window.XMLHttpRequest.prototype.setRequestHeader;\nwindow.XMLHttpRequest.prototype.setRequestHeader = function () {\n  oldSetRequestHeader.apply(this, arguments);\n  console.log('requestHeader params: ', arguments);\n};\n//\n\n\nvar oldSend = window.XMLHttpRequest.prototype.send;\nwindow.XMLHttpRequest.prototype.send = function () {\n  var self = this;\n  this.addEventListener('load', function () {\n    console.log('XHR response Headers: ', self.getAllResponseHeaders());\n    console.log('----------------------分割线---------------------------------');\n    try {\n      var data = JSON.parse(this.responseText);\n      sendBackAjaxLoadData(data);\n    } catch (error) {\n      console.log('maybe jsonp');\n      console.log('XHR response Content: ', this.responseText);\n    }\n    console.log('----------------------分割线-STRING--------------------------------');\n    console.log('XHR response Content: ', this.responseText);\n  });\n  this.addEventListener('error', function (error) {\n    console.error('error:', error);\n  });\n  oldSend.apply(this, arguments);\n  console.log('send content: ', arguments);\n};\n\nfunction sendBackAjaxRequestData(data) {\n  var event = new CustomEvent('ajaxRequestData', { 'detail': data });\n  document.dispatchEvent(event);\n}\n\nfunction sendBackAjaxLoadData(data) {\n  var event = new CustomEvent('ajaxDataBackEvent', { 'detail': data });\n  document.dispatchEvent(event);\n}\n\n//# sourceURL=webpack:///./src/monkeyPack.js?");

/***/ })

/******/ });