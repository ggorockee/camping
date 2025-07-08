<script setup>
import { RouterView } from "vue-router";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import AppHeader from "@/components/AppHeader.vue";

const authStore = useAuthStore();

onMounted(() => {
  // 앱이 마운트될 때 액세스 토큰이 있으면 사용자 정보를 가져옵니다.
  if (authStore.accessToken) {
    authStore.fetchUser();
  }
});
</script>

<template>
  <v-app>
    <!-- 헤더 컴포넌트 -->
    <app-header />

    <!-- 페이지 컨텐츠가 표시되는 메인 영역 -->
    <v-main>
      <router-view />
    </v-main>

    <!-- ✅ 로그인 시 항상 표시되는 전역 플로팅 버튼 -->
    <v-btn
      v-if="authStore.isAuthenticated"
      :to="{ name: 'campsite-create' }"
      icon="mdi-plus"
      size="x-large"
      elevation="8"
      aria-label="새 캠핑장 등록"
      class="fab-plus"
    ></v-btn>

    <v-footer class="d-flex flex-column pa-0" app>
      <div class="px-4 py-2 bg-black text-center w-100 text-caption">
        &copy; {{ new Date().getFullYear() }} Milo 2022, All rights reserved
      </div>
    </v-footer>
  </v-app>
</template>

<style scoped>
/* ✅ 플로팅 버튼을 위한 전용 스타일 */
.fab-plus {
  position: fixed;
  /* --v-footer-height: Vuetify가 자동으로 계산하는 푸터의 높이 변수입니다.
    calc() 함수를 사용해 푸터 높이 + 0.5rem 만큼 위로 띄웁니다.
  */
  bottom: calc(var(--v-footer-height, 48px) + 0.5rem);
  right: 0.5rem;

  /* 테마와 어울리는 색상 및 호버 효과 */
  background-color: #6c757d; /* 회색 배경 */
  color: white;
}

.fab-plus:hover {
  background-color: #5a6268; /* 호버 시 약간 더 어두운 회색 */
}
</style>
