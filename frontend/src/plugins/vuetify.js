// src/plugins/vuetify.js

import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

export default createVuetify({
  components,
  directives,
  theme: {
    // ✅ 'dark'를 'light'로 변경합니다.
    defaultTheme: "light",
  },
  icons: {
    defaultSet: "mdi",
  },
});
