<script setup>
import { RouterLink } from "vue-router";
import { useAuthStore } from "@/stores/auth"; // 1. Pinia 스토어 import

const authStore = useAuthStore(); // 2. 스토어 인스턴스 생성

// 로그아웃 버튼 클릭 시 스토어의 logout 액션을 호출하고, 홈 경로를 전달합니다.
function handleLogout() {
  authStore.logout("/");
}
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-light bg-white absolute-top">
      <div class="container">
        <!-- 왼쪽 메뉴 (데스크탑용) -->
        <div
          class="collapse navbar-collapse order-3 order-md-2"
          id="navbar-left"
        ></div>

        <!-- 중앙 로고 -->
        <RouterLink class="navbar-brand mx-auto order-1 order-md-3" to="/">
          ggorockee
        </RouterLink>

        <!-- 모바일 메뉴 토글 버튼 (추가된 부분) -->
        <button
          class="navbar-toggler order-2"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbar-right"
          aria-controls="navbar-right"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- 오른쪽 메뉴 (모바일에서 숨겨질 부분) -->
        <div
          class="collapse navbar-collapse order-4 order-md-4"
          id="navbar-right"
        >
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Contact</a>
            </li>

            <!-- 로그인/아웃 상태에 따른 UI 분기 -->
            <template v-if="!authStore.isAuthenticated">
              <li class="nav-item">
                <RouterLink to="/register" class="nav-link"
                  >Register</RouterLink
                >
              </li>
              <li class="nav-item">
                <RouterLink to="/login" class="nav-link">Login</RouterLink>
              </li>
            </template>

            <!-- 로그인 되었을 때 -->
            <template v-else>
              <li class="nav-item">
                <a class="nav-link" href="#">
                  Welcome, {{ authStore.username }}
                </a>
              </li>
              <li class="nav-item">
                <a href="#" class="nav-link" @click.prevent="handleLogout"
                  >Logout</a
                >
              </li>
            </template>
          </ul>

          <form class="form-inline" role="search"></form>
        </div>
      </div>
    </nav>
  </header>
</template>

<style scoped>
/* 헤더에만 적용되는 스타일이 있다면 여기에 추가 */
.nav-link {
  cursor: pointer;
}
</style>