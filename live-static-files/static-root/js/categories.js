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
var out = $(".outwear")
var top = $(".tops")
var bot = $(".bottoms")
var acc = $(".accessories")
if(".customCheckboxfootwear:checked"){
    $('.outwear').prop('checked', false)
    $('.tops').prop('checked', false)
    $('.bottoms').prop('checked', false)
    $('.footwear').prop('checked', false)
    footwear()
    tops()
    outwear()
    bottoms()
    $(".outwear").prop("disabled", true)
    $(".tops").prop("disabled", true)
    $(".bottoms").prop("disabled", true)
    $(".footwear").prop("disabled", true)
    }


$(".customCheckboxoutwear").change(
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
    if ($('.customCheckboxoutwear:checked').length==0){
        $(".footwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxtops").change(
  function(){
    if(this.checked){
        $('.outwear').prop('checked', false)
        $('.footwear').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.accessories').prop('checked', false)
        footwear()
        outwear()
        bottoms()
        accessories()
        $(".outwear").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxtops:checked').length==0){
        $(".outwear").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxbottoms").change(
  function(){
    if(this.checked){
        $('.outwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.footwear').prop('checked', false)
        $('.accessories').prop('checked', false)
        footwear()
        tops()
        outwear()
        accessories()
        $(".outwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxbottoms:checked').length==0){
        $(".outwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change

    if(".customCheckboxaccessories:checked"){
        $('.outwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.footwear').prop('checked', false)
        footwear()
        tops()
        outwear()
        bottoms()
        $(".outwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        }
    if ($('.customCheckboxaccessories:checked').length==0){
        $(".outwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".footwear").prop("disabled", false)

    }


function footwear() {
    if($(".footwear")[0].checked) {
        $(".footwear-btn").css('display', 'block')
    }
    else{
        $(".footwear-btn").css('display', 'none')
        $('.customCheckboxfootwear').prop('checked', false)
        $(".outwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)
    }
}
function outwear() {   
    if(out[0].checked) {
        $(".outwear-btn").css('display', 'block')
    }
    else{
        $(".outwear-btn").css('display', 'none')
        $('.customCheckboxoutwear').prop('checked', false)
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
        $(".outwear").prop("disabled", false)
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
        $(".outwear").prop("disabled", false)
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
        $(".outwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".footwear").prop("disabled", false)

    }
}
//checkboxes
$(".footwear").change(function(){

  footwear()});
$(".outwear").change(function() {
  outwear()
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
        $('.outwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.accessories').prop('checked', false)
        tops()
        outwear()
        bottoms()
        accessories()
        $(".outwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxfootwear:checked').length==0){
        $(".outwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxoutwear").change(
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
    if ($('.customCheckboxoutwear:checked').length==0){
        $(".footwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxtops").change(
  function(){
    if(this.checked){
        $('.outwear').prop('checked', false)
        $('.footwear').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.accessories').prop('checked', false)
        footwear()
        outwear()
        bottoms()
        accessories()
        $(".outwear").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxtops:checked').length==0){
        $(".outwear").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".bottoms").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxbottoms").change(
  function(){
    if(this.checked){
        $('.outwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.footwear').prop('checked', false)
        $('.accessories').prop('checked', false)
        footwear()
        tops()
        outwear()
        accessories()
        $(".outwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        $(".accessories").prop("disabled", true)
        }
    if ($('.customCheckboxbottoms:checked').length==0){
        $(".outwear").prop("disabled", false)
        $(".tops").prop("disabled", false)
        $(".footwear").prop("disabled", false)
        $(".accessories").prop("disabled", false)

    }
  })//change
$(".customCheckboxaccessories").change(
  function(){
    if(this.checked){
        $('.outwear').prop('checked', false)
        $('.tops').prop('checked', false)
        $('.bottoms').prop('checked', false)
        $('.footwear').prop('checked', false)
        footwear()
        tops()
        outwear()
        bottoms()
        $(".outwear").prop("disabled", true)
        $(".tops").prop("disabled", true)
        $(".bottoms").prop("disabled", true)
        $(".footwear").prop("disabled", true)
        }
    if ($('.customCheckboxaccessories:checked').length==0){
        $(".outwear").prop("disabled", false)
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
