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
        primary: '#2563eb',         // Deeper blue
        secondary: '#60a5fa',       // Light blue
        tertiary: '#bfdbfe',        // Very light blue
        background: '#f8fafc',      // Light background
        success: '#10b981',         // Green
        danger: '#ef4444',          // Red
        warning: '#f59e0b',         // Amber
      },
      boxShadow: {
        'card': '0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03)',
        'card-hover': '0 20px 25px -5px rgba(0, 0, 0, 0.07), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      },
    },
  },
  plugins: [],
} 