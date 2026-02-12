/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'simplyfi': {
          'dark-navy': '#001f3f',
          'navy': '#003d7a',
          'light-navy': '#1a5fa0',
          'gold': '#d4af37',
          'light-gold': '#f0d67d',
          'emerald': '#10b981',
          'red-warning': '#ef4444',
          'orange-warning': '#f97316',
          'neutral-bg': '#f8f9fa',
          'border-light': '#e5e7eb',
          'text-dark': '#1f2937',
          'text-muted': '#6b7280',
        },
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 31, 63, 0.05)',
        'base': '0 1px 3px 0 rgba(0, 31, 63, 0.1), 0 1px 2px 0 rgba(0, 31, 63, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 31, 63, 0.1), 0 2px 4px -1px rgba(0, 31, 63, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 31, 63, 0.1), 0 4px 6px -2px rgba(0, 31, 63, 0.05)',
      },
      borderRadius: {
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
      },
      spacing: {
        '3': '0.75rem',
        '4': '1rem',
        '6': '1.5rem',
        '8': '2rem',
        '12': '3rem',
        '16': '4rem',
      },
      opacity: {
        '5': '0.05',
        '10': '0.1',
      },
    },
  },
  plugins: [],
};
