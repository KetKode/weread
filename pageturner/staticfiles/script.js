$(document).ready(function() {
    $('.like-button').on('click', function(event) {
        event.preventDefault(); // Prevent the default behavior of the anchor tag

        var snippetId = $(this).data('snippet-id');

        // Send an AJAX request to the server
        $.ajax({
            type: 'POST', // or 'GET' depending on your server-side handling
            url: 'snippet_like/<int:pk>', // Specify the URL for your like endpoint
            data: {
                snippet_id: snippetId
            },
            success: function(data) {
                // Handle the success response if needed
                console.log('Liked successfully');
            },
            error: function(error) {
                // Handle the error response if needed
                console.error('Error occurred while liking:', error);
            }
        });
    });
});
