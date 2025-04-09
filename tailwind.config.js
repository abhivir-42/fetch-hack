/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1a73e8',
        secondary: '#7b61ff',
        background: '#f5f7fa',
        success: '#34c759',
        danger: '#ff3b30',
        warning: '#ffcc00',
      },
    },
  },
  plugins: [],
} 