$(document).ready(function() {
    

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
