document.addEventListener('DOMContentLoaded', () => {
  const menu = document.getElementById('mobileMenu');
  const toggleButton = document.getElementById('toggleMenu');

  toggleButton.addEventListener('click', () => {
    if (menu.classList.contains('max-h-0')) {
      menu.classList.remove('max-h-0');
      menu.classList.add('max-h-[500px]');
    } else {
      menu.classList.add('max-h-0');
      menu.classList.remove('max-h-[500px]');
    }
  });

    document.querySelector('.scroll-to-top').addEventListener('click', function (e) {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });






});
