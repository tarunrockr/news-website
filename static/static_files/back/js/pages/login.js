/*
 *  Document   : login.js
 *  Author     : pixelcave
 */
var Login=function(){return{init:function(){var i=$("#form-login"),n=$("#form-register");$("#link-login").click(function(){i.slideUp(250),n.slideDown(250,function(){$("input").placeholder()})}),$("#link-register").click(function(){n.slideUp(250),i.slideDown(250,function(){$("input").placeholder()})})}}}();