(function ($) {
    $(".form-main-contact").submit(function (event) {
      event.preventDefault();
   

      let successSendText = "Сообщение успешно отправлено";
      let errorSendText = "Сообщение не отправлено. Попробуйте еще раз!";
      let requiredFieldsText = "Заполните поля с именем и телефоном";
   
     
      let message = $(this).find(".contact-form__message");
   
      let form = $("#" + $(this).attr("id"))[0];
      let fd = new FormData(form);
      $.ajax({
        url: "/telegramform/php/send-message-to-telegram.php",
        type: "POST",
        data: fd,
        processData: false,
        contentType: false,
        beforeSend: () => {
          $(".preloader").addClass("preloader_active");
        },
        success: function success(res) {
          $(".preloader").removeClass("preloader_active");
  
          let respond = $.parseJSON(res);
   
          if (respond === "SUCCESS") {
            $('.success-form').addClass('show-modal') && $('.modal-background').addClass('show-modal');
            $('body').addClass('stop-body') && $('html').addClass('stop-body'); 
            $('#contact-form').trigger("reset");
          } else if (respond === "NOTVALID") {
            $('.failed-form').addClass('show-modal') && $('.modal-background').addClass('show-modal');
            $('body').addClass('stop-body') && $('html').addClass('stop-body'); 
          } else {
            message.text(errorSendText).css("color", "#d42121");
            $('.error-form').addClass('show-modal') && $('.modal-background').addClass('show-modal');
            $('body').addClass('stop-body') && $('html').addClass('stop-body'); 
          }
        }
      });
    });
  })(jQuery);