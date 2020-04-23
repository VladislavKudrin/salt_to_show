$(document).ready(
  function(){









// Spinner function
    function displayCreating(submitBtn, authenticityCheckBtn, defaultText, doSubmit, currentPath){
      if (doSubmit){
            if (currentPath.indexOf("create") != -1){ // Case 1 : product create
                submitBtn.addClass("disabled")
                submitBtn.attr("disabled", true)
                submitBtn.html("<i class='fas fa-spin fa-spinner'></i> " + authenticityCheckBtn)
            }
            else { // Case 2: product upload
                submitBtn.addClass("disabled")
                submitBtn.attr("disabled", true)
                submitBtn.html("<i class='fas fa-spin fa-spinner'></i> ")
            }
        } //if dosubmit 
      else {
        submitBtn.removeClass("disabled")
        submitBtn.attr("disabled", false)
        submitBtn.html(defaultText)
      }//else dosubmit
    }  




//Product Create
    var authenticityCheckBtn = $('#btn_authenticity_check').html()
    var currentPath = window.location.href
    var ImgDict = new Object()
    var fileCollection = new Array();
    var image_iteration_index = 0
    if (currentPath.indexOf("create") != -1){
        var languageOption = $('#language').val()
        var galleryUpdate = $('#gallery')
        var formSubmit = $('#example-form-1')
        var action = formSubmit.attr("action_url_create")
        var action_order = formSubmit.attr("action_url_create_order")
        var buttonImageUpload = $('.image-upload-button')
        var imagesUploadLimit = $('#images-upload-limit')
        var errorTooManyImages = $('#error_too_many_images').html()
        var uploadUrl = formSubmit.attr('image_upload_url')
        var deleteImageUrl = formSubmit.attr('image_delete_url')
        var rotateImageUrl = formSubmit.attr('image_rotate_url')
        var imageContainer = $('.temp-images')
        var imageContainerParent = $('.custom-upload-file-ajax-temp') 
        var imageContainerCol = $('#wow') 
        var formId = $('#form_id')
        var imagesTemplate = $.templates("#images-upload-update")
        var i = 0
    // brand autofill for product create
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
    //brand autofill
    function deleteRotateItem(item){
        item.on("click", 
        function(event){
            var $item = $(this),
            $target = $(event.target);
        if ($target.is("a.ui-icon-trash")) {
            event.preventDefault()
            var deleteData = parseInt($item.find("[name='qq-file-id']").val())
            if (fileCollection.length > 0){
                $item.remove()
            }//if filecollection exists
        }//if trash
        if ($target.is("svg.rotateItem")) {
                event.preventDefault()
                var rotatedTimes = $item.find("[name='rotateTimes']").val()
                rotatedTimes = parseInt(rotatedTimes) + 1
                $item.find("[name='rotateTimes']").val(rotatedTimes)
                var grad = 90 * rotatedTimes
                $item.children('img').css('transform', 'rotate('+grad+'deg)')
        }//if rotate
        })//onclicktrash
    }//deleteItem



        function displayUploading(doUpload, where_to_put=null, how_many_files=null){
            var imagesAlreadyUploadedCount = $('ul#customSort li').length
            if(doUpload){
                for (var i = 0; i < how_many_files; i++){
                    id = i
                    where_to_put.append("<i id='spinner_upload_"+ id +"' class='ml-3 mb-3 fa-2x fas fa-spin fa-spinner' style='font-size: 1.5em;'></i>")
                };
            }//doUpload
            else{

                $('#spinner_upload_'+where_to_put).remove();
            }//ifnotdoUpload
        }//displayUploading





        //upload images in browser cache
        buttonImageUpload.change(
            function(evt) {
                $('#id_image').removeClass('is-invalid')
                $('p.image').remove('.invalid-feedback')
                $("#customSort").sortable( "option", "disabled", true );
                var imagesAlreadyUploadedCount = $('ul#customSort li').length
                var files = evt.target.files;
                if (files.length > imagesUploadLimit.val() | files.length + imagesAlreadyUploadedCount > imagesUploadLimit.val()){
                    if ($('.image').length==0){
                        $('#id_image').addClass('is-invalid')
                        $('#id_image').after('<p style="position:relative!important" class="invalid-feedback image"><strong>' + errorTooManyImages +' '+ imagesUploadLimit.val() + '</strong></p>')//if more than 8 one time
                        $("#customSort").sortable( "option", "disabled", false );
                    return console.log('hellow')
                    }//if nothing under images errors
                }//ifmorethan8
                buttonImageUpload.attr('disabled', true);
                displayUploading(true, imageContainer, files.length);
                $.each(files, function(i, file){
                    var reader = new FileReader;
                    reader.readAsDataURL(file);
                    reader.onload = (function(theFile){
                        var li = document.createElement('li');
                        fileCollection.push(files[i])
                        li.setAttribute('class', 'ui-widget-content ui-corner-tr');
                        li.innerHTML = ['<img src="',
                        theFile.target.result, 
                        '"style="object-fit:contain;height:100px;padding: 0.2em;align-items:center;"><input type="hidden" id="qq-file-id" name="qq-file-id" value=',
                        image_iteration_index,
                        '><a class="ui-icon ui-icon-trash trash-custom-ecommerce" href="#"></a><a class="ui-icon-rotate rotateItem" style="cursor: pointer;"><i class="rotateItem fas fa-xs fa-sync-alt" style="padding: 0.2em;width: 2em;height: 1.3em;"></i><input type="hidden" name="rotateTimes" value="0"></a>'].join('');
                        document.getElementById('customSort').insertBefore(li, null);
                        displayUploading(false, i);
                        image_iteration_index+=1
                        var elementList = $("ul.gallery > li")
                        elementList.unbind()
                        deleteRotateItem(elementList)
                    })//onload
                })//each
                
                buttonImageUpload.attr('disabled', false);
                 $("#customSort").sortable( "option", "disabled", false );
            })//change-buttonImageUpload            
        

        formSubmit.submit(
        function(event){
        event.preventDefault()
        var keyArray = []
        var rotateArray = []
        var elements = $('#example-form-1 ul li')      
        $.each(elements,
        function(index, value){
            var attr = $(value).find("[name='qq-file-id']").val()
            var rotatedImageTimes = $(value).find("[name='rotateTimes']").val()
            rotateArray.push(rotatedImageTimes)
            keyArray.push(attr)  
        })//eacharray
        var formData = new FormData(this);
        formData.delete('image')
        $.each(keyArray, 
            function(index, value){
                formData.append('image', fileCollection[value])      
            })//each files
        var createFormSubmitBtn = formSubmit.find("[type='submit']")
        var createFormSubmitBtnTxt = createFormSubmitBtn.text()
        displayCreating(createFormSubmitBtn, authenticityCheckBtn, "",true, currentPath)
        $.ajax({
            url: action,
            method: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data){
                $('.is-invalid').removeClass('is-invalid')
                $('p').remove('.invalid-feedback')
                if(data['error']) {
                    $.each(data['error'],
                        function(index, value){
                            var btnText = createFormSubmitBtnTxt
                            displayCreating(createFormSubmitBtn, authenticityCheckBtn, btnText,false, currentPath)
                            if ($('.'+index).length==0){
                                $('#id_' + index).addClass('is-invalid')
                                $('#id_' + index).after("<p class='m-0 invalid-feedback "+index+"'><strong>"+value+"</strong></p>")  
                            }//if  
                        })//each
                        }//if there are errors
                else {
                    window.location.href=data.url
                }
            },
            error: function(errorData){
                console.log('error')
            }
        })//ajax
        })//submit
    }







//Product Update
    var currentPath = window.location.href
    if (currentPath.indexOf("update") != -1){
        var languageOption = $('#language_pref').val()
        function rotateItem(item){
        item.on("click", 
        function(event){
            var $item = $(this),
            $target = $(event.target);
            if ($target.is("svg.rotateItem")) {
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
        var createFormSubmitBtn = formSubmit.find("[type='submit']")
        var createFormSubmitBtnTxt = createFormSubmitBtn.text()
        formSubmit.submit(
        function(event){
        event.preventDefault()
        var formData = new FormData(this);
        var formCreate = $('#customSort')
        var galleryUpdate = $('#gallery')
        var rotateArray = []
        // Activate spinner
        displayCreating(createFormSubmitBtn, authenticityCheckBtn, "",true, currentPath)
        var action = formSubmit.attr("action_url")
        var action_update = formSubmit.attr("action_url_update")
        var elements = $('#example-form-1 ul li')
        var keyArray = []
        $.each(elements,
        function(index, value){
            var val = ($(value)).find("[name = 'image-id']")
            formData.append('keyArray', val.val())
        })//each
        $.ajax({
        url: action_update,
        method:'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data){
            $('.is-invalid').removeClass('is-invalid')
            $('p').remove('.invalid-feedback')
            if(data['error']) {
            $.each(data['error'],
                    function(index, value){
                        var btnText = createFormSubmitBtnTxt
                        if(languageOption=='RU'){
                        btnText = 'Сохранить'
                        }//if rus
                        else if (languageOption=='UK'){
                        btnText = 'Зберегти'
                        }//if rus
                        else{
                        btnText = 'Save'
                        }//if not rus
                    displayCreating(createFormSubmitBtn, btnText,false, currentPath)
                    if ($('.'+index).length==0){
                        $('#id_' + index).addClass('is-invalid')
                        $('#id_' + index).after("<p class='m-0 invalid-feedback "+index+"'><strong>"+value+"</strong></p>")  
                    }//if  
                })//each
                }//if there are errors
            else {
                var url = data.url
                window.location.href=url
                    }//else
                },//success
        error:function(errorData){
            console.log('error')
            console.log(errorData)
            }//error_1
        })//ajax
       })//submit_update_create
    }//if_current_path_update
     
        // There's the gallery and the trash
        $("#customSort").sortable();
        $("#customSort").disableSelection();









})//document ready