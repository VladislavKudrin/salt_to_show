$(document).ready(
  function(){
    //contactFormHandler
    var contactForm = $('.contact-form')
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    function displaySubmitting(submitBtn, defaultText, doSubmit){
      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Sending....")
      } else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
      }
    }            
    contactForm.submit(
      function(event){
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn, "",true)
        $.ajax({
          method: contactFormMethod,
          url: contactFormEndpoint,
          data: contactFormData,
          success: function(data){
            thisForm[0].reset()
            $.alert({
              title: 'Success',
              content: data.message,
              theme: "modern"
          })
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
            {displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt,false)}, 1000)
          }
        })
      })



  









    //Auto Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") //input name = 'q'
    var typingTimer;
    var typingInterval = 500 //0.5 seconds
    var searchBtn = searchForm.find("[type='submit']")
    searchInput.keyup(  //released key
      function(event){
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
      })
    searchInput.keydown( //key pressed
      function(event){
        clearTimeout(typingTimer)
     
      })
      
      function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fas fa-spin fa-spinner'></i> Searching....")
      }

      function performSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function(){
          window.location.href='/search/?q=' + query   
        }, 1000)
                   
      }


  


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
      var dataEndpoint = thisForm.attr("action");
      var actionEndpoint = thisForm.attr("data-endpoint");
      var httpMethod = thisForm.attr("method");

      var formData = thisForm.serialize();
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
                          confirm: function(){
                            window.location.href=next_url
                          },
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





    //delete add cart Ajax
    var productForm=$(".form-product-ajax")
    productForm.submit(
      function(event){
        event.preventDefault()
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        console.log(thisForm.attr("action"), thisForm.attr("method"))
        $.ajax({
          url: actionEndpoint,
          method: httpMethod,
          data: formData,
          success: function(data){
            var submitSpan = thisForm.find(".submit-span")
            if (data.added){
              submitSpan.html("In Cart <button type='submit' class='btn btn-link'>Remove?</button>")
            }
            else {
              submitSpan.html("<button type='submit' class='btn btn-dark'>Add to Cart</button>")
            }
            var navbarCount = $(".navbar-cart-count")
            navbarCount.text(data.cartItemCount)
            var currentPath = window.location.href

            if (currentPath.indexOf("cart") != -1){
              refreshCart()
            }
          },
          error: function(errorData){
            $.alert({
              title: 'OOps!',
              content: 'Simple alert!',
              theme: "modern"
            });
          }

        })
      }
    )
    function refreshCart(){
      console.log("privet")
      var cartTable = $(".cart-table")
      var cartBody = cartTable.find(".cart-body")
      //cartBody.html("<h1>Changed</h1>")
      var productRows = cartBody.find(".cart-product")
      var currentUrl = window.location.href
      var refreshCartUrl='/api/cart/';
      var refreshCartMethod = "GET";
      var data = {};
      $.ajax({
        url: refreshCartUrl,
        method: refreshCartMethod,
        data: data,
        success: function(data){
          var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
          if (data.products.length > 0){
            productRows.html(" ")
            i = data.products.length
            $.each(data.products,
              function(index, value){
                console.log(value)
                var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                newCartItemRemove.css("display", "block")
                //newCartItemRemove.removeClass("hidden-class")
                newCartItemRemove.find(".cart-item-product-id").val(value.id)
                cartBody.prepend(
                  "<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.title + "</a>" + newCartItemRemove.html() + "<td>" + value.price + "</td>" + "</td></tr>")
                i--

              })
            
            cartBody.find(".cart-subtotal").text(data.subtotal)
            cartBody.find(".cart-total").text(data.total)
          } 
          else{
            window.location.href = currentUrl
          }
        },
        error: function(errorData){
          $.alert({
              title: 'OOps!',
              content: 'Simple alert!',
              theme: "modern"
            });
        }
      
      })
    }
  }
        )