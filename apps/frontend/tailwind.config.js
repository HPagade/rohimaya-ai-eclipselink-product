/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // EclipseLink AI Brand Colors (Rohimaya branding)
        'peacock-teal': {
          50: '#e6f7f5',
          100: '#ccefeb',
          200: '#99dfd7',
          300: '#66cfc3',
          400: '#33bfaf',
          500: '#1a9b8e',  // Primary
          600: '#157c71',
          700: '#105d54',
          800: '#0a3e38',
          900: '#051f1c',
        },
        'phoenix-gold': {
          50: '#fef9e6',
          100: '#fdf3cc',
          200: '#fbe799',
          300: '#f9db66',
          400: '#f7cf33',
          500: '#f4c430',  // Accent
          600: '#c39d26',
          700: '#92761d',
          800: '#624e13',
          900: '#31270a',
        },
        'lunar-blue': {
          50: '#e8ebee',
          100: '#d1d7dd',
          200: '#a3afbb',
          300: '#758799',
          400: '#475f77',
          500: '#2c3e50',  // Text/Dark
          600: '#233240',
          700: '#1a2530',
          800: '#121920',
          900: '#090c10',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'medium': '0 4px 16px rgba(0, 0, 0, 0.12)',
        'large': '0 8px 32px rgba(0, 0, 0, 0.16)',
      },
    },
  },
  plugins: [],
}
