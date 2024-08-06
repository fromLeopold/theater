$(document).ready(function() {
    $('.actors').show();

    $('.troupe-menu li').on('click', function() {
//        alert("Функция вызвана!");
        var targetBlock = $(this).data('content');
        $('.' + targetBlock).show().siblings('.hide').hide();
        $(this).addClass('active');
        $('.troupe-menu li').not(this).removeClass('active');
    });
});
