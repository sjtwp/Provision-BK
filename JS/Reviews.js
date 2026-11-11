// Client reviews carousel. Used on the home page and the service area pages.
// Add new Google reviews to the list below. Only 5-star reviews are shown.
(function () {
  // Add new Google reviews here. Only 5-star reviews are shown.
  const reviews = [
    {
      rating: 5,
      name: "Kristin R.",
      business: "",
      text: "I highly recommend Matthew! He is incredibly knowledgeable, efficient, and detail-oriented. He's professional, responsive, and always takes the time to explain things clearly. His expertise has been a tremendous asset to my businesses and I truly appreciate his attention to detail and dedication."
    },
    {
      rating: 5,
      name: "Kristen P.",
      business: "Kristen's Skin Studio",
      text: "Highly recommend Provision Bookkeeping LLC services. I came to Matt with a mess of a situation and he is amazing, very thorough, timely and an absolute pleasure to work with. Always understanding, patient and more than helpful to me to understand the process. I had deadlines that needed to be met and he was calm, and generous with his time. Matt is very professional, attention to detail but also just a very easy, nice, and kind person to work with. I feel lucky that I was referred to Matt and I now feel confident that my bookkeeping is done promptly and correctly and I'm in good hands. Thank you for your exemplary services!"
    },
    {
      rating: 5,
      name: "Adam D.",
      business: "",
      text: "I highly recommend Provision Bookkeeping and especially Matthew for his outstanding service. Matthew's expertise and deep knowledge were evident throughout the entire process. He worked quickly and efficiently while maintaining exceptional attention to detail, ensuring everything was accurate and well-organized. What impressed me most was his responsiveness, professionalism, and ability to handle complex bookkeeping tasks with confidence."
    },
    {
      rating: 5,
      name: "Adrian D.",
      business: "Southwest Defense LLC",
      text: "Matthew does a great job doing Southwest Defense LLC bookkeeping! He is always detail oriented and very timely getting his reports to you. Matthew has been a breath of fresh air compared to previous bookkeepers!"
    }
  ].filter(function (r) { return r.rating === 5; });

  const track = document.getElementById('reviews-track');
  if (!track) return;
  const dotsBox = document.getElementById('reviews-dots');
  const carousel = track.closest('.reviews-carousel');
  let index = 0;
  let timer = null;

  function esc(t) {
    const d = document.createElement('div');
    d.textContent = t;
    return d.innerHTML;
  }

  reviews.forEach(function (r, i) {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.setAttribute('role', 'group');
    card.setAttribute('aria-label', 'Review ' + (i + 1) + ' of ' + reviews.length);
    card.innerHTML =
      '<div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>' +
      '<blockquote>&ldquo;' + esc(r.text) + '&rdquo;</blockquote>' +
      '<div class="reviewer">' + esc(r.name) +
      (r.business ? ' <span class="reviewer-biz">&middot; ' + esc(r.business) + '</span>' : '') + '</div>' +
      '<div class="source">Google review</div>';
    track.appendChild(card);

    const dot = document.createElement('button');
    dot.type = 'button';
    dot.setAttribute('aria-label', 'Show review ' + (i + 1));
    dot.addEventListener('click', function () { go(i); restart(); });
    dotsBox.appendChild(dot);
  });

  function go(i) {
    index = (i + reviews.length) % reviews.length;
    track.style.transform = 'translateX(-' + (index * 100) + '%)';
    Array.prototype.forEach.call(dotsBox.children, function (d, j) {
      d.classList.toggle('active', j === index);
    });
  }

  function restart() {
    clearInterval(timer);
    timer = setInterval(function () { go(index + 1); }, 8000);
  }

  carousel.querySelector('.prev').addEventListener('click', function () { go(index - 1); restart(); });
  carousel.querySelector('.next').addEventListener('click', function () { go(index + 1); restart(); });
  carousel.addEventListener('mouseenter', function () { clearInterval(timer); });
  carousel.addEventListener('mouseleave', restart);

  // Swipe on phones
  let startX = null;
  track.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
  track.addEventListener('touchend', function (e) {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 40) { go(dx < 0 ? index + 1 : index - 1); restart(); }
    startX = null;
  });

  go(0);
  restart();
})();
