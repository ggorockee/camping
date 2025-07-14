<template>
  <header
    class="fixed top-0 left-0 w-full bg-white px-6 py-4 flex items-center justify-between shadow-md z-50"
  >
    <div class="flex items-center space-x-4">
      <button @click="toggleMenu" class="focus:outline-none">
        <svg class="w-6 h-6 text-gray-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
      <RouterLink to="/" class="text-gray-800 font-bold text-xl"> ggorockee </RouterLink>
    </div>

    <div class="flex items-center space-x-6 px-8">
      <div v-if="isLoggedIn" class="flex items-center space-x-4">
        <span class="text-gray-800 font-medium hidden sm:block">{{ username }}님</span>
        <button
          @click="handleLogout"
          class="flex items-center space-x-1.5 text-gray-500 hover:text-gray-900 transition"
          aria-label="Logout"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          <span class="text-sm font-medium">Logout</span>
        </button>
      </div>

      <div v-else class="flex items-center space-x-4">
        <RouterLink
          to="/login"
          class="px-4 py-2 rounded-full border border-gray-800 text-gray-800 text-sm font-medium hover:bg-gray-100 transition"
        >
          Login
        </RouterLink>

        <RouterLink
          to="/register"
          class="px-4 py-2 rounded-full bg-black text-white text-sm font-medium hover:bg-gray-800 transition"
        >
          Sign up
        </RouterLink>
      </div>
    </div>

    <transition name="slide">
      <nav
        v-if="menuOpen"
        class="fixed inset-y-0 left-0 w-80 bg-white shadow-lg z-40 flex flex-col overflow-y-auto"
      >
        <div class="p-6">
          <button @click="toggleMenu" class="mb-6 focus:outline-none">
            <svg
              class="w-6 h-6 text-gray-800"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <div v-if="isLoggedIn" class="flex flex-col space-y-4">
            <div class="text-left p-4 rounded-lg bg-gray-50 border">
              <p class="font-bold text-lg text-gray-900">{{ username }}님</p>
              <p class="text-sm text-gray-500">{{ authStore.user?.email }}</p>
            </div>
            <button
              @click="handleLogout"
              class="w-full px-4 py-3 rounded-full bg-gray-800 text-white text-center font-medium hover:bg-black transition"
            >
              로그아웃
            </button>
          </div>

          <div v-else class="flex flex-col space-y-4">
            <RouterLink
              to="/register"
              @click="toggleMenu"
              class="w-full px-4 py-2 rounded-full bg-black text-white text-center font-medium"
            >
              Sign up
            </RouterLink>
            <RouterLink
              to="/login"
              @click="toggleMenu"
              class="w-full px-4 py-2 rounded-full border border-gray-800 text-gray-800 text-center font-medium"
            >
              Login
            </RouterLink>
          </div>
        </div>
        <div class="mt-auto p-6">
          <div class="flex flex-row space-x-4">
            <button
              class="flex-1 py-2 px-4 bg-gray-100 rounded-lg flex items-center justify-center space-x-2"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" stroke="none">
                <path d="M16 2H8a4 4 0 00-4 4v12a4 4 0 004 4h8a4 4 0 004-4V6a4 4 0 00-4-4z" />
              </svg>
              <span>iPhone</span>
            </button>
            <button
              class="flex-1 py-2 px-4 bg-gray-100 rounded-lg flex items-center justify-center space-x-2"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" stroke="none">
                <path
                  d="M17 8h2a1 1 0 011 1v11a1 1 0 01-1 1h-2m-10 0H5a1 1 0 01-1-1V9a1 1 0 011-1h2"
                />
                <circle cx="8" cy="4" r="1" />
                <circle cx="16" cy="4" r="1" />
              </svg>
              <span>Android</span>
            </button>
          </div>
        </div>
      </nav>
    </transition>

    <div v-if="menuOpen" @click="toggleMenu" class="fixed inset-0 bg-black/65 z-30"></div>
    <div class="fixed bottom-6 right-6 z-50">
      <RouterLink
        to="/new"
        class="w-14 h-14 rounded-full bg-black/75 text-white text-3xl leading-none flex items-center justify-center shadow-lg hover:bg-gray-800 transition"
        ><span class="relative -top-0.5">+</span></RouterLink
      >
    </div>
  </header>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore' // Pinia 스토어 import

// Pinia 스토어 및 라우터 사용
const authStore = useAuthStore()

// 메뉴 상태 관리
const menuOpen = ref(false)
function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

// ⭐️ [수정] 스토어의 isAuthenticated를 직접 사용하도록 변경
const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.username) // 스토어의 username 사용

// 로그아웃 처리 함수
async function handleLogout() {
  if (menuOpen.value) {
    toggleMenu()
  }
  // ⭐️ [수정] 컴포넌트에서 alert 제거 (스토어에서 이미 처리)
  await authStore.logout()
  // 스토어의 logout 함수가 리디렉션까지 처리하므로 여기서는 추가 작업 불필요
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
.slide-enter-to,
.slide-leave-from {
  transform: translateX(0);
}
</style>
