//Foreign Key Change


$(document).ready(
  function(){
    var categoryField = $('#id_category')
    var selected_option_value_1=$("#id_category option:selected").val();
    console.log(selected_option_value_1)
    categoryField.change(
      function(event){
        var actionEndpoint = '/products/create/'
        var formData = $("#id_category option:selected").val()
        console.log(formData)
        console.log(selected_option_value_1)
        $.ajax({
            url: actionEndpoint,
            data: {selected: formData},
            success: function(data){
            var id_size = $('#id_size').empty()
            $.each(data.sizes,
              function(index, value){
              $(id_size).append('<option value='+value.id+'>'+value.size+'</option>')
              console.log(value)
              })//each
            
              
            },//function
        })//ajax
        })//function(event)
  })//document.ready
