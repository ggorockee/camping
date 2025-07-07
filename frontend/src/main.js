import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

import vuetify from "./plugins/vuetify"; // ✅ 1. vuetify 플러그인 import
import "./assets/css/global.css"; // ✅ 2. 전역 CSS import

// 우리의 메인 SCSS 파일 하나만 남겨둡니다.
import "./assets/scss/milo.scss";
import "bootstrap"; // 이 라인을 추가!

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(vuetify);

app.mount("#app");
