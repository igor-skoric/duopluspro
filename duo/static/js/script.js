document.addEventListener('DOMContentLoaded', () => {

  const menu = document.getElementById('mobileMenu');
  const contact = document.getElementById('contact');
  const toggleButton = document.getElementById('toggleMenu');

  toggleButton.addEventListener('click', () => {
    if (menu.classList.contains('max-h-0')) {
        menu.classList.remove('max-h-0');
        menu.classList.add('max-h-[500px]');
        if (contact === "" || contact === null || contact === undefined) {
//            console.log("Contact is empty");

        } else {
            // The contact is not empty
            contact.classList.toggle('-translate-y-36');
            contact.classList.toggle('duration-400');
        }
    } else {
        menu.classList.add('max-h-0');
        menu.classList.remove('max-h-[500px]');
        if (contact === "" || contact === null || contact === undefined) {

        } else {
            // The contact is not empty
            contact.classList.toggle('-translate-y-36');
        }

    }
  });

});
