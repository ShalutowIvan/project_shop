/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  corePlugins:{
    preflight: false // <== disable this. Это чтобы не было конфликтов tailwindCSS с ant design
  },
}