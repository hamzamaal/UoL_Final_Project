document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll('.stat-number');
    const duration = 2000; // Animation duration in milliseconds
  
    counters.forEach(counter => {
      const isCurrency = counter.getAttribute('data-target').includes('.');
      const target = parseFloat(counter.getAttribute('data-target'));
      const startTime = performance.now();
  
      const updateCount = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const value = target * progress;
  
        if (isCurrency) {
          counter.innerText = 'R' + value.toFixed(2);
        } else {
          counter.innerText = Math.floor(value).toLocaleString();
        }
  
        if (progress < 1) {
          requestAnimationFrame(updateCount);
        } else {
          counter.innerText = isCurrency ? 'R' + target.toFixed(2) : target.toLocaleString();
        }
      };
  
      requestAnimationFrame(updateCount);
    });
  });
  