$(".deleteReport").on("click", function(e){
    $.blockUI({ 
      message:'<h1>Eliminando el registro..</h1>'
    }); 
    const to_remove = $(this).closest('tr');
    var id = $(this).closest("tr").find(".nr").text();
    const url ='/deleteReport/'+id
    fetch(url)
    .then(function (response) {
        return response.json();
    }).then(function (text) {
        console.log(text.greeting); 
        to_remove.remove();
        $.unblockUI();
    }); 
    
  });
  $(".redoReport").on("click", function(){
    var id = $(this).closest("tr").find(".nr").text();
    try{
      d = {'id_report': id}     
      $.ajax({
        type: "POST",
        url: $('#update_report').val(),
        data: JSON.stringify(d),
        contentType: "application/json",
        dataType: 'json',
        success: function(response) {
          window.location.href = response.redirect
        }
        });
      } catch(error) {
        console.log(error)
      }   
  });
 $("#btn-read-sftp").on("click", function(){
  $.blockUI({ 
    message:'<h1>Procesando XML..</h1>'
  }); 
  fecha = document.getElementById("fecha").innerText;
  try{
    data = {'fecha':fecha};
    $.ajax({
      type: "POST",
      url: $('#read_sftp').val(),
      data: JSON.stringify(data),
      contentType: "application/json",
      dataType: 'json',
      success: function(response) {
        window.location.href = response.redirect
      }
    });
  }catch(error){
    console.log(error)
  }
 });

 