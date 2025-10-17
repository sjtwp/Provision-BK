window.addEventListener("DOMContentLoaded", () => {
  const parallaxContainer = document.querySelector(".parallax");

  // Create an image element
  const image = new Image();
  image.src = "Images/minh-pham-IisDPFNUS4k-unsplash 3.JPG";
  image.classList.add("parallax-image");
  parallaxContainer.appendChild(image);

  // Function to check if device is mobile
  function isMobile() {
    return window.innerWidth <= 768; // Adjust breakpoint as needed (768px = tablet, 480px = phone)
  }

  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;
    const speed = isMobile() ? 0.05 : 0.5; // 0.05 = half speed on mobile, 0.5 = normal on desktop
    
    // Adjust the image's position for parallax effect
    image.style.transform = `translateY(${scrollY * speed}px)`;
  });

  // Also check on resize (for orientation changes)
  window.addEventListener("resize", () => {
    // Trigger scroll event to update immediately
    window.dispatchEvent(new Event('scroll'));
  });
});