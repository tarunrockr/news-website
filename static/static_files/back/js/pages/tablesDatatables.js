/*
 *  Document   : tablesDatatables.js
 *  Author     : pixelcave
 */
var TablesDatatables=function(){return{init:function(){App.datatables(),$("#example-datatable").dataTable({aoColumnDefs:[{bSortable:!1,aTargets:[1,5]}],iDisplayLength:10,aLengthMenu:[[10,20,30,-1],[10,20,30,"All"]]}),$(".dataTables_filter input").addClass("form-control").attr("placeholder","Search"),$(".dataTables_length select").addClass("form-control")}}}();