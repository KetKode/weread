const gap = 10;

const carousel = document.querySelectorAll(".carousel");
const content = document.querySelectorAll(".carousel-content");
const next = document.querySelectorAll(".next");
const prev = document.querySelectorAll(".prev");

for (let i = 0; i < carousel.length; i++) {
  let width = content[i].offsetWidth;
  let scrollAmount = 0;
  let maxScroll = carousel[i].scrollWidth - width;

  next[i].addEventListener("click", () => {
    if (scrollAmount < maxScroll) {
      scrollAmount += width;
      carousel[i].scrollTo({
        top: 0,
        left: scrollAmount,
        behavior: "smooth"
      });
    }
  });

  prev[i].addEventListener("click", () => {
    if (scrollAmount > 0) {
      scrollAmount -= width;
      carousel[i].scrollTo({
        top: 0,
        left: scrollAmount,
        behavior: "smooth"
      });
    }
  });

  // Adjust carousel width when the window is resized
  window.addEventListener("resize", () => {
    width = content[i].offsetWidth;
    maxScroll = carousel[i].scrollWidth - width;

    // Ensure scrollAmount does not exceed the new maxScroll value after resizing
    if (scrollAmount > maxScroll) {
      scrollAmount = maxScroll;
      carousel[i].scrollTo({
        top: 0,
        left: scrollAmount,
        behavior: "auto"
      });
    }
  });
}

