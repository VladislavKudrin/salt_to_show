// Google
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-150733918-1');




// put cursor at end
    jQuery.fn.putCursorAtEnd = function() {

      return this.each(function() {
        
        // Cache references
        var $el = $(this),
            el = this;

        // Only focus if input isn't already
        if (!$el.is(":focus")) {
         $el.focus();
        }

        // If this function exists... (IE 9+)
        if (el.setSelectionRange) {

          // Double the length because Opera is inconsistent about whether a carriage return is one character or two.
          var len = $el.val().length * 2;
          
          // Timeout seems to be required for Blink
          setTimeout(function() {
            el.setSelectionRange(len, len);
          }, 1);
        
        } else {
          
          // As a fallback, replace the contents with itself
          // Doesn't work in Chrome, but Chrome supports setSelectionRange
          $el.val($el.val());
          
        }

        // Scroll to the bottom, in case we're in a tall textarea
        // (Necessary for Firefox and Chrome)
        this.scrollTop = 999999;

      });
    };




$(document).ready(
  
  function(){
  



    //search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") //input name = 'q'
    var actionEndpoint = searchForm.attr("action");
    var searchAutocompleteInput = $("#searchAutoComplete")
    var collapseSearchbar = $("#collapseSearchbar")
    var currentPath = window.location.href
    if (currentPath.indexOf("search") != -1){
    collapseSearchbar.addClass("show");
    searchAutocompleteInput.focus();
    searchAutocompleteInput.putCursorAtEnd() // should be chainable
    }

    collapseSearchbar.on('show.bs.collapse', function () {
      console.log('Input on');
      searchAutocompleteInput.focus();
    })

    $.ajax({
    url: actionEndpoint,
    data: searchInput,
    success: function(data){
        var availableTags = data.filtered_products
        $( "#searchAutoComplete" ).autocomplete({
          source: availableTags,
          position: { my: "left bottom", at: "left top", collision: "flip" },
          open: function (event, ui) {
            $("body").css({overflow: 'hidden'});
          },
          close: function () {
              $("body").css({overflow: 'inherit'});
          }
          }).data("ui-autocomplete")._renderItem=function (ul, item) { //for  clicking results
            return $("<li></li>")
            .data("item.autocomplete", item)
            .append("<a href='/search/?q=" + item.value + "'>"+"<span class='suggestions'>" +item.value+ "</span></a>")
            .appendTo(ul);
          };
    }, 
    error: function(errorData){
        console.log('some error');
        }
    })//ajax











  // Region Modal Initialization

    var regionInput = $('#region_input')
    var urlRegion = '/region-init/'
    if (regionInput.val() == 'None'){
    var location = window.location.href
    $.ajax({
              url: urlRegion,
              data:{location: location},
              success: function(data){
                  $(document.body).append(data.html)
                  $('#modal-region').modal({
                              keyboard: false,
                              backdrop: 'static',
                              focus:true
                            })
                  $('#modal-region').modal('show')
                 
                  }//success_first

              })//ajax
    }//if region none










    var languageGlobe = $('#language-pref') 
    $('.language-preference-globe').click(
        function(event){ 
          languageGlobe.select()
    }
    )//onclick



    // Labels and placeholders for accounts settings and checkout
    var inputs = [
    "#id_user_form-username", 
    "#id_user_form-email", 
    "#id_user_form-region", 
    "#id_address_form-name", 
    "#id_address_form-additional_line", 
    "#id_address_form-street", 
    "#id_address_form-city", 
    "#id_address_form-number", 
    "#id_address_form-postal_code", 
    "#id_address_form-state", 
    "#id_address_form-country", 
    "#id_address_form-post_office", 
    "#id_address_form-phone",
    "#id_title",
    "#id_brand",
    "#id_title",
    "#id_sex",
    "#id_undercategory",
    "#id_condition",
    "#id_size",
    "#id_price",
    "#id_shipping_price",
    "#id_description",
    "#id_email",
    "#id_content",
    "#id_national_shipping",
    "#id_region",
    "#id_old_password",
    "#id_new_password1",
    "#id_new_password2",
    ]

    jQuery.each(inputs, function(index, item) {
        var item_val = $(item).val()
        var input_str = 'input'+item
        var css_small = {"font-size": "10px", "padding-top": "1px"}
        var css_big = {"font-size": "14px", "padding-top": "calc(.375rem + 1px)"}

        // for prefilled fields
        if (item_val){
          $("label[for='" + $(item).attr('id') + "']").css(css_small);
        }

        // on focus
        $(item).focus(function() {
          $("label[for='" + $(this).attr('id') + "']").css(css_small);
        });

        // if fields were touched
        $(item).blur(function() {
          var input_str_val = $(input_str).val()
          // if fields were filled out
          if ( input_str_val ) {
            $("label[for='" + $(this).attr('id') + "']").css(css_small);
          };
          // if fields were left blank
          if ( input_str_val == '' ) {
            $("label[for='" + $(this).attr('id') + "']").css(css_big);
          };

        });
    });



    //click image
    function click_image(){
      $('.wish-div').click(
        function(e){
          $targetCard = $(e.target)
          if (e.target.tagName == 'IMG'){
          linkCard = $targetCard.attr('link_for_click')
          window.location.href = linkCard
          }//if img
        })//click card
    }//click image
          





      
})

      



    //contactFormHandler
    var contact=$('.contact-form')
    // var userEmail = contact.find("[name='popchik']")
    // var input = contact.find("[name='email']").val(userEmail.val())
    var language = $('#language').val()
    var contactForm = $('.contact-form')
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    function displaySubmitting(submitBtn, defaultText, doSubmit, submitText){
      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fas fa-spin fa-spinner'></i> "+submitText)
        submitBtn.attr("disabled", true)
        
      } //if submit
      else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
        submitBtn.attr("disabled", false)
      }
    }            
    contactForm.submit(
      function(event){
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        var submitText = $('#contactSubmitted').text()
        displaySubmitting(contactFormSubmitBtn, "",true, submitText)
        $.ajax({
          method: contactFormMethod,
          url: contactFormEndpoint,
          data: contactFormData,
          success: function(data){
          if (data.report){
            $.alert({
              title: data.success_message,
              content: data.message,
              theme: "modern",
              buttons:{
                confirm:{
                  text: 'OK',
                  action:function(){
                  window.location.href = data.location
                        }//action OK alert
                      }//confirm
                    }//buttons
                  })//alert
              }//if report
          else{
            thisForm[0].reset()
            $.alert({
              title: data.success_message,
              content: data.message,
              theme: "modern",
              })//alert
          setTimeout(
            function()
            {displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt,false)}, 1000)
        }//if not report

          
        },
          error: function(error){
            console.log(error.responseJSON)
            var jsonData = error.responseJSON
            var msg = ""
            $.each(jsonData, function(key, value){
              msg += key + ": " + value[0].message + "</br>"
            })
            console.log('some error');
            setTimeout(
            function()
            {displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt,false, language)}, 1000)
          }
        })
      })






  //Product Delete Alert Ajax
    var languagePref = $('#language_pref')
    var deleteForm=$(".delete-product-form")
    var instance_id = deleteForm.attr("data_id")
    var instance_title = deleteForm.attr("product_title")
    var instance_user = deleteForm.attr("data_user")
    var action = deleteForm.attr("action")
    var data_endpoint = deleteForm.attr("data-endpoint")
    var next_url = deleteForm.attr("next_url")
    var deleteTemplate = $.templates("#delete-product-confirm-form")
    if (languagePref.val() == 'RU'){
      var placeholderText = 'Почему?'
      var titleConfirm = 'Удалить Айтем?'
      var btnText = 'Удалить'
      var titleConfirmSecond = 'Спасибо'
      var contentConfirmSecond = 'Айтем успешно удален'
      var cancelText = 'Отмена'
    }//if ru
    else if (languagePref.val() == 'UK'){
      var placeholderText = 'Чому?'
      var titleConfirm = 'Видалити айтем?'
      var btnText = 'Видалити'
      var titleConfirmSecond = 'Дякуємо'
      var contentConfirmSecond = 'Айтем успішно видалений'
      var cancelText = 'Скасувати'
    }//if ru
    else{
      var placeholderText = 'Why do you want delete this product?'
      var titleConfirm = 'Delete Your Product?'
      var btnText = 'Delete'
      var titleConfirmSecond = 'Thanks'
      var contentConfirmSecond = 'Product has been deleted'
      var cancelText = 'Cancel'
    }//if not ru
    var deleteTemplateDataContext = {
       action_url: action,
       data_endpoint: data_endpoint,
       user: instance_user,
       product_id: instance_id,
       product_title:instance_title,
       next_url:next_url,
       placeholder_text:placeholderText
            }
    var deleteTemplateHtml  = deleteTemplate.render(deleteTemplateDataContext)
      deleteForm.submit(
      function(event){
      var thisForm = $(this)
      var dataEndpoint = thisForm.attr("action");
      var actionEndpoint = thisForm.attr("data-endpoint");
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();
      event.preventDefault()
      var deleteComfirmFormTemplate = $.templates("#delete-product-confirm-form")
      $.confirm({
    title: titleConfirm,
    // content: '' + deleteTemplateHtml,
    content: '', 
    buttons: {
        formSubmit: {
            text: btnText,
            btnClass: 'btn pdv button-black btn-block',
            action: function () {
                $.ajax({
                    url: actionEndpoint,
                    method: httpMethod,
                    data: formData,
                    success: function(){

                      $.confirm({
                        title: titleConfirmSecond,
                        content: contentConfirmSecond,
                        buttons:{
                          confirm: { 
                            text: 'Ok',
                            btnClass: 'btn pdv button-black btn-block',
                            action: function(){
                            window.location.href=next_url
                          }},
                        }//buttons
                      })},//success
                    error: function(errorData){
                      console.log(errorData)
                      $.alert({
                          title: 'Error',
                          content: 'Romaloh',
                          theme: "modern"
                              });//alert
                                               }//error
                      })//ajax
            }//action
        },//formSubmit
        cancel: {
          text:cancelText,
          btnClass: 'btn pdv btn-block btn-outline-danger',
          action: function (){

          }//action cancel
        }//cancel
    },//buttons
});


    })


// Wishlist Product List View

var productForm=$(".form-product-ajax-wishlist")
function bind_ajax_heart(form){
  form.submit(
      function (event){

        event.preventDefault()
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
          url: actionEndpoint,
          method: httpMethod,
          data: formData,
          success: function(data){
            var submitSpan = thisForm.find(".submit-span-wishlist")
            if (data.added){
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='fas fa-heart fa-5x'></i></button>")
            }
            else {
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='far fa-heart fa-5x'></i></button>")
            }

            var navbarCount = $(".navbar-wish-count")
            navbarCount.text(data.wishes_count)
        },
          error: function(errorData){
            console.log('some error');
  }
})
      }
    )
  }
  bind_ajax_heart(productForm)

  
// lazy loading
  $.extend($.lazyLoadXT, {
    // edgeY:  200,
    // edgeX:  200,
    // blankImage: "{% static 'img/dust_stratches.png' %}",
    // blankImage: "https://upload.wikimedia.org/wikipedia/commons/5/59/Empty.png",
    scrollContainer: document.getElementById("myTabContent"),
    srcAttr: 'data-src'
  });
// For ajax
  $(window).on('ajaxComplete', function() {
  setTimeout(function() {
    $(window).lazyLoadXT();
  }, 50);
});
    

// Wishlist Product Detail View

      var productForm=$(".form-product-ajax-wishlist-detail")
    productForm.submit(

      function(event){

        event.preventDefault()
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
          url: actionEndpoint,
          method: httpMethod,
          data: formData,
          success: function(data){
            var submitSpan = thisForm.find(".submit-span-wishlist")
            if (data.added){
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='fas fa-heart fa-2x black-heart'></i></button>")
            }
            else {
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='far fa-heart fa-2x black-heart'></i></button>")
            }

            var navbarCount = $(".navbar-wish-count")
            navbarCount.text(data.wishes_count)

            var likesCount = $(".product-likes")
            console.log('HUINA', data.product_likes)
            likesCount.text(data.product_likes)
        },
          error: function(errorData){
            console.log('some error');
  }
})
      }
    )

 