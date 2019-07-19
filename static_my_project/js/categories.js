//Foreign Key Change


$(document).ready(
  function(){
    var categoryField = $('#id_category')
    var selected_option_value_1=$("#id_category option:selected").val();
    console.log(selected_option_value_1)
    categoryField.change(
      function(){
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



//filterboxeslogic
var foot = $(".footwear")
var out = $(".outerwear")
var top = $(".tops")
var bot = $(".bottoms")
var acc = $(".accessories")
// if(".customCheckboxfootwear:checked"){
//         $('.outwear').prop('checked', false)
//         $('.tops').prop('checked', false)
//         $('.bottoms').prop('checked', false)
//         $('.accessories').prop('checked', false)
//         tops()
//         outwear()
//         bottoms()
//         accessories()
//         $(".outwear").prop("disabled", true)
//         $(".tops").prop("disabled", true)
//         $(".bottoms").prop("disabled", true)
//         $(".accessories").prop("disabled", true)
//     }

// if(".customCheckboxoutwear:checked"){
//         $('.footwear').prop('checked', false)
//         $('.tops').prop('checked', false)
//         $('.bottoms').prop('checked', false)
//         $('.accessories').prop('checked', false)
//         tops()
//         footwear()
//         bottoms()
//         accessories()
//         $(".footwear").prop("disabled", true)
//         $(".tops").prop("disabled", true)
//         $(".bottoms").prop("disabled", true)
//         $(".accessories").prop("disabled", true)
//     }


// if(".customCheckboxtops:checked"){
//         $('.footwear').prop('checked', false)
//         $('.outwear').prop('checked', false)
//         $('.bottoms').prop('checked', false)
//         $('.accessories').prop('checked', false)
//         outwear()
//         footwear()
//         bottoms()
//         accessories()
//         $(".footwear").prop("disabled", true)
//         $(".outwear").prop("disabled", true)
//         $(".bottoms").prop("disabled", true)
//         $(".accessories").prop("disabled", true)
//     }






function footwear() {
    if($(".footwear")[0].checked) {
        $(".footwear-btn").css('display', 'block')
    }
    else{
        $(".footwear-btn").css('display', 'none')
        $('.customCheckboxfootwear').prop('checked', false)
        $(".outerwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)
    }
}
function outerwear() {   
    if(out[0].checked) {
        $(".outerwear-btn").css('display', 'block')
    }
    else{
        $(".outerwear-btn").css('display', 'none')
        $('.customCheckboxouterwear').prop('checked', false)
        $(".footwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)
    }
}
function tops() {   
    if(top[0].checked) {
        $(".tops-btn").css('display', 'block')
    }
    else{
        $(".tops-btn").css('display', 'none')
        $('.customCheckboxtops').prop('checked', false)
        $(".outerwear").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)
    }
}
function bottoms() {   
    if(bot[0].checked) {
        $(".bottoms-btn").css('display', 'block')
    }
    else{
        $(".bottoms-btn").css('display', 'none')
        $('.customCheckboxbottoms').prop('checked', false)
        $(".outerwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".accessories").prop("disabled", false)
    }
}
function accessories() {   
    if(acc[0].checked) {
        $(".accessories-btn").css('display', 'block')
    }
    else{
        $(".accessories-btn").css('display', 'none')
        $('.customCheckboxaccessories').prop('checked', false)
        $(".outerwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".footwear").prop("disabled", false)

    }
}
//checkboxes
$(".footwear").change(function(){

  footwear()});
$(".outerwear").change(function() {
  outerwear()
});
$(".tops").change(function() {
  tops()
});
$(".bottoms").change(function() {
  bottoms()
});
$(".accessories").change(function () {
  accessories()
});
//checkboxes
// checkboxes - sizes
$(".customCheckboxfootwear").change(
  function(){
    if(this.checked){
        $('.outerwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.accessories').prop('checked', false)
        tops()
        outerwear()
        bottoms()
        accessories()
        $(".outerwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxfootwear:checked').length==0){
        $(".outerwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxouterwear").change(
  function(){

    if(this.checked){
        $('.footwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.accessories').prop('checked', false)
        footwear()
        tops()
        bottoms()
        accessories()
        $(".footwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxouterwear:checked').length==0){
        $(".footwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxtops").change(
  function(){
    if(this.checked){
        $('.outerwear').prop('checked', false)
        $('.footwear').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.accessories').prop('checked', false)
        footwear()
        outerwear()
        bottoms()
        accessories()
        $(".outerwear").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxtops:checked').length==0){
        $(".outerwear").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxbottoms").change(
  function(){
    if(this.checked){
        $('.outerwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.footwear').prop('checked', false)
        $('.accessories').prop('checked', false)
        footwear()
        tops()
        outerwear()
        accessories()
        $(".outerwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxbottoms:checked').length==0){
        $(".outerwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxaccessories").change(
  function(){
    if(this.checked){
        $('.outerwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.footwear').prop('checked', false)
        footwear()
        tops()
        outerwear()
        bottoms()
        $(".outerwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        }
    if ($('.customCheckboxaccessories:checked').length==0){
        $(".outerwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".footwear").prop("disabled", false)

    }
  })//change
//filterboxeslogic


//slider filter box
$("#slider").slideReveal({
  trigger: $("#trigger"),
  push: false,
  overlay: true,
  overlayColor:'rgba(0,0,0,0.5)',
  width:'500px',
});
//slider filter box

$("#slider_2").slideReveal({
  trigger: $("#trigger_2"),
  push: false,
  overlay: true,
  overlayColor:'rgba(0,0,0,0.5)',
  width:'500px',
});



// Add slideDown animation to Bootstrap dropdown when expanding.
$('.customDropRight').on('show.bs.dropdown', function() {
  $(this).find('.customDropRightMenu').first().stop(true, true).slideDown();
});

// Add slideUp animation to Bootstrap dropdown when collapsing.
$('.customDropRight').on('hide.bs.dropdown', function() {
  $(this).find('.customDropRightMenu').first().stop(true, true).slideUp();
});
$('.customDropRightMenu').click(function(e) {
  e.stopPropagation();
});






  })//document.ready
