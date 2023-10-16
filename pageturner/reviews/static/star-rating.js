document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const ratingInput = document.getElementById("id_rating");
    console.log(ratingInput);

    stars.forEach((star, index) => {
        star.addEventListener("click", () => {
            // Set the value of the hidden input field to the selected rating
            ratingInput.value = index + 1;
            console.log("Rating set:", ratingInput.value);

            // Reset all stars to inactive state
            stars.forEach((star, index2) => {
                star.classList.remove("active");
                if (index2 <= index) {
                    star.classList.add("active");
                }
            });
        });
    });
});
