//Foreign Key Change


$(document).ready(


  function(){
      

    var currentPath = window.location.href
    if ((currentPath.indexOf("update") != -1) || (currentPath.indexOf("create") != -1)){
    var actionEndpoint = '/products/create/'
    var genderField = $('#id_sex')
    var undercategoryField = $('#id_undercategory')
    var sizeField = $('#id_size')
    var conditionField =$('#id_condition')
    var inputUnder = $('.input-undercategory')
    var inputGender = $('.input-gender')
    var inputSize = $('.input-size')
    var inputCondition = $('.input-condition')
    var dropBoxSize = $('.category-size')
    if (currentPath.indexOf("update") != -1){
        initialOvercategory = $('#id_sex').attr('overcategory')
        initialGender = $('#id_sex').attr('gender')
        initialUndercategory = $('#id_undercategory').attr('undercategory')
        initialCategory = $('#id_undercategory').attr('category')
        initialSize = $('#id_size').attr('size')
        console.log(initialSize)
        initialCondition = $('#id_condition').attr('condition')
        idGender = $('#id_sex').attr('id_for_upd')
        idUndercat = $('#id_undercategory').attr('id_for_upd')
        idSize = $('#id_size').attr('id_for_upd')
        idCondition = $('#id_condition').attr('id_for_upd')
        inputGender.val(idGender)
        inputUnder.val(idUndercat)
        inputSize.val(idSize)
        inputCondition.val(idCondition)
        $('.overcategories').find("[initial_update='"+initialOvercategory+"']").addClass('background-black').siblings().removeClass('background-black')
        $('.'+initialOvercategory).find("[gender-for-cat='"+initialGender+"']").addClass('background-black').siblings().removeClass('background-black')
        $('.'+initialOvercategory).show()
        var categoryDrop = $('.categories')
        var categoryDropActive = $('.active-undercategory')
        $.ajax({
            url: actionEndpoint,
            data: {obj_id_gender: idGender},
            success: function(data){
                categoryDrop.html('')
                categoryDropActive.html('')
                $.each(data.categories,
                    function(index, category){
                        categoryDrop.append("<div class='col-12 categories-class' category-admin='"+category.category+"' value='"+category.category+"'><p value='"+category.category+"'>"+category.category_language+"</p></div>")
                        categoryDropActive.append("<div class='"+category.category+" category-undercategory'></div>")
                        $.each(data.undercategories,
                            function(index, undercategory){
                                if(category.category == undercategory.undercategory_for){
                                    $("."+category.category).append("<div class='col-12 undercategories-class' id_for_fk ='"+undercategory.id+"' category-for-size='"+category.category+"' undercategory-admin='"+undercategory.undercategory+"' value ='"+undercategory.undercategory_language+"'><p class='mb-0' id_for_fk ='"+undercategory.id+"'value ='"+undercategory.undercategory_language+"'>"+undercategory.undercategory_language+"</p></div>")
                                }//if undercat==cat
                        })//eachUndercategories
                      })//eachCategories
                var categoriesClass = document.getElementsByClassName("categories-class")
                var categoryUnder = document.getElementsByClassName("category-undercategory")
                attachHoverDropdown(categoriesClass, 'category-undercategory')
                attachClickDropdown(categoryUnder, 'active-undercategory', undercategoryField, inputUnder, true, false)
                $('.active-undercategory').find("."+initialCategory).show()
                $('.active-size').find("."+initialCategory+'-size').show()
                $('.active-undercategory').find("[undercategory-admin='"+initialUndercategory+"']").addClass('background-black').siblings().removeClass('background-black')
                $('.categories').find("[category-admin='"+initialCategory+"']").addClass('background-black').siblings().removeClass('background-black')
                $('.active-condition').find("[activated='"+initialCondition+"']").addClass('background-black').siblings().removeClass('background-black')
                $('.'+initialCategory+'-size').find("[for_black_size='"+initialSize+"-"+initialCategory+"']").addClass('background-black').siblings().removeClass('background-black')
                }//success

            })//ajax

    }//if update initials
    function attachHoverDropdown(dropbox, underbox){
        for (i=0;i<dropbox.length;i++){
            dropbox[i].onmouseover = function(e){
                var element = e.target
                var $element = $(element)
                if ($element.is('div')){
                    var choice = $element.attr('value')
                    $element.addClass('background-black').siblings().removeClass('background-black')
                }//if element is div
                else {
                    var choice = $element.attr('value')
                    $element.parent().addClass('background-black').siblings().removeClass('background-black')
                }//else
                var dropBoxUnder = $('.'+underbox)
                dropBoxUnder.hide()
                $('.'+choice).show()
            }//function on hover
        }//for dropovercat        
    }//attachHoverDropdown
    function attachClickDropdown(dropbox, klass, field, input, undercat, for_condition){
        for (i=0;i<dropbox.length;i++){
        dropbox[i].onclick = function(e){
            if (!for_condition){
                sizeField.val('')
                inputSize.val('')
                $('.active-size div').removeClass("background-black")
            }//if not for condition
            var element = e.target
            var $element = $(element)
            var elementId = $element.attr('id_for_fk')
            if ($element.is('div')){
                $("."+klass+" div div").removeClass("background-black");
                var chosen = $element.attr('value')
                var catForSize = $element.attr('category-for-size')
                $element.addClass('background-black').siblings().removeClass('background-black')
                }//if element is div
            else {
                $("."+klass+" div div").removeClass("background-black");
                var chosen = $element.attr('value')
                var catForSize = $element.parent().attr('category-for-size')
                $element.parent().addClass('background-black').siblings().removeClass('background-black')
                }//else
            if (undercat == true){
                dropBoxSize.hide()
                $('.'+catForSize+'-size').show()
                }//if undercat

            field.val(chosen)
            if (elementId){
                input.val(elementId)  
            }//ifId

            }//onclick
        }//for
    }//attachClickDropdown
    var underSize = document.getElementsByClassName("category-size")
    var conditionCondition = document.getElementsByClassName("condition-class")
    attachClickDropdown(underSize, 'active-size', sizeField, inputSize, false, false)
    attachClickDropdown(conditionCondition, 'active-condition', conditionField, inputCondition, false, true)
    function setDropdownWidth(id, dropdown){
        fieldWidth = document.getElementById(id).offsetWidth
        document.getElementsByClassName("dropdown-content")[dropdown].style.width = fieldWidth + 'px'
    }//setWidth
    setDropdownWidth('id_sex', 0)
    setDropdownWidth('id_undercategory', 1)
    setDropdownWidth('id_size', 2)
    setDropdownWidth('id_condition', 3)



    function myFunction(index, dropdownContent) {
        var overcategory = document.getElementsByClassName('overcategory')
        dropdownContent[index].classList.toggle("show");
        }//myFunction

    window.onclick = function(e) {
        var myDropdown = document.getElementsByClassName("dropdown-content");
        if (!e.target.matches('#id_sex')){
            if (myDropdown[0].classList.contains('show')) {
                myDropdown[0].classList.remove('show');
            }//if already shown - hide_sex
        }//if target is input field gender
        if (!e.target.matches('#id_undercategory')){
            if (myDropdown[1].classList.contains('show')) {
                myDropdown[1].classList.remove('show');
            }//if already shown - hide_undercat
        }//if target is input field undercat
        if (!e.target.matches('#id_size')){
            if (myDropdown[2].classList.contains('show')) {
                myDropdown[2].classList.remove('show');
            }//if already shown - hide_size
        }//if target is input field size
        if (!e.target.matches('#id_condition')){
            if (myDropdown[3].classList.contains('show')) {
                myDropdown[3].classList.remove('show');
            }//if already shown - hide_condition
        }//if target is input field condition
    }//click window
    var dropdownContent = document.getElementsByClassName("dropdown-content")
    genderField.click(function(){
        myFunction(0, dropdownContent)
    })//clickGender
    undercategoryField.click(function(){
        myFunction(1, dropdownContent)
    })//clickCategory
    sizeField.click(function(){
        myFunction(2, dropdownContent)
    })//clickSize
        conditionField.click(function(){
        myFunction(3, dropdownContent)
    })//clickCondition
    var dropBoxOvercat = document.getElementsByClassName("overcategories-class")
    var dropBoxGender = document.getElementsByClassName("overcategory-gender")
    attachHoverDropdown(dropBoxOvercat, 'overcategory-gender')


    for (i=0;i<dropBoxGender.length;i++){
        dropBoxGender[i].onclick = function(e){
            var elementGender = e.target
            var $elementGender = $(elementGender)
            if ($elementGender.is('div')){
                $(".active-gender div div").removeClass("background-black");
                var genderChosen = $elementGender.attr('gender-for-cat')
                $elementGender.addClass('background-black').siblings().removeClass('background-black')
                }//if element is div
            else {
                $(".active-gender div div").removeClass("background-black");
                var genderChosen = $elementGender.parent().attr('gender-for-cat')
                $elementGender.parent().addClass('background-black').siblings().removeClass('background-black')
            }//else
        genderField.val(genderChosen)
        undercategoryField.val('')
        sizeField.val('')
        inputUnder.val('')
        inputSize.val('')
        dropBoxSize.hide()
        var obj_id_gender = $elementGender.attr('value')
        inputGender.val(obj_id_gender)
        var categoryDrop = $('.categories')
        var categoryDropActive = $('.active-undercategory')
        $.ajax({
            url: actionEndpoint,
            data: {obj_id_gender: obj_id_gender},
            success: function(data){
                categoryDrop.html('')
                categoryDropActive.html('')
                $.each(data.categories,
                    function(index, category){
                        categoryDrop.append("<div class='col-12 categories-class' value='"+category.category+"'><p value='"+category.category+"'>"+category.category_language+"</p></div>")
                        categoryDropActive.append("<div class='"+category.category+" category-undercategory'></div>")
                        $.each(data.undercategories,
                            function(index, undercategory){
                                if(category.category == undercategory.undercategory_for){
                                    $("."+category.category).append("<div class='col-12 undercategories-class' id_for_fk ='"+undercategory.id+"' category-for-size='"+category.category+"' value ='"+undercategory.undercategory_language+"'><p class='mb-0' id_for_fk ='"+undercategory.id+"'value ='"+undercategory.undercategory_language+"'>"+undercategory.undercategory_language+"</p></div>")
                                }//if undercat==cat
                        })//eachUndercategories
                      })//eachCategories
                var categoriesClass = document.getElementsByClassName("categories-class")
                var categoryUnder = document.getElementsByClassName("category-undercategory")
                attachHoverDropdown(categoriesClass, 'category-undercategory')
                attachClickDropdown(categoryUnder, 'active-undercategory', undercategoryField, inputUnder, true, false)
            }//success
        })//ajax
        }//onclick
    }//for gender
}//if create or update


//FILTERS
    var h = screen.height; 
    document.getElementById("container-filters-update").style.height = (h - 220) + 'px'
    document.getElementById("slider_filters").style.height = h - 250 + 'px'
function displayRefreshingItems(container, display){
    if (display==true){
        if ($('.loadingPaginating').length==0){
            container.append('<div class="col-12 mt-2 mb-2 loadingPaginating text-center p-0"><i class="fas fa-spin fa-4x fa-spinner"></i></div>')
        }//if one icon only
    }//if display
    else{
        container.find('.loadingPaginating').remove()
    }//if not display
}//displayRefreshing
function setCheckboxRadio(klass){
    $("input:checkbox." + klass).on('click', function() {
  
  var $box = $(this);
  if ($box.is(":checked")) {
    
    var group = "input:checkbox[name='" + $box.attr("name") + "']";
    
    $(group).prop("checked", false);
    $box.prop("checked", true);
  } else {
    $box.prop("checked", false);
  }
})//click
}//setCheckboxRadio
 var hideFiltersBtn = $('#btn-filters')
 var hideShowText = $('#text-for-hide-show')
 var containerFilter = $('#container-filters-update')
 var filterBox = $('#slider_filters')
 hideFiltersBtn.click(
    function(e){
        if (hideFiltersBtn.attr('hide') == 'true') {
           filterBox.addClass('hide')
           hideFiltersBtn.attr('hide', 'false')
           containerFilter.removeClass('col-9')
           containerFilter.addClass('col-12')
           //card
           $('.card-img-top-hidden').removeClass('card-img-top-hidden').addClass('card-img-top')
           $('.card-body-hidden').removeClass('card-body-hidden').addClass('card-body')
           $('.like-center-hidden').removeClass('like-center-hidden').addClass('like-center')
           //card
           hideShowText.html('Show Filters')
        }//if we hide filters
        else if (hideFiltersBtn.attr('hide') == 'false') {
           filterBox.removeClass('hide')
           hideFiltersBtn.attr('hide', 'true')
           containerFilter.removeClass('col-12')
           containerFilter.addClass('col-9')
           //card
           $('.card-img-top').removeClass('card-img-top').addClass('card-img-top-hidden')
           $('.card-body').removeClass('card-body').addClass('card-body-hidden')
           $('.like-center').removeClass('like-center').addClass('like-center-hidden')
           //card
           hideShowText.html('Hide Filters')
        }//if we show filters
 })//click on hide/show filter

 //filters hide by default for mobile
 // var currentPath = window.location.href
 //    if ((currentPath.indexOf("products/givemetheloot") != -1) && ($(window).width() < 768)){
 //        $(hideFiltersBtn.attr('hide') = 'true');
 //    } else {
 //        $(hideFiltersBtn.attr('hide') = 'false');      
 //    }

 var checkboxes = $('.input-for-filters')
 var formCheckboxes = $('#form_checkboxes')
 var formCheckboxesEndpoint = formCheckboxes.attr('action')
 var containerWithItems = $('#container-filters-update')
 setCheckboxRadio('radioOvercategorie')
 setCheckboxRadio('radioGender')
 var categoriesCheckboxesInitial = $('.undercategory-for-check').find("[name='undercategory']:checked")
 var sizesCheckboxInitial = $('.size_for_initial').find("[name='size']:checked")
 $.each(sizesCheckboxInitial,
    function(idx,data){
        $target = $(data)
    if ($target.parent().parent().parent().find("[name='size']:checked").length == $target.parent().parent().parent().find("[name='size']").length){
        $target.parent().parent().parent().find("[name='category-size']").prop('checked',true)
                }//if all checked
 })//each checked checkbox 
 $.each(categoriesCheckboxesInitial,
    function(idx,data){
        $target = $(data)
    if ($target.parent().parent().parent().find("[name='undercategory']:checked").length == $target.parent().parent().parent().find("[name='undercategory']").length){
        $target.parent().parent().parent().find("[name='category']").prop('checked',true)
                }//if all checked
 })//each checked checkbox 

 if ($('.undercategory-for-check').find("[name='undercategory']:checked").length == $('.undercategory-for-check').find("[name='undercategory']").length){
        $('.undercategory-for-check').find("[name='category']").prop('checked',true)
    }//if all checked
// checkboxes.click(
//     function(e){
//         console.log(e.target)
//     })//click on disbled checkboxes
$('.undercategory_for_disabled_checkbox_lable').click(
    function(e){
        $target = $(e.target)
        if ($target.parent().find('input').prop('disabled') == true){
            $target.parent().parent().find('input').prop('disabled', false)
        }//if click on disabled checkbox
})//click on lables in undercat checkboxes
$('.size_for_disabled_checkbox_lable').click(
    function(e){
        $target = $(e.target)
        if ($target.parent().find('input').prop('disabled') == true){
            $target.parent().parent().find('input').prop('disabled', false)
        }//if click on disabled checkbox
})//click on lables in undercat checkboxes

containerWithItems.scroll(
    function(e){
        if(e.target.offsetHeight + e.target.scrollTop == e.target.scrollHeight)
            {   
            var pageNum = 0
            if (window.location.href.indexOf('?page=') == -1){
                pageNum = 2
            }
            else {
                var arr_link = window.location.href.split('/')
                var numFromLink = parseInt(arr_link.slice(-1)[0].split('?').slice(-1)[0].split('=').slice(-1)[0])
                pageNum = numFromLink + 1
            }
            var formCheckboxesData = formCheckboxes.serialize()
            formCheckboxesData = formCheckboxesData + '&page=' + pageNum
                $.ajax({
                    url: formCheckboxesEndpoint,
                    method: 'get',
                    data: formCheckboxesData,
                    success: function(data){
                        if (data.count_pages == true){
                            // displayRefreshingItems($('#filtersTestRefresh'),true)
                            // setTimeout(function(){
                            // displayRefreshingItems($('#filtersTestRefresh'),false)
                            $('#container-filters-update').append(data.html)
                            $('#items_count').html(data.count_items)

                            var productForm=$(".form-product-ajax-wishlist")
                            productForm.unbind()
                            bind_ajax_heart(productForm)
                            data.link = data.link + '?page='+pageNum
                            window.history.replaceState( {} , 'title', data.link)
                            // },2000)
                            
                        }//if continue
                                }//success
                    })//ajax form submit
        }//if end of scroll
    })//scroll

$('#brand-select').searchableOptionList({
        texts: {
            searchplaceholder: 'Please, select a brand'
        },
        showSelectAll: false,
        maxHeight:'250px',
        events: {            
        onChange:function() {
        containerWithItems.scrollTop(0)
        var formCheckboxesData = formCheckboxes.serialize()
        $.ajax({
            url: formCheckboxesEndpoint,
            method: 'get',
            data: formCheckboxesData,
            success: function(data){
               $('#container-filters-update').html(data.html)
               $('#items_count').html(data.count_items)
                var productForm=$(".form-product-ajax-wishlist")
                bind_ajax_heart(productForm)
                window.history.replaceState( {} , 'title', data.link)
                        }//success
        })//ajax form submit
            },
            
            // more events as you need
        }
    })

 checkboxes.change(
    function (e) {
        containerWithItems.scrollTop(0)      
        var $target = $(e.target)
        console.log($target)
        if ($target[0].name == 'overcategory'){
            $('#title_gender').hide()
            $('#gender-filter-box > div > div').hide()
            $('#gender-filter-box > div > div > div > input').prop('checked', false)
            //gender
            $('#title_category').hide()
            $('#category-filter-box > div > div').hide()
            $('#category-filter-box > div > div > div > input').prop('checked', false)
            //category
            $('#title_size').hide()
            $('#size-filter-box > div > div').hide()
            $('#size-filter-box > div > div > div > input').prop('checked', false)
            //size
            $('.collapse div1').collapse('hide')
            $('#category-filter-box > div > div > div > div > div > input').prop('checked', false)
            $('#size-filter-box > div > div > div > div > div > input').prop('checked', false)
            if ($target.prop('checked') == true){
                $('#title_gender').show()
                $('#'+$target.attr('data_for_gender')+'-gender-checkbox').show()
            }//if true, zeigen
        }//if overcategory
        if ($target[0].name == 'gender'){
            $('#title_category').hide()
            $('#category-filter-box > div > div').hide()
            $('#category-filter-box > div > div > div > input').prop('checked', false)
            //category
            $('#title_size').hide()
            $('#size-filter-box > div > div').hide()
            $('#size-filter-box > div > div > div > input').prop('checked', false)
            //size
            $('.collapse div1').collapse('hide')
            $('#category-filter-box > div > div > div > div > div > input').prop('checked', false)
            $('#size-filter-box > div > div > div > div > div > input').prop('checked', false)
            if ($target.prop('checked') == true){
                $('#title_category').show()
                $('#'+$target.attr('data_for_category')+'-category-checkbox').show()
                $('#title_size').show()
                $('#'+$target.attr('data_for_category')+'-size-checkbox').show()
            }//if true, zeigen
        }
        if ($target[0].name == 'category'){
            if ($target.prop('checked') == true){
                $('#'+$target.attr('data_for_category')+'-size-checkbox > div').hide()
                $('#'+$target.attr('data_for_size')).attr('active', 'true')
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='true']").show()
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('checked',false)
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('disabled',false)
                $target.parent().find("[name='undercategory']").prop('checked', true)
                $target.parent().find("[name='undercategory']").prop('disabled', true)
            }//if all checked
            else{
                $('#'+$target.attr('data_for_category')+'-size-checkbox > div').hide()
                $('#'+$target.attr('data_for_size')).attr('active', 'false')
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='true']").show()
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('checked',false)
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('disabled',false)
                $target.parent().find("[name='undercategory']").prop('checked', false)
                $target.parent().find("[name='undercategory']").prop('disabled', false)
                if ($('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='true']").length == 0){
                   $('#'+$target.attr('data_for_category')+'-size-checkbox > div').show()
                }//if no category checked
            }//if not checked
        }//if category
        if ($target[0].name == 'undercategory'){
            if ($target.prop('checked') == false){
                $('#'+$target.attr('data_for_category')+'-size-checkbox > div').hide()
                $('#'+$target.attr('data_for_size')).attr('active', 'false')
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='true']").show()
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('checked',false)
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('disabled',false)
                $target.parent().parent().parent().find("[name='category']").prop('checked',false)
                if ($('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='true']").length == 0){
                   $('#'+$target.attr('data_for_category')+'-size-checkbox > div').show()
                }//if no category checked
            }//if not all checked in category 
            else if($target.prop('checked') == true){
                $('#'+$target.attr('data_for_category')+'-size-checkbox > div').hide()
                $('#'+$target.attr('data_for_size')).attr('active', 'true')
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='true']").show()
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('checked',false)
                $('#'+$target.attr('data_for_category')+'-size-checkbox').find("[active='false']").find('input').prop('disabled',false)
                if ($target.parent().parent().parent().find("[name='undercategory']:checked").length == $target.parent().parent().parent().find("[name='undercategory']").length){
                    $target.parent().parent().parent().find("[name='category']").prop('checked',true)
                    $target.parent().parent().find('input').prop('disabled', true)
                }//if all checked
            }//if checked
        }//if undercategory
        if ($target[0].name == 'size'){
            if ($target.prop('checked') == false){
                $target.parent().parent().parent().find("[name='category-size']").prop('checked',false)
            }//if not all checked in category 
            else if($target.prop('checked') == true){
                if ($target.parent().parent().parent().find("[name='size']:checked").length == $target.parent().parent().parent().find("[name='size']").length){
                    $target.parent().parent().parent().find("[name='category-size']").prop('checked',true)
                }//if all checked
            }//if checked
        }//if size
        if ($target[0].name == 'category-size'){
            if ($target.prop('checked') == true){
                $target.parent().find("[name='size']").prop('checked', true)
            }//if all checked
            else{
                $target.parent().find("[name='size']").prop('checked', false)
            }//if not checked
        }//if category
        var formCheckboxesData = formCheckboxes.serialize()
        $.ajax({
            url: formCheckboxesEndpoint,
            method: 'get',
            data: formCheckboxesData,
            success: function(data){
               $('#container-filters-update').html(data.html)
               $('#items_count').html(data.count_items)
                var productForm=$(".form-product-ajax-wishlist")
                bind_ajax_heart(productForm)
                window.history.replaceState( {} , 'title', data.link)
                        }//success
        })//ajax form submit
    })//change checkboxes







    // var toggleOvercategory = $('.toggle-overcategory')
    // toggleOvercategory.click(
    //     function(event){
    //         if (!($(event.target).hasClass('active'))){
    //             $('.toggle-gender').hide()
    //             $('.toggle-gender').children().removeClass('active')
    //         }//if alreadyActive
    //         var targetOvercategory = ($(event.target).children().attr('overcategory-chosen'))
    //         $('#choise-overcategory-'+targetOvercategory).show()
    //     })//on change toggle overcategory
    // var categoryField = $('#id_undercategory')
    // var selected_option_value_1=$("#id_undercategory option:selected").val();
    // console.log(selected_option_value_1)
    // categoryField.change(
    //   function(){
    //     var actionEndpoint = '/products/create/'
    //     var formData = $("#id_undercategory option:selected").val()
    //     console.log(formData)
    //     console.log(selected_option_value_1)
    //     $.ajax({
    //         url: actionEndpoint,
    //         data: {selected: formData},
    //         success: function(data){
    //         var id_size = $('#id_size').empty()
    //         $.each(data.sizes,
    //           function(index, value){
    //           $(id_size).append('<option value='+value.id+'>'+value.size+'</option>')
    //           console.log(value)
    //           })//each
            
              
    //         },//function
    //     })//ajax
    //     })//function(event)



// //filterboxeslogic
// var foot = $(".footwear")
// var out = $(".outerwear")
// var top = $(".tops")
// var bot = $(".bottoms")
// var acc = $(".accessories")
// // if(".customCheckboxfootwear:checked"){
// //         $('.outwear').prop('checked', false)
// //         $('.tops').prop('checked', false)
// //         $('.bottoms').prop('checked', false)
// //         $('.accessories').prop('checked', false)
// //         tops()
// //         outwear()
// //         bottoms()
// //         accessories()
// //         $(".outwear").prop("disabled", true)
// //         $(".tops").prop("disabled", true)
// //         $(".bottoms").prop("disabled", true)
// //         $(".accessories").prop("disabled", true)
// //     }

// // if(".customCheckboxoutwear:checked"){
// //         $('.footwear').prop('checked', false)
// //         $('.tops').prop('checked', false)
// //         $('.bottoms').prop('checked', false)
// //         $('.accessories').prop('checked', false)
// //         tops()
// //         footwear()
// //         bottoms()
// //         accessories()
// //         $(".footwear").prop("disabled", true)
// //         $(".tops").prop("disabled", true)
// //         $(".bottoms").prop("disabled", true)
// //         $(".accessories").prop("disabled", true)
// //     }


// // if(".customCheckboxtops:checked"){
// //         $('.footwear').prop('checked', false)
// //         $('.outwear').prop('checked', false)
// //         $('.bottoms').prop('checked', false)
// //         $('.accessories').prop('checked', false)
// //         outwear()
// //         footwear()
// //         bottoms()
// //         accessories()
// //         $(".footwear").prop("disabled", true)
// //         $(".outwear").prop("disabled", true)
// //         $(".bottoms").prop("disabled", true)
// //         $(".accessories").prop("disabled", true)
// //     }






// function footwear() {
//     if($(".footwear")[0].checked) {
//         $(".footwear-btn").css('display', 'block')
//     }
//     else{
//         $(".footwear-btn").css('display', 'none')
//         $('.customCheckboxfootwear').prop('checked', false)
//         $(".outerwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".accessories").prop("disabled", false)
//     }
// }
// function outerwear() {   
//     if(out[0].checked) {
//         $(".outerwear-btn").css('display', 'block')
//     }
//     else{
//         $(".outerwear-btn").css('display', 'none')
//         $('.customCheckboxouterwear').prop('checked', false)
//         $(".footwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".accessories").prop("disabled", false)
//     }
// }
// function tops() {   
//     if(top[0].checked) {
//         $(".tops-btn").css('display', 'block')
//     }
//     else{
//         $(".tops-btn").css('display', 'none')
//         $('.customCheckboxtops').prop('checked', false)
//         $(".outerwear").prop("disabled", false)
//         $(".footwear").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".accessories").prop("disabled", false)
//     }
// }
// function bottoms() {   
//     if(bot[0].checked) {
//         $(".bottoms-btn").css('display', 'block')
//     }
//     else{
//         $(".bottoms-btn").css('display', 'none')
//         $('.customCheckboxbottoms').prop('checked', false)
//         $(".outerwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".footwear").prop("disabled", false)
//         $(".accessories").prop("disabled", false)
//     }
// }
// function accessories() {   
//     if(acc[0].checked) {
//         $(".accessories-btn").css('display', 'block')
//     }
//     else{
//         $(".accessories-btn").css('display', 'none')
//         $('.customCheckboxaccessories').prop('checked', false)
//         $(".outerwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".footwear").prop("disabled", false)

//     }
// }
// //checkboxes
// $(".footwear").change(function(){

//   footwear()});
// $(".outerwear").change(function() {
//   outerwear()
// });
// $(".tops").change(function() {
//   tops()
// });
// $(".bottoms").change(function() {
//   bottoms()
// });
// $(".accessories").change(function () {
//   accessories()
// });
// //checkboxes
// // checkboxes - sizes
// $(".customCheckboxfootwear").change(
//   function(){
//     if(this.checked){
//         $('.outerwear').prop('checked', false)
//         $('.tops').prop('checked', false)
//         $('.bottoms').prop('checked', false)
//         $('.accessories').prop('checked', false)
//         tops()
//         outerwear()
//         bottoms()
//         accessories()
//         $(".outerwear").prop("disabled", true)
//         $(".tops").prop("disabled", true)
//         $(".bottoms").prop("disabled", true)
//         $(".accessories").prop("disabled", true)
//         }
//     if ($('.customCheckboxfootwear:checked').length==0){
//         $(".outerwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".accessories").prop("disabled", false)

//     }
//   })//change
// $(".customCheckboxouterwear").change(
//   function(){

//     if(this.checked){
//         $('.footwear').prop('checked', false)
//         $('.tops').prop('checked', false)
//         $('.bottoms').prop('checked', false)
//         $('.accessories').prop('checked', false)
//         footwear()
//         tops()
//         bottoms()
//         accessories()
//         $(".footwear").prop("disabled", true)
//         $(".tops").prop("disabled", true)
//         $(".bottoms").prop("disabled", true)
//         $(".accessories").prop("disabled", true)
//         }
//     if ($('.customCheckboxouterwear:checked').length==0){
//         $(".footwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".accessories").prop("disabled", false)

//     }
//   })//change
// $(".customCheckboxtops").change(
//   function(){
//     if(this.checked){
//         $('.outerwear').prop('checked', false)
//         $('.footwear').prop('checked', false)
//         $('.bottoms').prop('checked', false)
//         $('.accessories').prop('checked', false)
//         footwear()
//         outerwear()
//         bottoms()
//         accessories()
//         $(".outerwear").prop("disabled", true)
//         $(".footwear").prop("disabled", true)
//         $(".bottoms").prop("disabled", true)
//         $(".accessories").prop("disabled", true)
//         }
//     if ($('.customCheckboxtops:checked').length==0){
//         $(".outerwear").prop("disabled", false)
//         $(".footwear").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".accessories").prop("disabled", false)

//     }
//   })//change
// $(".customCheckboxbottoms").change(
//   function(){
//     if(this.checked){
//         $('.outerwear').prop('checked', false)
//         $('.tops').prop('checked', false)
//         $('.footwear').prop('checked', false)
//         $('.accessories').prop('checked', false)
//         footwear()
//         tops()
//         outerwear()
//         accessories()
//         $(".outerwear").prop("disabled", true)
//         $(".tops").prop("disabled", true)
//         $(".footwear").prop("disabled", true)
//         $(".accessories").prop("disabled", true)
//         }
//     if ($('.customCheckboxbottoms:checked').length==0){
//         $(".outerwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".footwear").prop("disabled", false)
//         $(".accessories").prop("disabled", false)

//     }
//   })//change
// $(".customCheckboxaccessories").change(
//   function(){
//     if(this.checked){
//         $('.outerwear').prop('checked', false)
//         $('.tops').prop('checked', false)
//         $('.bottoms').prop('checked', false)
//         $('.footwear').prop('checked', false)
//         footwear()
//         tops()
//         outerwear()
//         bottoms()
//         $(".outerwear").prop("disabled", true)
//         $(".tops").prop("disabled", true)
//         $(".bottoms").prop("disabled", true)
//         $(".footwear").prop("disabled", true)
//         }
//     if ($('.customCheckboxaccessories:checked').length==0){
//         $(".outerwear").prop("disabled", false)
//         $(".tops").prop("disabled", false)
//         $(".bottoms").prop("disabled", false)
//         $(".footwear").prop("disabled", false)

//     }
//   })//change
// //filterboxeslogic


// //slider filter box
// $("#slider").slideReveal({
//   trigger: $("#trigger"),
//   push: false,
//   overlay: true,
//   overlayColor:'rgba(0,0,0,0.5)',
//   width:'500px',
// });
// //slider filter box

// $("#slider_2").slideReveal({
//   trigger: $("#trigger_2"),
//   push: false,
//   overlay: true,
//   overlayColor:'rgba(0,0,0,0.5)',
//   width:'500px',
// });



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
