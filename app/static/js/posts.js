function loadPosts() {
    // Get form values
    var filter_by = $('#filter_by').val();
    var filter_value = $('#filter_value').val();
    var order = $('#order').val();
    
    // Make AJAX request
    $.ajax({
        url: "/api/posts",
        data: {
            filter_by: filter_by,
            filter_value: filter_value,
            order: order
        },
        success: function(data) {
            // Clear existing posts
            $('#posts-list').empty();
            
            // Insert new posts
            data.forEach(function(post) {
                var postItem = `
                    <li class="list-group-item">
                        <h5>${post.title}</h5>
                        <p>by ${post.author_first_name} ${post.author_last_name} on ${post.date_posted}</p>
                        <p>Tag: ${post.tag}</p>
                        <p>${post.content}</p>
                    </li>
                `;
                $('#posts-list').append(postItem);
            });
        }
    });
}

$(document).ready(function() {
    // Load posts on page load
    loadPosts();

    // Trigger AJAX request on change
    $('#filter_by, #filter_value, #order').on('change input', function() {
        loadPosts();
    });

    // Autocomplete for filter value
    $('#filter_value').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api/autocomplete_posts",
                data: {
                    q: request.term,
                    filter_by: $('#filter_by').val()
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 1
    });
});