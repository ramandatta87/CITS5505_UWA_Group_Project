$(document).ready(function() {
    function loadPosts(page = 1) {
        // Get the selected order value
        var order = $('#order').val();

        // Make AJAX request
        $.ajax({
            url: "/api/posts",
            data: {
                order: order,
                page: page
            },
            success: function(data) {
                // Clear existing posts
                $('#posts-list').empty();

                // Insert new posts
                data.posts_data.forEach(function(post) {
                    var postItem = `
                        <li class="list-group-item">
                            <h5><a href="/post/${post.id}">${post.title}</a></h5>
                            <p><strong>Tag:</strong> <span class="tagnew">${post.tag}</span></p>
                            <p>${post.career_preparation ? '<span class="career">Career Preparation</span>' : '<span class="unit">Unit</span>'}</p>
                            ${post.answered ? '<p>Answered</p>' : ''}
                            <p>${post.content}</p>
                            <p><strong>Author:</strong> <span class="authorpost">${post.author_first_name} ${post.author_last_name}</span></p>
                            <p><strong>Created on:</strong> ${post.date_posted}</p>
                        </li>
                    `;
                    $('#posts-list').append(postItem);
                });

                // Clear existing pagination
                $('.pagination').remove();

                // Update pagination
                var pagination = `
                    <nav aria-label="Page navigation">
                        <ul class="pagination justify-content-center">
                            ${page > 1 ? `<li class="page-item"><a class="page-link" href="#" aria-label="Previous" data-page="${page - 1}"><span aria-hidden="true">&laquo;</span></a></li>` : '<li class="page-item disabled"><a class="page-link" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'}
                            ${data.has_next ? `<li class="page-item"><a class="page-link" href="#" aria-label="Next" data-page="${page + 1}"><span aria-hidden="true">&raquo;</span></a></li>` : '<li class="page-item disabled"><a class="page-link" href="#"
