$(document).ready(function () {
    $('#signUpPhone , #profilePhone').mask('+7 (***) ***-**-**')
})
$('.sign-selector').click(function () {
    $('#signModal').animate({left: 0, opacity: "show", background: '$yellow', transition: '.2s linear'}, 500)
    $('#index-footer-image').animate({'opacity': 1,'z-index':25},500)
})
$('#sign-modal-close').click(function () {
    $('#signModal').animate({left: '-200%', opacity: "show"}, 500)
    $('#index-footer-image').animate({'opacity': 0},500)
})
$('#signUpSelector').click(function () {
    $('#signUpForm').css({'z-index':'25','opacity':'1'})
    $('#signInForm').fadeOut('fast', function () {

    })
    $('#signUpForm').fadeIn('fast', function () {

    })
})
$('#signInSelector').click(function () {
    $('#signUpForm').css('opacity',0)
    $('#signUpForm').fadeOut('fast', function () {

    })
    $('#signInForm').fadeIn('fast', function () {

    })
})

$('#signUpSelector').click(function () {

    $(this).addClass('active')
    $('#signInSelector').removeClass('active')
})

$('#signInSelector').click(function () {
 $(this).addClass('active')
    $('#signUpSelector').removeClass('active')
})

$('.ripple').on('click', function(event) {
    var $div = $('<div/>'),
        btnOffset = $(this).offset(),
        xPos = event.pageX - btnOffset.left,
        yPos = event.pageY - btnOffset.top;

    $div.addClass('ripple-effect');
    var $ripple = $(".ripple-effect");

    $ripple.css("height", $(this).height());
    $ripple.css("width", $(this).height());
    $div
        .css({
            top: yPos - ($ripple.height() / 2),
            left: xPos - ($ripple.width() / 2),
            background: $(this).data("ripple-color")
        })
        .appendTo($(this));

    window.setTimeout(function() {
        $div.remove();
    }, 1200);
});