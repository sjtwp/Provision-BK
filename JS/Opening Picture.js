window.addEventListener("DOMContentLoaded", () => {
  const parallaxContainer = document.querySelector(".parallax");

  // Create an image element
  const image = new Image();
  let isMobile = window.innerWidth <= 768; // detect at load

  // Use same image for both
  image.src = "../Images/minh-pham-IisDPFNUS4k-unsplash 3.JPG";
  image.classList.add("parallax-image");
  parallaxContainer.appendChild(image);

  // Parallax scroll effect (only moves, no scale)
  const handleScroll = () => {
    const scrollY = window.scrollY;
    const speed = isMobile ? 0.25 : 0.5; // slower movement on mobile
    image.style.transform = `translate3d(0, ${scrollY * speed}px, 0)`; // ✅ No scale, no zoom
  };

  window.addEventListener("scroll", handleScroll);

  // Update on resize (orientation changes)
  window.addEventListener("resize", () => {
    const newIsMobile = window.innerWidth <= 768;
    if (newIsMobile !== isMobile) {
      isMobile = newIsMobile;
      handleScroll();
    }
  });

  window.addEventListener("scroll", () => {
  const scrollY = window.scrollY;
  const speed = window.innerWidth <= 768 ? 0.25 : 0.5;
  image.style.transform = `translateY(${scrollY * speed}px)`; // ✅ no scaling
});


});
