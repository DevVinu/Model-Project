/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        neu: {
          light: '#e8ecf4',
          lightSurface: '#f1f5fa',
          dark: '#1c2028',
          darkSurface: '#242934',
        },
        highlight: {
          green: '#10b981',
          yellow: '#f59e0b',
          red: '#ef4444',
          blue: '#3b82f6',
          purple: '#8b5cf6',
        }
      },
      boxShadow: {
        // Light Neumorphism (White/Black theme)
        'neu-flat': '7px 7px 15px #c8d0dd, -7px -7px 15px #ffffff',
        'neu-flat-sm': '4px 4px 8px #c8d0dd, -4px -4px 8px #ffffff',
        'neu-pressed': 'inset 4px 4px 8px #c8d0dd, inset -4px -4px 8px #ffffff',
        'neu-pressed-sm': 'inset 2px 2px 5px #c8d0dd, inset -2px -2px 5px #ffffff',
        
        // Dark Neumorphism
        'neu-dark-flat': '7px 7px 15px #14171d, -7px -7px 15px #242933',
        'neu-dark-flat-sm': '4px 4px 8px #14171d, -4px -4px 8px #242933',
        'neu-dark-pressed': 'inset 4px 4px 8px #14171d, inset -4px -4px 8px #242933',
      }
    },
  },
  plugins: [],
}
