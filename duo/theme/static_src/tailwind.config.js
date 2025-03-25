/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
         '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
         '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
     theme: {
        extend: {
          keyframes: {
            fadeIn: {
              '0%': { opacity: 0 },
              '100%': { opacity: 1 },
            },
            slideInRight: {
              '0%': { transform: 'translateX(100%)', opacity: 0 },
              '100%': { transform: 'translateX(0)', opacity: 1 },
            },
            slideInLeft: {
              '0%': { transform: 'translateX(-100%)', opacity: 0 },
              '100%': { transform: 'translateX(0)', opacity: 1 },
            },
            slideUp: {
              '0%': { transform: 'translateY(100%)', opacity: 0 },
              '100%': { transform: 'translateY(0)', opacity: 1 },
            },
            scaleUp: {
              '0%': { transform: 'scale(0)', opacity: 0 },
              '100%': { transform: 'scale(1)', opacity: 1 },
            },
          },
          animation: {
            // Fade-In variations
            'fade-in-fast': 'fadeIn 0.5s ease-in-out forwards',
            'fade-in-medium': 'fadeIn 1s ease-in-out forwards',
            'fade-in-slow': 'fadeIn 1.5s ease-in-out forwards',

            // Slide-In Right variations
            'slide-in-right-fast': 'slideInRight 0.5s ease-out forwards',
            'slide-in-right-medium': 'slideInRight 1s ease-out forwards',
            'slide-in-right-slow': 'slideInRight 1.5s ease-out forwards',

            // Slide-In Left variations
            'slide-in-left-fast': 'slideInLeft 0.5s ease-out forwards',
            'slide-in-left-medium': 'slideInLeft 1s ease-out forwards',
            'slide-in-left-slow': 'slideInLeft 1.5s ease-out forwards',

            // Slide-Up variations
            'slide-up-fast': 'slideUp 0.5s ease-out forwards',
            'slide-up-medium': 'slideUp 1s ease-out forwards',
            'slide-up-slow': 'slideUp 1.5s ease-out forwards',

            // Scale-Up variations
            'scale-up-fast': 'scaleUp 0.5s ease-out forwards',
            'scale-up-medium': 'scaleUp 1s ease-out forwards',
            'scale-up-slow': 'scaleUp 1.5s ease-out forwards',
          },
          fontFamily: {
            serif: ['Playfair Display', 'serif'],
            sans: ['Poppins', 'sans-serif'],
          },
        },
      },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
