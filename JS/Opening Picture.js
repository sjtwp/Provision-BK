window.addEventListener("DOMContentLoaded", () => {
  const parallaxContainer = document.querySelector(".parallax");

  // Create an image element
  const image = new Image();
  const isMobile = window.innerWidth <= 768; // Check mobile at load

  // Set image source based on device
  image.src = isMobile 
    ? "Images/minh-pham-IisDPFNUS4k-unsplash 4.jpg" // New photo for mobile
    : "Images/minh-pham-IisDPFNUS4k-unsplash 3.JPG"; // Original for desktop
  image.classList.add("parallax-image");
  parallaxContainer.appendChild(image);

  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;
    const speed = isMobile ? 0.5 : 0.5; // 0.5 = slow on mobile, 0.5 = normal on desktop
    
    // Adjust the image's position for parallax effect
    image.style.transform = `translateY(${scrollY * speed}px)`;
  });

  // Update on resize (e.g., orientation change)
  window.addEventListener("resize", () => {
    const newIsMobile = window.innerWidth <= 768;
    if (newIsMobile !== isMobile) {
      // Reload image if device type changes
      image.src = newIsMobile 
        ? "Images/minh-pham-IisDPFNUS4k-unsplash 4.jpg"
        : "Images/minh-pham-IisDPFNUS4k-unsplash 3.JPG";
    }
    window.dispatchEvent(new Event('scroll'));
  });
});