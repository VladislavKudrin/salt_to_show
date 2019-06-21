$(document).ready(
  
  function(){
      var searchForm = $(".search-form")
      var searchInput = searchForm.find("[name='q']") //input name = 'q'
      var actionEndpoint = searchForm.attr("action");


      $.ajax({
      url: actionEndpoint,
      data: searchInput,
      success: function(data){
              var availableTags = data.filtered_products
              var searchBtn = searchForm.find("[type='submit']")
              $( "#searchAutoComplete" ).autocomplete({
                          source: availableTags
                          }).data("ui-autocomplete")._renderItem=function (ul, item) { //for  clicking results
                          return $("<li></li>")
                          .data("item.autocomplete", item)
                          .append("<a href='/search/?q=" + item.value + "'>"+"<span class='suggestions'>" +item.value+ "</span></a>")
                          .appendTo(ul);
                          };
              }, 
      error: function(errorData){
          $.alert({
              title: 'OOps!',
              content: 'Simple alert!',
              theme: "modern"
            });
            }
      })//ajax
      
})

      






    //contactFormHandler
    var language = $('#language').val()
    var contactForm = $('.contact-form')
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    function displaySubmitting(submitBtn, defaultText, doSubmit, languageOption){
      if (doSubmit){
        if (languageOption == 'RU'){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Отправка....")
        submitBtn.attr("disabled", true)
        }//if rus
        else {
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Sending....")
        submitBtn.attr("disabled", true)
        }//if not rus
        
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
        displaySubmitting(contactFormSubmitBtn, "",true, language)
        $.ajax({
          method: contactFormMethod,
          url: contactFormEndpoint,
          data: contactFormData,
          success: function(data){
            thisForm[0].reset()
            if (language == 'RU'){
              $.alert({
              title: 'Успешно отправлено',
              content: data.message,
              theme: "modern"
              })//alert
            }//if rus
            else {
              $.alert({
              title: 'Success',
              content: data.message,
              theme: "modern"
              })//alert
            }//if not rus

          setTimeout(
            function()
            {displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt,false)}, 1000)
          
        },
          error: function(error){
            console.log(error.responseJSON)
            var jsonData = error.responseJSON
            var msg = ""
            $.each(jsonData, function(key, value){
              msg += key + ": " + value[0].message + "</br>"
            })
            $.alert({
              title: 'OOps!',
              content: msg,
              theme: "modern"
            })
            setTimeout(
            function()
            {displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt,false, language)}, 1000)
          }
        })
      })



  








  


  //Product Delete Alert Ajax
    var deleteForm=$(".delete-product-form")
    var instance_id = deleteForm.attr("data_id")
    var instance_title = deleteForm.attr("product_title")
    var instance_user = deleteForm.attr("data_user")
    var action = deleteForm.attr("action")
    var data_endpoint = deleteForm.attr("data-endpoint")
    var next_url = deleteForm.attr("next_url")
    var deleteTemplate = $.templates("#delete-product-confirm-form")
    var deleteTemplateDataContext = {
       action_url: action,
       data_endpoint: data_endpoint,
       user: instance_user,
       product_id: instance_id,
       product_title:instance_title,
       next_url:next_url
            }
    var deleteTemplateHtml  = deleteTemplate.render(deleteTemplateDataContext)
      deleteForm.submit(
      function(event){
      var thisForm = $(this)
      console.log(thisForm)
      var dataEndpoint = thisForm.attr("action");
      var actionEndpoint = thisForm.attr("data-endpoint");
      var httpMethod = thisForm.attr("method");
      console.log('hello')
      console.log(actionEndpoint)
      console.log(httpMethod)
      var formData = thisForm.serialize();
      console.log(formData)
      event.preventDefault()
      console.log(deleteTemplateHtml)
      var deleteComfirmFormTemplate = $.templates("#delete-product-confirm-form")
      $.confirm({
    title: 'Delete Your Product?',
    content: '' + deleteTemplateHtml,
    buttons: {
        formSubmit: {
            text: 'Delete',
            btnClass: 'btn btn-dark',
            action: function () {
                $.ajax({
                    url: actionEndpoint,
                    method: httpMethod,
                    data: formData,
                    success: function(){

                      $.confirm({
                        title: 'Thank you for your money!',
                        content:'Product has been deleted. Mojete sosnut pisku',
                        buttons:{
                          confirm: { 
                            text: 'Ok',
                            action: function(){
                            window.location.href=next_url
                          }},
                        }
                      })},
                    error: function(errorData){
                      console.log(errorData)
                      $.alert({
                          title: 'Error',
                          content: 'Romaloh',
                          theme: "modern"
                              });
                                               }
                      })
            }
        },
        cancel: function () {
            //close
        },
    },
});


    })


// Wishlist Product List View

    var productForm=$(".form-product-ajax-wishlist")
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
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='fas fa-heart fa-5x'></i></button>")
            }
            else {
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='far fa-heart fa-5x'></i></button>")
            }

            var navbarCount = $(".navbar-wish-count")
            navbarCount.text(data.wishes_count)
        },
          error: function(errorData){
            $.alert({
              title: 'Oops!',
              content: errorData,
              theme: "modern",
            });
  }
})
      }
    )
      

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
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='fas fa-heart fa-2x'></i></button>")
            }
            else {
              submitSpan.html("<button type='submit' class='hidden-button hidden-button-outline'><i class='far fa-heart fa-2x'></i></button>")
            }

            var navbarCount = $(".navbar-wish-count")
            navbarCount.text(data.wishes_count)
        },
          error: function(errorData){
            $.alert({
              title: 'Oops!',
              content: errorData,
              theme: "modern",
            });
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