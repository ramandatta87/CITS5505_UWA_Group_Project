$(document).ready(function() {
    function loadPosts() {
        // Get form values
        var order = $('#order').val();

        // Determine the URL to make the AJAX request based on the current page
        var url = window.location.pathname.includes('my_answers') ? "/api/my_answers_posts" : "/api/posts";

        // Make AJAX request
        $.ajax({
            url: url,
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
                            <p>${post.content}</p>
                            ${post.answered ? '<p><strong>Answered</strong></p>' : ''}
                            <p><strong>${post.career_preparation ? 'Career Preparation' : 'Unit'}</strong></p>
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
    $('#order').on('change', function() {
        loadPosts();
    });
});
