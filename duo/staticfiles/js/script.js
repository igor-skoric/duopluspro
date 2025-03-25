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
});
