import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from "tailwindcss";


// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss:{
      plugins: [tailwindcss()],
    },
  },
})


//это вставили для того чтобы работал tailwindcss, он еще конфликтует с ant design
// css: {
//     postcss:{
//       plugins: [tailwindcss()],
//     },