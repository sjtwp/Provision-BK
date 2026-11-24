window.addEventListener("DOMContentLoaded", () => {
  const parallaxContainer = document.querySelector(".parallax");
  if (!parallaxContainer) return;

  // Use the hero image already in the page (home page), or add it (other pages)
  let image = parallaxContainer.querySelector(".parallax-image");
  if (!image) {
    image = new Image();
    image.src = "/Images/hero-office.webp";
    image.srcset = "/Images/hero-office-960.webp 960w, /Images/hero-office.webp 1920w";
    image.sizes = "100vw";
    image.alt = "";
    image.decoding = "async";
    image.classList.add("parallax-image");
    parallaxContainer.prepend(image);
  }

  // Gentle parallax on scroll (moves only, no zoom); skipped for reduced-motion users
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const handleScroll = () => {
    const speed = window.innerWidth <= 768 ? 0.25 : 0.5;
    image.style.transform = `translate3d(0, ${window.scrollY * speed}px, 0)`;
  };
  window.addEventListener("scroll", handleScroll, { passive: true });
  window.addEventListener("resize", handleScroll);
});
