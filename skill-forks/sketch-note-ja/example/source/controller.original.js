const slides = document.querySelectorAll('.slide');
  const counter = document.getElementById('counter');
  let current = 0;
  const total = slides.length;

  function go(idx) {
    if (idx < 0 || idx >= total) return;
    slides[current].classList.remove('active');
    current = idx;
    slides[current].classList.add('active');
    counter.textContent = `${current + 1} / ${total}`;
  }

  document.getElementById('prev').addEventListener('click', () => go(current - 1));
  document.getElementById('next').addEventListener('click', () => go(current + 1));

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
      e.preventDefault();
      go(current + 1);
    }
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      go(current - 1);
    }
    if (e.key === 'Home') go(0);
    if (e.key === 'End') go(total - 1);
  });

  // Touch swipe support
  let touchStartX = 0;
  document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
  document.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) {
      if (dx < 0) go(current + 1);
      else go(current - 1);
    }
  });
