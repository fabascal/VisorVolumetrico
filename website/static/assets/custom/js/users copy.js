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
            invalidMessage:"Algúnos datos estan erróneos, favor de validar el formulario de usuarios.",
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
                        url: "/api_users",
                        ajaxGridOptions: { contentType: 'application/json; charset=utf-8' },
                        dataType: "json",
                    });
                },
                insertItem: function (item) {
                    return $.ajax({
                        type: "POST",
                        url: "/api_users/insert",
                        data: JSON.stringify(item),
                        dataType: "json",
                        contentType: "application/json",
                    });
                },
                updateItem: function (item) {
                    var d = $.Deferred();
                    $.ajax({
                        type: "PUT",
                        url: "/api_users/update",
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
                {name: "username", title: "Usuario", type: "text", width: 60, validate: "required"},
                {name: "email", title: "Correo", type: "text",  width: 50, validate: "required"},
                {name: "grupo", title: "Grupo", type: "select", items: groups, valueField: "id", textField: "nombre",width: 50, validate: "required"},
                {name: "activo", title: "Activo", type: "checkbox", width: 50, filtering: false, sorting: false, validate: "required"},
                {name: "password", title: "Password", align: "center",width: 30,height:10,
            	itemTemplate: function(value, item) {
              	return $("<button class='btn btn-default'> <i class='fas fa-unlock-alt'></i> </button>")
                		.on("click", function() {
                            //funcion para cambio de contraseña mediante correo.
               				alert("button clicked" + item.id);
                      return false;
                    });
              }
            },
                {type: "control", deleteButton: false,}
            ]
        });
    });
});