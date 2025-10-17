window.addEventListener("DOMContentLoaded", () => {
  const parallaxContainer = document.querySelector(".parallax");

  // Create an image element
  const image = new Image();
  image.src = "Images/minh-pham-IisDPFNUS4k-unsplash 3.JPG";
  image.classList.add("parallax-image");
  parallaxContainer.appendChild(image);

  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;
    // Adjust the image's position for parallax effect
    image.style.transform = `translateY(${scrollY * 0.5}px)`;
  });
});