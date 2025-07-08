// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx,css}', // 이 라인이 핵심!
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
