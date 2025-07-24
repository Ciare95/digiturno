import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000', // Cambia el puerto si tu backend usa otro
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
})
