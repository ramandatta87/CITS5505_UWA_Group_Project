$(document).ready(function() {
    if ($.ui) {
        console.log("jQuery UI is loaded: ", $.ui);
    } else {
        console.error("jQuery UI is not loaded");
    }

    $('#autocomplete').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/autocomplete',
                data: {
                    term: request.term
                },
                dataType: 'json',
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 1
    });
});
