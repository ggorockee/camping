import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools(), tailwindcss()],
  server: {
    port: 3000,
    proxy: {
      // '/api'로 시작하는 요청은 모두 target 주소로 전달
      '/api': {
        target: 'http://localhost:8000', // Django 백엔드 서버 주소
        changeOrigin: true, // cross-origin 요청을 위해 필수로 추가
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
