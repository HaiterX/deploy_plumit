console.log("JS работает");


var swiper = new Swiper(".mySwiper", {
    cssMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
    },
    mousewheel: true,
    keyboard: true,
  });

$(window).keyup(function(e){
  var target = $('.checkbox-btn input:focus');
  if (e.keyCode == 9 && $(target).length){
      $(target).parent().addClass('focused');
  }
});

$('.checkbox-btn input').focusout(function(){
  $(this).parent().removeClass('focused');
});

$('.header-mobile-burger').click(function(){
  $('.header-mobile-block').addClass('show-navbar');
  $('body').addClass('stop-body') && $('html').addClass('stop-body');
});
$('.header-x-mobile').click(function(){
  $('.header-mobile-block').removeClass('show-navbar');
  $('body').removeClass('stop-body') && $('html').removeClass('stop-body');
})


// var hashTagActive = "";
// $("a").on("click touchstart" , function (event) {
//     if(hashTagActive != this.hash) { //this will prevent if the user click several times the same link to freeze the scroll.
//         event.preventDefault();

//         var dest = 0;
//         if ($(this.hash).offset().top > $(document).height() - $(window).height()) {
//             dest = $(document).height() - $(window).height();
//         } else {
//             dest = $(this.hash).offset().top;
//         }
//         //go to destination
//         $('html,body').animate({
//             scrollTop: dest
//         }, 2000, 'swing');
//         hashTagActive = this.hash;
//     }
// });



window.onload = function () {
  document.body.classList.add('loaded');
}

$('#st-serv').click(function(){
  $('#st-serv-modal').addClass('show-modal') && $('.modal-background').addClass('show-modal');
  $('body').addClass('stop-body') && $('html').addClass('stop-body');
});
$('#le-serv').click(function(){
  $('#le-serv-modal').addClass('show-modal') && $('.modal-background').addClass('show-modal');
  $('body').addClass('stop-body') && $('html').addClass('stop-body');
});
$('#rd-serv').click(function(){
  $('#rd-serv-modal').addClass('show-modal') && $('.modal-background').addClass('show-modal');
  $('body').addClass('stop-body') && $('html').addClass('stop-body');
});
$('#fo-serv').click(function(){
  $('#fo-serv-modal').addClass('show-modal') && $('.modal-background').addClass('show-modal');
  $('body').addClass('stop-body') && $('html').addClass('stop-body');
});
$('#fi-serv').click(function(){
  $('#fi-serv-modal').addClass('show-modal') && $('.modal-background').addClass('show-modal');
  $('body').addClass('stop-body') && $('html').addClass('stop-body');
});
$('#six-serv').click(function(){
  $('#six-serv-modal').addClass('show-modal') && $('.modal-background').addClass('show-modal');
  $('body').addClass('stop-body') && $('html').addClass('stop-body');
});
$('.modal-close').click(function(){
  $('.modal-window-services').removeClass('show-modal');
  $('.modal-background').removeClass('show-modal');
  $('body').removeClass('stop-body');
  $('html').removeClass('stop-body'); 
})



$('.step-work-block').click(function(){
  $(this).toggleClass('show-block-step');
});

$('.money-check input').on('change', function() {
  $('.money-check input').not(this).prop('checked', false);  
});

  $.mask.definitions['h'] = "[0|1|3|4|5|6|7|9]"
  $(".mask-phone").mask("+7 (h99) 999-99-99");