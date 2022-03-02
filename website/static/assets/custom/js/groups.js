$(function () {     
    $.ajax({
        type: "GET",
        url: "/api_groups",
        ajaxGridOptions: { contentType: 'application/json; charset=utf-8' },
        dataType: "json",
    }).done(function (groups) {
        groups.unshift({ id: "0", nombre: "" });
        $("#jsGrid").jsGrid({
            height: "auto",
            width: "100%",
  
            inserting: true,
            editing: true,
            sorting: true,
            paging: false,
            autoload: true,
            invalidMessage:"Algúnos datos estan erróneos, favor de validar el formulario de grupos.",
            //confirmDeleting: true,
            //deleteConfirm: "Do you really want to delete the client?",
            //filtering: true,

            //rowClick: function(args) {
            //    showDialog(args.item);
            //},
             
            controller: {
                loadData: function (filter) {
                    return $.ajax({
                        type: "GET",
                        url: "/api_groups",
                        ajaxGridOptions: { contentType: 'application/json; charset=utf-8' },
                        dataType: "json",
                    });
                },
                insertItem: function (item) {
                    var d = $.Deferred();
                    $.ajax({
                        type: "POST",
                        url: "/api_groups/insert",
                        data: JSON.stringify(item),
                        dataType: "json",
                        contentType: "application/json",
                    }).done(function(response){
                        $("#jsGrid").jsGrid("loadData");
                        alert(response.message);
                        d.resolve(response);
                    }).fail(function(response) {
                        alert(JSON.parse(response.responseText).message);
                    });
                },
                updateItem: function (item) {
                    var d = $.Deferred();
                    $.ajax({
                        type: "PUT",
                        url: "/api_groups/update",
                        data: JSON.stringify(item),
                        dataType: "json",
                        contentType: "application/json",
                    }).done(function(response){
                        $("#jsGrid").jsGrid("loadData");
                        alert(response.message);
                        d.resolve(response);
                    }).fail(function(response) {
                        alert(JSON.parse(response.responseText).message);
                    });
                    
                },
                deleteItem: function (item) {
                    return $.ajax({
                        type: "DELETE",
                        url: "/api_users/delete",
                        data: item
                    });
                }
            },
            fields: [
                {name: "nombre", title: "Grupo", type: "text", width: 30, validate: "required"},
                {name: "descripcion", title: "Descripción", type: "text",  width: 100, validate: "required"},
                {type: "control", deleteButton: false,width: 20}
            ]
        });
    });
});