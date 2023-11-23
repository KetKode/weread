$(document).ready(function() {
    $(document).on('click', '.like-button', function(event) {
        event.preventDefault();
        var likeButton = $(this);
        var snippetId = likeButton.data('snippet-id');
        var likeUrl = likeButton.data('like-url');
        var likeCountElement = likeButton.find('.like-count');

        $.ajax({
            type: 'POST',
            url: likeUrl,
            data: {
                snippet_id: snippetId
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data) {
                console.log('Liked successfully');

                // Update the like count in the UI for the specific snippet
                var newLikeCount = data.like_count;

                // Toggle heart icon classes
                likeButton.find('i').toggleClass('fa-regular fa-solid');

                // Update like count text
                likeCountElement.text(newLikeCount);
            },
            error: function(error) {
                console.error('Error occurred while liking:', error);
            }
        });
    });
});
