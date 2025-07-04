import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// 우리의 메인 SCSS 파일 하나만 남겨둡니다.
import "./assets/scss/milo.scss";
import "bootstrap"; // 이 라인을 추가!

const app = createApp(App);

app.use(router);

app.mount("#app");
