import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    port: 3000, // 포트를 3000으로 지정
    proxy: {
      // '/api'로 시작하는 요청은 모두 target 주소로 전달됩니다.
      "/api": {
        target: "http://localhost:8000", // Django 백엔드 서버 주소
        changeOrigin: true, // cross-origin 요청을 위해 필수로 추가
      },
    },
  },
});
