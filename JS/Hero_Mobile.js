// Home page hero on phones: keep the headline below the fixed header,
// and hide the floating Call Now button while the quote form is on screen.
(function () {
  function setHeaderHeight() {
    var header = document.querySelector('header');
    if (header) {
      document.documentElement.style.setProperty('--hdr', header.offsetHeight + 'px');
    }
  }

  function watchForm() {
    var form = document.querySelector('.hero-form');
    if (!form || !('IntersectionObserver' in window)) return;
    document.body.classList.add('hero-in-view');
    new IntersectionObserver(function (entries) {
      document.body.classList.toggle('hero-in-view', entries[0].isIntersecting);
    }).observe(form);
  }

  function init() {
    setHeaderHeight();
    watchForm();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  window.addEventListener('load', setHeaderHeight);
  window.addEventListener('resize', setHeaderHeight);
})();
