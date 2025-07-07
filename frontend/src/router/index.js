import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterView from "../views/RegisterView.vue";
import LoginView from "@/views/LoginView.vue";
import CampsiteCreate from "@/components/CampsiteCreate.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/campsites/new", // 접속할 URL 경로
      name: "campsite-create", // 이 라우트의 고유한 이름
      component: CampsiteCreate, // 이 경로와 연결될 컴포넌트
      meta: { requiresAuth: true }, // ✨ (보안 강화) 이 페이지는 로그인이 필요함을 명시
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
  ],
});

// ✨ (보안 강화) 로그인 유무에 따른 라우트 접근 제어 (Navigation Guard)
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem("accessToken"); // 간단한 로그인 확인 예시

  if (to.meta.requiresAuth && !isLoggedIn) {
    // 로그인이 필요한 페이지에 비로그인 상태로 접근 시 로그인 페이지로 리디렉션
    alert("로그인이 필요합니다.");
    next({ name: "login" }); // 'login'은 로그인 페이지 라우트의 이름
  } else {
    // 그 외의 경우는 정상적으로 페이지 이동
    next();
  }
});

export default router;
