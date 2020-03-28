$(document).ready(
  function(){




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
    if (currentPath.indexOf("create") != -1){
        var languageOption = $('#language').val()
        var galleryUpdate = $('#gallery')
        var formSubmit = $('#example-form-1')
        var action = formSubmit.attr("action_url_create")
        var action_order = formSubmit.attr("action_url_create_order")
        // console.log(action_order)
        var buttonImageUpload = $('.image-upload-button')
        var imagesUploadLimit = $('#images-upload-limit')
        // buttonImageUpload.hide()
        // if (languageOption=='RU'){
        //     buttonImageUpload.parent().prepend('<label for="image_custom" class="btn btn-block hover-button button-white large-button prod-create-browse">Выбрать</label>')
        // }//if rus
        // else if (languageOption=='UA'){
        //     buttonImageUpload.parent().prepend('<label for="image_custom" class="btn btn-block hover-button button-white large-button prod-create-browse">Вибрати</label>')
        // }//if rus
        // else {
        //     buttonImageUpload.parent().prepend('<label for="image_custom" class="btn btn-block hover-button button-white large-button prod-create-browse">Browse</label>')
        // }//if not rus
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

    function deleteRotateItem(item){
        item.on("click", 
        function(event){
            console.log('rotate')
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
        if ($target.is("svg.rotateItem")) {
            // console.log('here')
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



        function displayUploading(doUpload, where_to_put=null, how_many_files=null){
            console.log(doUpload)
            if(doUpload){
                for (var i = 0; i < how_many_files; i++){
                    where_to_put.append("<i id='spinner_upload_"+ i +"' class='ml-3 mb-3 fa-2x fas fa-spin fa-spinner' style='font-size: 1.5em;'></i>")
                };
            }//doUpload
            else{
                console.log('#spinner_upload_'+where_to_put)
                $('#spinner_upload_'+where_to_put).remove();
            }//ifnotdoUpload
        }//displayUploading





        //upload images in browser cache
        buttonImageUpload.change(
            function(evt) {
                $('#id_image').removeClass('is-invalid')
                $('p.image').remove('.invalid-feedback')
                var files = $(this)[0].files;
                if (files.length > imagesUploadLimit.val()){
                    if ($('.image').length==0){
                        $('#id_image').addClass('is-invalid')
                        $('#id_image').after('<p style="position:relative!important" class="invalid-feedback image"><strong>' + errorTooManyImages +' '+ imagesUploadLimit.val() + '</strong></p>')//if more than 8 one time
                    return console.log('hellow')
                    }//if nothing under images errors
                }//ifmorethan8
                buttonImageUpload.attr('disabled', true);
                displayUploading(true, imageContainer, files.length);
                for (var i = 0, f; f = files[i]; i++) {
                    var new_i = 0
                    var reader = new FileReader();
                    reader.onload = (function(theFile){
                        return function(e){
                            var li = document.createElement('li');
                            li.setAttribute('class', 'ui-widget-content ui-corner-tr');
                            li.innerHTML = ['<img src="',
                            e.target.result, 
                            '"style="object-fit:contain;height:100px;padding: 0.2em;align-items:center;"><input type="hidden" id="qq-file-id" name="qq-file-id" value=',
                            i,
                            '><a class="ui-icon ui-icon-trash trash-custom-ecommerce" href="#"></a><a class="ui-icon-rotate rotateItem" style="cursor: pointer;"><i class="rotateItem fas fa-xs fa-sync-alt" style="padding: 0.2em;width: 2em;height: 1.3em;"></i><input type="hidden" name="rotateTimes" value="0"></a>'].join('');
                            
                            document.getElementById('customSort').insertBefore(li, null);
                            displayUploading(false, new_i);
                            new_i += 1
                            var elementList = $("ul.gallery > li")  
                            elementList.unbind()
                            deleteRotateItem(elementList)
                        };//render thumbnail
                    })(f)//onload
                    reader.readAsDataURL(f);
                }//for images
                buttonImageUpload.attr('disabled', false);
                
                
         
        })//change-buttonImageUpload

        formSubmit.submit(
        function(event){
        event.preventDefault()
        var createFormSubmitBtn = formSubmit.find("[type='submit']")
        var createFormSubmitBtnTxt = createFormSubmitBtn.text()
        var formData = new FormData(this);
        // var files = $(this)[0].files;
        // console.log(files)
        // $.each(files, 
        //     function(index, value){
        //         formData.append('image', value)
        //     })//each files
        console.log(formData)
        var elements = $('#example-form-1 ul li')
        var keyArray = []
        var rotateArray = []
        $.ajax({
            url: action,
            method: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data){
                console.log('hi')
            },
            error: function(errorData){
                console.log('error')
            }
        })//ajax
        // Activate Spinner
        displayCreating(createFormSubmitBtn, authenticityCheckBtn, "",true, currentPath)
        // $.each(elements,
        // function(index, value){
        //     var attr = $(value).find("[name='qq-file-id']").val()
        //     var rotatedImageTimes = $(value).find("[name='rotateTimes']").val()
        //     keyArray.push(attr)  
        //     rotateArray.push(rotatedImageTimes)
        // })//eacharray
        // $.ajax({
        // url: action,
        // method:'POST',
        // data: formData,
        // success: function(data){
        //     $('.is-invalid').removeClass('is-invalid')
        //     $('p').remove('.invalid-feedback')
        //     if(data['error']) {
        //     $.each(data['error'],
        //         function(index, value){
        //             var btnText = createFormSubmitBtnTxt
        //             displayCreating(createFormSubmitBtn, authenticityCheckBtn, btnText,false, currentPath)
        //             if ($('.'+index).length==0){
        //                 $('#id_' + index).addClass('is-invalid')
        //                 $('#id_' + index).after("<p class='m-0 invalid-feedback "+index+"'><strong>"+value+"</strong></p>")  
        //             }//if  
        //         })//each
        //         }//if there are errors
        //     else {
        //       $.ajax({
        //         url: action_order,
        //         method:'POST',
        //         data: {'data[]':keyArray, 'slug':data.slug, 'rotate[]':rotateArray},
        //         success:function(data){
        //             },//success second ajax
        //         error:function(errorData){
        //             }//error second ajax
        //         })//ajax in ajax
        //         window.location.href=data.url
        //             }//else
        //         },//success
        // error:function(errorData){
        //     }//error_1
        // })//ajax
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
        var formData = formSubmit.serialize()
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
            keyArray.push(val.val())
            var rotatedImageTimes = $(value).find("[name='rotateTimes']").val()
            rotateArray.push(rotatedImageTimes)
        })//each
        $.ajax({
        url: action_update,
        method:'POST',
        data: formData,
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
                $.ajax({
                url: action,
                method:'POST',
                data: {'data[]':keyArray, 'rotate[]':rotateArray},
                success: function(data){
                    window.location.href=url
                },//success
                error: function(errorData){
                // $.alert({
                // title: 'OOps!',
                // content: 'Simple alert!',
                // theme: "modern"
                // });
                console.log('some error');
                }//error
                })//ajax in ajax

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