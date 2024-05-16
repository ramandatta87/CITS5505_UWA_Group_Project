$(document).ready(function() {
    function loadPosts() {
        var order = $('#order').val();
        var tag_id = $('#tag_id').val();

        // Make AJAX request
        $.ajax({
            url: "/api/posts",
            data: {
                order: order,
                tag_id: tag_id
            },
            success: function(data) {
                // Clear existing posts
                $('#posts-list').empty();

                // Insert new posts
                data.forEach(function(post) {
                    var postItem = `
                        <li class="list-group-item">
                            <h5><a href="/post/${post.id}">${post.title}</a></h5>
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

    // Load posts on page load
    loadPosts();

    // Trigger AJAX request on change
    $('#order').on('change input', function() {
        loadPosts();
    });
});
