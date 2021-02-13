/*
 *  Document   : formsGeneral.js
 *  Author     : pixelcave
 */
var FormsGeneral=function(){return{init:function(){$(".toggle-bordered").click(function(){$(this).parents(".block").find("form").toggleClass("form-bordered")})}}}();