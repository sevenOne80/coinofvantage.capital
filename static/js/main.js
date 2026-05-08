// Intersection Observer for fade-in animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.fade-in').forEach(el => {
  el.style.animationPlayState = 'paused';
  observer.observe(el);
});

// Auto-hide flash messages
document.querySelectorAll('.flash').forEach(flash => {
  setTimeout(() => {
    flash.style.transition = 'opacity .4s';
    flash.style.opacity = '0';
    setTimeout(() => flash.remove(), 400);
  }, 4000);
});
