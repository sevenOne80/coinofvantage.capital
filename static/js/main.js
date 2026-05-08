// CoinOfVantage — front-end interactions
(function () {
  'use strict';

  // Reveal-on-scroll for .fade-in elements
  if ('IntersectionObserver' in window) {
    const els = document.querySelectorAll('.fade-in');
    els.forEach((el) => {
      el.style.animationPlayState = 'paused';
      el.style.opacity = '0';
    });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.animationPlayState = 'running';
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach((el) => io.observe(el));
  }

  // Subtle nav shadow on scroll
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 8) {
        nav.style.boxShadow = '0 6px 20px -12px rgba(4,36,26,0.18)';
      } else {
        nav.style.boxShadow = 'none';
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Auto-dismiss flash messages after 5s
  document.querySelectorAll('.flash').forEach((flash) => {
    setTimeout(() => {
      flash.style.transition = 'opacity .4s ease, transform .4s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateX(20px)';
      setTimeout(() => flash.remove(), 400);
    }, 5000);
  });
})();
