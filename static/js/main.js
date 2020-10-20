$('#start-modal-button').click(function (){
    $('.start-modal').addClass('start-modal-active')
})
$('#start-modal-close').click(function (){
    $('.start-modal').removeClass('start-modal-active')
})

$('#popular-problems').click(function (){
    $('#popular-problems-modal').addClass('popular-problems-modal-active')
    // $('#popular-problems-modal-content').addClass('wow flipInX')
})
$('#popular-problems-modal-close').click(function (){
    $('#popular-problems-modal').removeClass('popular-problems-modal-active')
    // $('#popular-problems-modal-content').removeClass('wow flipInX')
})
$('#payment-read-more').click(function (){
    $('#modal-payment').addClass('modal-payment-active')
})
$('#modal-payment-close').click(function (){
    $('#modal-payment').removeClass('modal-payment-active')
})
setTimeout(function () {
        $('#preloader').css('display', 'none')
}, 4000)
setTimeout(function () {
    $('#preloader-bg').css({'display':'none','z-index':'-1000'})
},3000)
$('#chatBtn').click(function () {
    if($('#mobNav-support').attr("type") == 0){
        $('#chatra-wrapper').css({'bottom':'10%','transition':'.2s linear all','opacity':'1'})
        $('#mobNav-support').attr("src","/static/images/mobNav-support-active.svg")
        setTimeout(function () {
            $('#mobNav-support').attr("type","1")
        },300)
    }
    if($('#mobNav-support').attr("type") == 1){
        $('#mobNav-support').attr("src","/static/images/mobNav-support-inactive.svg")
        $('#chatra-wrapper').css({'bottom':'-500px','transition':'.2s linear all','opacity':'1'})
        $('#mobNav-support').attr("type","0")
        setTimeout(function () {
            $('#mobNav-support').attr("type","0")
        },300)
    }
})

$('.desktop-nav').mousemove(function () {
    $(this).addClass('desktop-nav-active')
    $('.desktop-nav-arrow').addClass('desktop-nav-arrow_active')
    $(this).mouseout(function () {
        if($(this).hasClass('disabled')){

        }else {
            $(this).removeClass('desktop-nav-active')
            $('.desktop-nav-arrow').removeClass('desktop-nav-arrow_active')
        }
    })
})
$('.desktop-nav-arrow').click(function () {
    $(this).toggleClass('desktop-nav-arrow_active')
    $('.desktop-nav').toggleClass('desktop-nav-active')
    $('.desktop-nav').toggleClass('disabled')
})