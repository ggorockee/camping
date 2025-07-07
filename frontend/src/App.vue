<script setup>
import { RouterView } from "vue-router";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import Header from "@/components/AppHeader.vue";

const authStore = useAuthStore();

// 2. 앱이 처음 로드될 때 실행
onMounted(() => {
  // localStorage에 저장된 토큰이 있다면,
  // 해당 토큰으로 사용자 정보를 다시 불러와서 로그인 상태를 유지합니다.
  if (authStore.accessToken) {
    authStore.fetchUser();
  }
});
</script>

<template>
  <!-- 3. 헤더 컴포넌트 사용 -->
  <Header />

  <!-- 페이지 컨텐츠가 렌더링되는 부분 -->
  <RouterView />

  <!-- 푸터는 그대로 유지 -->
  <footer class="site-footer bg-dark">
    <div class="container">
      <ul class="nav justify-content-center">
        <li class="nav-item">
          <a class="nav-link" href="#">Privacy policy</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Terms</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Feedback</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Advertise</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Contact</a>
        </li>
      </ul>
      <div class="copy">
        &copy; Milo 2022<br />
        All rights reserved
      </div>
    </div>
  </footer>
</template>

<style scoped>
/* App.vue에만 필요한 스타일이 있다면 여기에 유지 */
</style>
