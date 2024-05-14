document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("reply-button").addEventListener("click", function() {
        document.getElementById("reply-form").style.display = "block";
        document.querySelectorAll(".post-buttons").forEach(function(button) {
            button.style.display = "none";
        });
        CKEDITOR.replaceAll('ckeditor');
    });

    document.getElementById("cancel-reply").addEventListener("click", function() {
        document.getElementById("reply-form").style.display = "none";
        document.querySelectorAll(".post-buttons").forEach(function(button) {
            button.style.display = "inline-block";
        });
    });

    document.querySelectorAll(".answer-toggle-button").forEach(function(button) {
        button.addEventListener("click", function() {
            var replyId = this.getAttribute("data-reply-id");
            var action = this.getAttribute("data-action");
            fetch(`/post/toggle_answer/${replyId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                },
                body: JSON.stringify({ action: action })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                   // alert('Action performed successfully.');
                    location.reload();
                } else {
                    // alert('Failed to perform the action.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    document.querySelectorAll(".edit-reply-button").forEach(function(button) {
        button.addEventListener("click", function() {
            var replyId = this.getAttribute("data-reply-id");
            var repliesList = document.getElementById("replies-list");
            var allReplies = repliesList.querySelectorAll(".list-group-item");
            allReplies.forEach(function(reply) {
                if (reply.id !== `reply-${replyId}`) {
                    reply.style.display = "none";
                }
            });

            var replyContent = document.querySelector(`#reply-${replyId} .reply-content`);
            var replyEditForm = document.querySelector(`#reply-${replyId} .reply-edit-form`);
            var replyButtons = document.querySelector(`#reply-${replyId} .reply-buttons`);
            replyContent.style.display = "none";
            replyEditForm.style.display = "block";
            replyButtons.style.display = "none";
            document.getElementById("reply-button").style.display = "none";
            CKEDITOR.replaceAll('ckeditor');
        });
    });

    document.querySelectorAll(".cancel-edit-reply-button").forEach(function(button) {
        button.addEventListener("click", function() {
            var replyId = this.getAttribute("data-reply-id");
            var repliesList = document.getElementById("replies-list");
            var allReplies = repliesList.querySelectorAll(".list-group-item");
            allReplies.forEach(function(reply) {
                reply.style.display = "block";
            });

            var replyContent = document.querySelector(`#reply-${replyId} .reply-content`);
            var replyEditForm = document.querySelector(`#reply-${replyId} .reply-edit-form`);
            var replyButtons = document.querySelector(`#reply-${replyId} .reply-buttons`);
            replyContent.style.display = "block";
            replyEditForm.style.display = "none";
            replyButtons.style.display = "block";
            document.getElementById("reply-button").style.display = "inline-block";
        });
    });

    document.querySelectorAll(".save-reply-button").forEach(function(button) {
        button.addEventListener("click", function() {
            var replyId = this.getAttribute("data-reply-id");
            var newAnswer = CKEDITOR.instances[`edit-answer-${replyId}`].getData();
            fetch(`/post/edit_reply/${replyId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                },
                body: JSON.stringify({ answer: newAnswer })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                   // alert('Reply updated successfully.');
                    location.reload();
                } else {
                    //alert('Failed to update the reply.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
