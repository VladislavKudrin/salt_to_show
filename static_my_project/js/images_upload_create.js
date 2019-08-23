$(document).ready(
  function(){


//brand autofill 
var formSubmitBrand = $('#example-form-1')
var actionBrand = formSubmitBrand.attr("action_url_create")
$.ajax({
    url: actionBrand,
    method:'GET',
    success: function(data){
    var availableTags = data.brand 
    $( ".brandautofill" ).autocomplete({
      source: availableTags
    });
    },//success
    error: function(errorData){
    // $.alert({
    // title: 'OOps!',
    // content: 'Simple alert!',
    // theme: "modern"
    // });
    console.log('some error');
    }//error
    })//ajax










//create
var currentPath = window.location.href
if (currentPath.indexOf("create") != -1){
    var languageOption = $('#language').val()
    var galleryUpdate = $('#gallery')
    var formSubmit = $('#example-form-1')
    var action = formSubmit.attr("action_url_create")
    var action_order = formSubmit.attr("action_url_create_order")
    var buttonImageUpload = $('.image-upload-button')
    var imagesUploadLimit = $('#images-upload-limit')
    buttonImageUpload.hide()
    if (languageOption=='RU'){
        buttonImageUpload.parent().prepend('<label for="image_custom" class="btn btn-block hover-button button-white large-button prod-create-browse">Выбрать</label>')
    }//if rus
    else {
        buttonImageUpload.parent().prepend('<label for="image_custom" class="btn btn-block hover-button button-white large-button prod-create-browse">Browse</label>')
    }//if not rus

     
    var uploadUrl = formSubmit.attr('image_upload_url')
    var deleteImageUrl = formSubmit.attr('image_delete_url')
    var rotateImageUrl = formSubmit.attr('image_rotate_url')
    var imageContainer = $('.temp-images')
    var imageContainerParent = $('.custom-upload-file-ajax-temp') 
    var imageContainerCol = $('#wow') 
    var formId = $('#form_id')
    var imagesTemplate = $.templates("#images-upload-update")
    var i = 0
    $(window).bind('beforeunload',function(){
     $.ajax({
        url: deleteImageUrl,
        method:'POST',
        data: {'data':'delete_on_reload', 'form_id':formId.val()},
        success:function(data){
                },//success
        error:function(errorData){

                }//error
     })//ajaxbeforereload
    })//beforereload
function deleteRotateItem(item){
    item.on("click", 
    function(event){
        var $item = $(this),
        $target = $(event.target);
        if ($target.is("a.ui-icon-trash")) {
            event.preventDefault()
            var deleteData = $item.find("[name='qq-file-id']").val()
            $.ajax({
                url: deleteImageUrl,
                method:'POST',
                data: {'data':deleteData, 'form_id':formId.val()},
                success:function(data){
                   $item.remove()
                   if (data.count<=8){
                    buttonImageUpload.attr('disabled', false)
                   } //enabelbtniflessthan8
                },//success
                error:function(errorData){

                }//error
            })//ajax for delete
    }//if trash
    if ($target.is("i.rotateItem")) {
            event.preventDefault()
            var rotatedTimes = $item.find("[name='rotateTimes']").val()
            rotatedTimes = parseInt(rotatedTimes) + 1
            $item.find("[name='rotateTimes']").val(rotatedTimes)
            var grad = 90 * rotatedTimes
            $item.children('img').css('transform', 'rotate('+grad+'deg)')
            // var deleteData = $item.find("[name='qq-file-id']").val()
            // $.ajax({
            //     url: rotateImageUrl,
            //     method:'POST',
            //     data: {'data':deleteData, 'form_id':formId.val()},
            //     success:function(data){
            //         
            //         console.log('1')
            //        // $item.remove()
            //        // if (data.count<=8){
            //        //  buttonImageUpload.attr('disabled', false)
            //        // } //enabelbtniflessthan8
            //     },//success
            //     error:function(errorData){

            //     }//error
            // })//ajax for rotate
    }//if rotate
    })//onclicktrash
}//deleteItem
    function displayUploading(files, doUpload){
        if(doUpload){
        $.each(files, 
            function(index, value){
            buttonImageUpload.attr('disabled', true)
            imageContainer.append("<i class='ml-3 mb-3 fa-2x fas fa-spin fa-spinner'></i>")
            })//each-displayfilesupload
        }//doUpload
        else{
            buttonImageUpload.attr('disabled', false)
            $('.fa-spinner').hide()
        }//ifnotdoUpload
    }//displayUploading
    buttonImageUpload.change(
        function() {
            $('#id_image').removeClass('is-invalid')
            $('p.image').remove('.invalid-feedback')

            var data = new FormData()
            var imagesArr = []
            var myFiles = $(this)[0].files;
            if (myFiles.length>imagesUploadLimit.val()){
                if ($('.image').length==0){
                    if(languageOption=='RU'){
                        $('#id_image').addClass('is-invalid')
                        $('#id_image').after('<p class="invalid-feedback image"><strong>Слишком много фотографий. Максимальное колличество - '+ imagesUploadLimit.val() +'</strong></p>')}//if more than 8 one time
                    }//if ru
                    else{
                        $('#id_image').addClass('is-invalid')
                        $('#id_image').after('<p class="invalid-feedback image"><strong>Too many images. Should be less than '+ imagesUploadLimit.val() + '</strong></p>')//if more than 8 one time
                    }//if not ru
                return console.log('hellow')
            }//ifmorethan8
            displayUploading(myFiles, true)
            $.each(myFiles, 
            function(index, value){
                data.append('image', value)
            })//each-buttonImageUpload
            data.append('form_id', formId.val())
            data.append('qq-file-id', i)
            console.log(i)
        $.ajax({
            url: uploadUrl,
            method:'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success:function(data){
                displayUploading(myFiles, false)
                $.each(data.image,
                  function(index, value){
                  imageContainer.append('<li class="ui-widget-content ui-corner-tr"><img src="'+ value.image_url + '" width="96" height="72"><input type="hidden" id="qq-file-id" name="qq-file-id" value='+i+'><a class="ui-icon ui-icon-trash trash-custom-ecommerce mt-1" href="#"></a><a class="mt-1 mr-5 ui-icon-rotate rotateItem"><i class="rotateItem fas fa-xs fa-sync-alt"></i><input type="hidden" name="rotateTimes" value="0"></a></li>')
                  i++
                  })//eachfoto

            var elementList = $("ul.gallery > li")
            elementList.unbind()
            deleteRotateItem(elementList)
            if (data.count>8){
                buttonImageUpload.attr('disabled', true)
            }//if more than 8 already uploaded
            },//success ajax-image-uploader
            error:function(errorData){
            }//error ajax-image-uploader
            })//ajax-image-uploader
    })//change-buttonImageUpload


    function displayCreating(submitBtn, defaultText, doSubmit){
        console.log('')
      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.attr("disabled", true)
        submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Authenticity check...")
        if(languageOption=='RU'){
            submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Проверка на оригинальность...")
        }//if rus
        else if (languageOption=='UA'){
            submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Перевірка на оригінальність...")
        }//if rus
        else{
            submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Authenticity check...")
        }//if not rus
        } //if dosubmit 
      else {
        submitBtn.removeClass("disabled")
        submitBtn.attr("disabled", false)
        submitBtn.html(defaultText)
      }//elsedosubmit
    }        
    formSubmit.submit(
    function(event){
    event.preventDefault()
    var createFormSubmitBtn = formSubmit.find("[type='submit']")
    var createFormSubmitBtnTxt = createFormSubmitBtn.text()
    var formData = formSubmit.serialize()
    var elements = $('#example-form-1 ul li')
    var keyArray = []
    var rotateArray = []
    displayCreating(createFormSubmitBtn, "",true)
    $.each(elements,
    function(index, value){
        var attr = $(value).find("[name='qq-file-id']").val()
        var rotatedImageTimes = $(value).find("[name='rotateTimes']").val()
        keyArray.push(attr)  
        rotateArray.push(rotatedImageTimes)
    })//eacharray
    console.log(keyArray)
    console.log(rotateArray)
    $.ajax({
    url: action,
    method:'POST',
    data: formData,
    success: function(data){
        $('.is-invalid').removeClass('is-invalid')
        $('p').remove('.invalid-feedback')
        if(data['error']) {
        $.each(data['error'],
            function(index, value){
                displayCreating(createFormSubmitBtn, "Create",false)
                if ($('.'+index).length==0){
                    $('#id_' + index).addClass('is-invalid')
                    $('#id_' + index).after("<p class='invalid-feedback "+index+"'><strong>"+value+"</strong></p>")  
                }//if  
            })//each
            }//if there are errors
        else {
          $.ajax({
            url: action_order,
            method:'POST',
            data: {'data[]':keyArray, 'slug':data.slug, 'rotate[]':rotateArray},
            success:function(data){
              console.log('successsssss')
                },//success second ajax
            error:function(errorData){
                }//error second ajax
            })//ajax in ajax
            window.location.href=data.url
                }//else
            },//success
    error:function(errorData){
        console.log('error')
        console.log(errorData)
        }//error_1
    })//ajax
    })//submit
}


//update 

//brand and image sort

//update
var currentPath = window.location.href

if (currentPath.indexOf("update") != -1){
    function rotateItem(item){
    item.on("click", 
    function(event){
        var $item = $(this),
        $target = $(event.target);
        if ($target.is("i.rotateItem")) {
            event.preventDefault()
            var rotatedTimes = $item.find("[name='rotateTimes']").val()
            rotatedTimes = parseInt(rotatedTimes) + 1
            $item.find("[name='rotateTimes']").val(rotatedTimes)
            var grad = 90 * rotatedTimes
            $item.children('img').css('transform', 'rotate('+grad+'deg)')
    }//if rotate
    })//onclicktrash
}//deleteItem
    var formSubmit = $('#example-form-1')
    var elementList = $("ul.gallery > li")
    rotateItem(elementList)
    formSubmit.submit(
    function(event){
    var formCreate = $('#customSort')
    var galleryUpdate = $('#gallery')
    var action = formSubmit.attr("action_url")
    var elements = $('#example-form-1 ul li')
    var keyArray = []
    $.each(elements,
    function(index, value){
        var val = ($(value)).find("[name = 'image-id']")
        keyArray.push(val.val())
    })//each
    $.ajax({
    url: action,
    method:'POST',
    data: {'data[]':keyArray},
    success: function(data){
    },//success
    error: function(errorData){
    // $.alert({
    // title: 'OOps!',
    // content: 'Simple alert!',
    // theme: "modern"
    // });
    console.log('some error');
    }//error
    })//ajax
   })//submit_update_create
}//if_current_path_update
 
    // There's the gallery and the trash
    $("#customSort").sortable();
    $("#customSort").disableSelection();












})//document ready