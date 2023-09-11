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
            invalidMessage: "Algunos datos están erróneos, favor de validar el formulario de usuarios.",
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
                    }).done(function (response) {
                        $("#jsGrid").jsGrid("loadData");
                        alert(response.message);
                        d.resolve(response);
                    }).fail(function (response) {
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
                { name: "username", title: "Usuario", type: "text", width: 60, validate: "required" },
                { name: "email", title: "Correo", type: "text", width: 50, validate: "required" },
                { name: "grupo", title: "Grupo", type: "select", items: groups, valueField: "id", textField: "nombre", width: 50, validate: "required"},
                { name: "activo", title: "Activo", type: "checkbox", width: 50, filtering: false, sorting: false, validate: "required" },
                {
                    name: "password", title: "Password", align: "center", width: 60,
                    itemTemplate: function (value) {
                        return "<span class='password-cell'>" + value.replace(/./g, '*').slice(0, 10) + "</span>";
                    },
                    insertTemplate: function () {
                        var $input = $("<input type='password'  class='password-input' />");
                        return $input;
                    },
                    editTemplate: function (value, item) {
                        var $input = $("<input type='password'  class='password-input' />");
                        $input.val(value);
                        $input.on("input", function () {
                            item.password = $(this).val();
                        }).addClass("password-cell");
                        return $input;
                    }
                },
                { type: "control", deleteButton: false }
            ]
        });
    });
});
