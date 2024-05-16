$(document).ready(function() {
    function loadPosts() {
        // Get the selected order value
        var order = $('#order').val();

        // Make AJAX request
        $.ajax({
            url: "/api/posts",
            data: {
                order: order
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
                            <p>${post.career_preparation ? 'Career Preparation' : 'Unit'}</p>
                            ${post.answered ? '<p>Answered</p>' : ''}
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

    // Trigger AJAX request on order change
    $('#order').on('change', function() {
        loadPosts();
    });
});
