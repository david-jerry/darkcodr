/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    darkMode: 'class',
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
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            screens: {
                "xs": '475px',
                ...defaultTheme.screens
            },
            fontFamily: {
                "raleway": ["'Raleway'", "Be Vietnam Pro", "sans-serif"],
                "cursive": ["'Poiret One'", "cursive"],
            },
            colors: {
                "black": "#1a1a1a",
                "dark": "#10192A",
                "light": "#e2e2e2",
                "primary": "#A82DCA",
                "secondary": "#03C7F7",
                "anchor": "#E3AEF2",
                "variant-1": "#CAA04B",
                "variant-2":"#E5AB8B",
            },
            transitionTimingFunction: {
                'in-expo': 'cubic-bezier(0.95, 0.05, 0.795, 0.035)',
                'out-expo': 'cubic-bezier(0.19, 1, 0.22, 1)',
                'menu': 'cubic-bezier(.84,.06,.52,1.8)',
            },
            keyframes: {
                wiggle: {
                    '0%, 100%': { transform: 'rotate(-3deg)' },
                    '50%': { transform: 'rotate(3deg)' },
                },
                slideIn: {
                    '0%': {width: '0%'},
                    '20%': {width: '30%'},
                    '50%': {width: '10%'},
                    '100%': {width: '25%'},
                },
                slideOut: {
                    '0%': {width: '20%'},
                    '50%': {width: '30%'},
                    '100%': {width: '0%'},
                },
                shotUp: {
                    '0%': {transform: 'translateY(300%)', opacity: 0},
                    '90%': {transform: 'translateY(-50px)'},
                    '100%': {transform: 'translateY(0%)', opacity: 1},
                },
                transformMenu1: {
                    '0%': {transform: 'translateY(-12px)'},
                    '100%': {transform: 'translateY(0px)'},
                },
                transformMenu2: {
                    '0%': {width: '100%'},
                    '100%': {width: '0%'},
                },
                transformMenu3: {
                    '0%': {transform: 'translateY(12px)'},
                    '100%': {transform: 'translateY(0px)'},
                },
            },
            animation: {
                wiggle: 'wiggle 1s ease-in-out infinite',
                'wiggle-slow': 'wiggle 3s linear infinite',
                'ping-slow': 'ping 1s linear infinite',
                'ping-slower': 'ping 2s linear infinite',
                'bounce-slow': 'bounce 3s linear infinite',
                'slide-in': 'slideIn 1s ease-in-out',
                'slide-out': 'slideOut 1s linear',
                'slide-in-slow': 'slideIn 3s linear',
                'shot-up': 'shotUp linear',
                'shot-up-slow': 'shotUp 3s linear',
                'transform-menu1': 'transformMenu1 400ms',
                'transform-menu2': 'transformMenu2 400ms',
                'transform-menu3': 'transformMenu3 400ms',
            }
        },
    },
    variants: {
        extend: {},
        scrollBar: ["rounded"],
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('tailwind-scrollbar-hide'),
        require('tailwind-scrollbar')
    ],
}
