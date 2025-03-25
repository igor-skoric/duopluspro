document.addEventListener('DOMContentLoaded', function () {
  const elements = document.querySelectorAll('[class*="on-scroll"], .count-up-on-scroll');

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.remove('opacity-0');

        // Dodaj animaciju na osnovu klase
        if (entry.target.classList.contains('fade-in-fast-on-scroll')) {
          entry.target.classList.add('animate-fade-in-fast');
        } else if (entry.target.classList.contains('fade-in-medium-on-scroll')) {
          entry.target.classList.add('animate-fade-in-medium');
        } else if (entry.target.classList.contains('fade-in-slow-on-scroll')) {
          entry.target.classList.add('animate-fade-in-slow');
        } else if (entry.target.classList.contains('slide-in-right-fast-on-scroll')) {
          entry.target.classList.add('animate-slide-in-right-fast');
        } else if (entry.target.classList.contains('slide-in-right-medium-on-scroll')) {
          entry.target.classList.add('animate-slide-in-right-medium');
        } else if (entry.target.classList.contains('slide-in-right-slow-on-scroll')) {
          entry.target.classList.add('animate-slide-in-right-slow');
        } else if (entry.target.classList.contains('slide-in-left-fast-on-scroll')) {
          entry.target.classList.add('animate-slide-in-left-fast');
        } else if (entry.target.classList.contains('slide-in-left-medium-on-scroll')) {
          entry.target.classList.add('animate-slide-in-left-medium');
        } else if (entry.target.classList.contains('slide-in-left-slow-on-scroll')) {
          entry.target.classList.add('animate-slide-in-left-slow');
        } else if (entry.target.classList.contains('slide-up-fast-on-scroll')) {
          entry.target.classList.add('animate-slide-up-fast');
        } else if (entry.target.classList.contains('slide-up-medium-on-scroll')) {
          entry.target.classList.add('animate-slide-up-medium');
        } else if (entry.target.classList.contains('slide-up-slow-on-scroll')) {
          entry.target.classList.add('animate-slide-up-slow');
        } else if (entry.target.classList.contains('scale-up-fast-on-scroll')) {
          entry.target.classList.add('animate-scale-up-fast');
        } else if (entry.target.classList.contains('scale-up-medium-on-scroll')) {
          entry.target.classList.add('animate-scale-up-medium');
        } else if (entry.target.classList.contains('scale-up-slow-on-scroll')) {
          entry.target.classList.add('animate-scale-up-slow');
        }

        // Ako element ima klasu za brojanje, pokreni brojanje
        if (entry.target.classList.contains('count-up-on-scroll')) {
          const targetValue = parseInt(entry.target.getAttribute('data-target'));
          animateNumber(entry.target, targetValue, 2000); // 2 sekunde
        }

        observer.unobserve(entry.target); // Zaustavi praćenje ovog elementa
      }
    });
  }, { threshold: 0.5 });

  // Počni da pratiš sve elemente
  elements.forEach(element => {
    observer.observe(element);
  });

  // Funkcija za animaciju brojeva
  function animateNumber(element, target, duration) {
    let current = 0;
    let increment = target / (duration / 50); // Brzina inkrementa

    const interval = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(interval);
      }
      element.innerText = Math.floor(current); // Postavljanje broja u HTML
    }, 50); // Svakih 50ms
  }


// **NOVI KOD - Pokretanje fade-in-fast odmah**
  const loadElements = document.querySelectorAll('.fade-in-fast-on-load');

  loadElements.forEach(element => {
    element.classList.remove('opacity-0');
    element.classList.add('animate-fade-in-fast');
  });





});
