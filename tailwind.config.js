/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#10B981', // Green color
        'primary-dark': '#059669',
        'primary-light': '#34D399',
        'background': '#0F172A', // Dark blue background
        'background-light': '#1E293B',
        'text-primary': '#F3F4F6',
        'text-secondary': '#9CA3AF',
        'accent': '#8B5CF6', // Purple accent
        'accent-light': '#A78BFA',
        'danger': '#EF4444',
        'warning': '#F59E0B',
        'success': '#10B981',
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-roboto-mono)', 'monospace'],
      },
      keyframes: {
        shimmer: {
          '0%': {
            backgroundPosition: '-1000px 0',
          },
          '100%': {
            backgroundPosition: '1000px 0',
          },
        },
        glow: {
          '0%, 100%': {
            boxShadow: '0 0 5px rgba(16, 185, 129, 0.6), 0 0 10px rgba(16, 185, 129, 0.4)',
          },
          '50%': {
            boxShadow: '0 0 15px rgba(16, 185, 129, 0.8), 0 0 20px rgba(16, 185, 129, 0.6)',
          },
        },
        float: {
          '0%, 100%': {
            transform: 'translateY(0)',
          },
          '50%': {
            transform: 'translateY(-10px)',
          },
        },
      },
      animation: {
        shimmer: 'shimmer 2s infinite linear',
        glow: 'glow 2s infinite ease-in-out',
        float: 'float 3s infinite ease-in-out',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'shimmer-gradient': 'linear-gradient(to right, transparent, rgba(16, 185, 129, 0.1), transparent)',
      },
      boxShadow: {
        'glow-sm': '0 0 5px rgba(16, 185, 129, 0.6)',
        'glow-md': '0 0 10px rgba(16, 185, 129, 0.6)',
        'glow-lg': '0 0 15px rgba(16, 185, 129, 0.6)',
      },
    },
  },
  plugins: [],
}