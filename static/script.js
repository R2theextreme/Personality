$(document).ready(function() {
    $('.tag').click(function() {
        $('.tag').removeClass('selected');
        $(this).addClass('selected');
        $('.personality-content').hide();  // Hide all personality contents
        var personality = $(this).data('personality');
        $('#' + personality + '-content').fadeIn();  // Show the selected personality content
    });
});
