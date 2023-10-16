
document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll('.star-rating span');

    stars.forEach((star, index) => {
        star.addEventListener('mouseover', () => {
            resetStars();
            for (let i = 0; i <= index; i++) {
                stars[i].classList.add('checked');
            }
        });

        star.addEventListener('click', () => {
            const ratingField = document.getElementById('id_rating');
            ratingField.value = index + 1;
        });

        star.addEventListener('mouseout', () => {
            resetStars();
        });
    });

    function resetStars() {
        stars.forEach(star => {
            star.classList.remove('checked');
        });
    }
});
