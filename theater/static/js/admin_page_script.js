//$(document).ready(function() {
//    $('.statistics').show();
//
//    $('.admin-menu li').on('click', function() {
//
//        var targetBlock = $(this).data('content');
//        $('.' + targetBlock).show().siblings('.hide').hide();
//        $(this).addClass('active');
//        $('.admin-menu li').not(this).removeClass('active');
//    });
//});

$(document).ready(function() {
    // Detach the recommendations block by default
    var recommendations = $('.recommendations').detach();

    $('.admin-menu li').on('click', function() {
        var targetBlock = $(this).data('content');

        // Detach the current visible block
        if ($('.statistics').is(':visible')) {
            $('.statistics').detach();
        } else {
            $('.recommendations').detach();
        }

        // Append the target block
        if (targetBlock === 'statistics') {
            $('.admin-content').append($('.statistics'));
        } else if (targetBlock === 'recommendations') {
            $('.admin-content').append(recommendations);
        }

        // Add active class to clicked menu item
        $(this).addClass('active');

        // Remove active class from other menu items
        $('.admin-menu li').not(this).removeClass('active');
    });
});