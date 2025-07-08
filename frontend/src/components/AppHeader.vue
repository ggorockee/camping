<template>
  <header
    class="fixed top-0 left-0 w-full bg-white px-6 py-4 flex items-center justify-between shadow-md z-50"
  >
    <!-- Left: 메뉴 버튼 + 이름 -->
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
      <span class="text-gray-800 font-bold text-xl">ggorockee</span>
    </div>

    <!-- Right: Login, Sign up 버튼 -->
    <div class="flex items-center space-x-4 px-8">
      <button
        class="px-4 py-2 rounded-full border border-gray-800 text-gray-800 text-sm font-medium hover:bg-gray-100 transition"
      >
        Login
      </button>
      <button
        class="px-4 py-2 rounded-full bg-black text-white text-sm font-medium hover:bg-gray-800 transition"
      >
        Sign up
      </button>
    </div>

    <!-- Slide-out 메뉴 -->
    <transition name="slide">
      <nav
        v-if="menuOpen"
        class="fixed inset-y-0 left-0 w-80 bg-white shadow-lg z-40 flex flex-col overflow-y-auto"
      >
        <div class="p-6">
          <!-- Close Button -->
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
          <!-- Top Buttons: Sign up & Login -->
          <div class="flex flex-col space-y-4">
            <button
              class="w-full px-4 py-2 rounded-full bg-black text-white text-center font-medium"
            >
              Sign up
            </button>
            <button
              class="w-full px-4 py-2 rounded-full border border-gray-800 text-gray-800 text-center font-medium"
            >
              Login
            </button>
          </div>
        </div>
        <!-- Bottom Buttons: iPhone & Android -->
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

    <!-- Overlay with slight blur and light opacity -->
    <div v-if="menuOpen" @click="toggleMenu" class="fixed inset-0 bg-black/65 z-30"></div>
    <div class="fixed bottom-6 right-6 z-50">
      <button
        @click="true"
        class="w-14 h-14 rounded-full bg-black/75 text-white text-3xl leading-none flex items-center justify-center shadow-lg hover:bg-gray-800 transition"
      >
        <span class="relative -top-0.5">+</span>
      </button>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const menuOpen = ref(false)
function toggleMenu() {
  menuOpen.value = !menuOpen.value
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
