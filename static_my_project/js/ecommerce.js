

$(document).ready(
  
  function(){
  

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
                  $('.modal').modal('show')
                 
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
          




    //search
      var searchForm = $(".search-form")
      var searchInput = searchForm.find("[name='q']") //input name = 'q'
      var actionEndpoint = searchForm.attr("action");
      var searchAutocompleteInput = $("#searchAutoComplete")
      var currentPath = window.location.href

      // on search page autofocus on by default
      if (currentPath.indexOf("search") != -1){
        searchAutocompleteInput.focus();
      }

      $.ajax({
      url: actionEndpoint,
      data: searchInput,
      success: function(data){
              var availableTags = data.filtered_products
              var searchBtn = searchForm.find("[type='submit']")

              $( "#searchAutoComplete" ).autocomplete({
                          source: availableTags,
                          position: { my: "left-24 bottom", at: "left top", collision: "flip" }
                          }).data("ui-autocomplete")._renderItem=function (ul, item) { //for  clicking results
                          return $("<li></li>")
                          .data("item.autocomplete", item)
                          .append("<a href='/search/?q=" + item.value + "'>"+"<span class='suggestions'>" +item.value+ "</span></a>")
                          .appendTo(ul);
};
              $('#ui-id-1').attr('style', 'z-index:2000;')
              }, 
      error: function(errorData){
          console.log('some error');
            }
      })//ajax
      
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
            // $.alert({
            //   title: 'OOps!',
            //   content: msg,
            //   theme: "modern"
            // })
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
    else if (languagePref.val() == 'UA'){
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
    content: '' + deleteTemplateHtml,
    buttons: {
        formSubmit: {
            text: btnText,
            btnClass: 'btn btn-dark',
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
            // $.alert({
            //   title: 'Oops!',
            //   content: errorData,
            //   theme: "modern",
            // });
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
    blankImage: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solid_white.svg/1024px-Solid_white.svg.png",
    scrollContainer: document.getElementById("my-custom-scrollbar"),
    srcAttr: 'data-src'
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
            // $.alert({
            //   title: 'Oops!',
            //   content: errorData,
            //   theme: "modern",
            // });
            console.log('some error');
  }
})
      }
    )

  //   //delete add cart Ajax
  //   var productForm=$(".form-product-ajax")
  //   productForm.submit(
  //     function(event){
  //       event.preventDefault()
  //       var thisForm = $(this)
  //       var actionEndpoint = thisForm.attr("action");
  //       var actionEndpoint = thisForm.attr("data-endpoint");
  //       console.log(actionEndpoint)
  //       var httpMethod = thisForm.attr("method");
  //       var formData = thisForm.serialize();

  //       console.log(thisForm.attr("action"), thisForm.attr("method"))
  //       $.ajax({
  //         url: actionEndpoint,
  //         method: httpMethod,
  //         data: formData,
  //         success: function(data){
  //           var submitSpan = thisForm.find(".submit-span")
  //           if (data.added){
  //             submitSpan.html("In Cart <button type='submit' class='btn btn-link'>Remove?</button>")
  //           }
  //           else {
  //             submitSpan.html("<button type='submit' class='btn btn-dark'>Add to Cart</button>")
  //           }
  //           var navbarCount = $(".navbar-cart-count")
  //           navbarCount.text(data.cartItemCount)
  //           var currentPath = window.location.href

  //           if (currentPath.indexOf("cart") != -1){
  //             refreshCart()
  //           }
  //         },
  //         error: function(errorData){
  //           $.alert({
  //             title: 'OOps!',
  //             content: 'Simple alert!',
  //             theme: "modern"
  //           });
  //         }

  //       })
  //     }
  //   )
  //   function refreshCart(){
  //     console.log("privet")
  //     var cartTable = $(".cart-table")
  //     var cartBody = cartTable.find(".cart-body")
  //     //cartBody.html("<h1>Changed</h1>")
  //     var productRows = cartBody.find(".cart-product")
  //     var currentUrl = window.location.href
  //     var refreshCartUrl='/api/cart/';
  //     var refreshCartMethod = "GET";
  //     var data = {};
  //     $.ajax({
  //       url: refreshCartUrl,
  //       method: refreshCartMethod,
  //       data: data,
  //       success: function(data){
  //         var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
  //         if (data.products.length > 0){
  //           productRows.html(" ")
  //           i = data.products.length
  //           $.each(data.products,
  //             function(index, value){
  //               console.log(value)
  //               var newCartItemRemove = hiddenCartItemRemoveForm.clone()
  //               newCartItemRemove.css("display", "block")
  //               //newCartItemRemove.removeClass("hidden-class")
  //               newCartItemRemove.find(".cart-item-product-id").val(value.id)
  //               cartBody.prepend(
  //                 "<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.title + "</a>" + newCartItemRemove.html() + "<td>" + value.price + "</td>" + "</td></tr>")
  //               i--

  //             })
            
  //           cartBody.find(".cart-subtotal").text(data.subtotal)
  //           cartBody.find(".cart-total").text(data.total)
  //         } 
  //         else{
  //           window.location.href = currentUrl
  //         }
  //       },
  //       error: function(errorData){
  //         $.alert({
  //             title: 'OOps!',
  //             content: 'Simple alert!',
  //             theme: "modern"
  //           });
  //       }
      
  //     })
  //   }
  // }
  //  )





  //   function refreshCart(){
  //     console.log("privet")
  //     var cartTable = $(".cart-table")
  //     var cartBody = cartTable.find(".cart-body")
  //     //cartBody.html("<h1>Changed</h1>")
  //     var productRows = cartBody.find(".cart-product")
  //     var currentUrl = window.location.href
  //     var refreshCartUrl='/api/cart/';
  //     var refreshCartMethod = "GET";
  //     var data = {};
  //     $.ajax({
  //       url: refreshCartUrl,
  //       method: refreshCartMethod,
  //       data: data,
  //       success: function(data){
  //         var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
  //         if (data.products.length > 0){
  //           productRows.html(" ")
  //           i = data.products.length
  //           $.each(data.products,
  //             function(index, value){
  //               console.log(value)
  //               var newCartItemRemove = hiddenCartItemRemoveForm.clone()
  //               newCartItemRemove.css("display", "block")
  //               //newCartItemRemove.removeClass("hidden-class")
  //               newCartItemRemove.find(".cart-item-product-id").val(value.id)
  //               cartBody.prepend(
  //                 "<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.title + "</a>" + newCartItemRemove.html() + "<td>" + value.price + "</td>" + "</td></tr>")
  //               i--

  //             })
            
  //           cartBody.find(".cart-subtotal").text(data.subtotal)
  //           cartBody.find(".cart-total").text(data.total)
  //         } 
  //         else{
  //           window.location.href = currentUrl
  //         }
  //       },
  //       error: function(errorData){
  //         $.alert({
  //             title: 'OOps!',
  //             content: 'Simple alert!',
  //             theme: "modern"
  //           });
  //       }  
  //     })
  //   }
  // })