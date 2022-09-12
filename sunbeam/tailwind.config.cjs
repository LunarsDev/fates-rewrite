module.exports = {
  mode: 'jit',
  corePlugins: {
    preflight: false
  },
  content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/tw-elements/dist/js/**/*.js'],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            '--tw-prose-headings': 'white !important',
            color: 'white !important',
            p: {
              color: 'white !important',
              'margin-top': 0
            },
            pre: {
              color: 'white !important'
            },
            th: 'white !important',
            td: 'white !important',
            table: {
              color: 'white !important',
              'border-color': 'white'
            },
            code: {
              color: 'white !important'
            },
            strong: {
              color: 'white !important'
            },
            a: {
              'font-size': 'initial !important'
            },
            'code::before': {
              content: ''
            },
            'code::after': {
              content: ''
            },
            // Force disable for p
            'p::before': {
              content: "'' !important"
            },
            'p::after': {
              content: "'' !important"
            }
          }
        }
      }
    }
  },
  plugins: [require('@tailwindcss/typography'), require('tw-elements/dist/plugin')]
};
