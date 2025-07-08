<template>
  <!-- 화면이 전체일 때 좌우 여백 확보를 위한 반응형 패딩 추가 -->
  <div class="container mx-auto px-4">
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div
        v-for="(item, index) in items"
        :key="index"
        class="relative rounded-lg overflow-hidden bg-white shadow"
      >
        <!-- 이미지 (정사각 유지) -->
        <div class="relative w-full aspect-square">
          <img
            :src="item.imageSrc"
            :alt="item.title"
            class="absolute inset-0 w-full h-full object-cover"
          />
          <div
            v-if="item.guestPreferred"
            class="absolute top-2 left-2 bg-white bg-opacity-75 text-xs font-medium px-2 py-0.5 rounded-full"
          >
            게스트 선호
          </div>
          <button
            class="absolute top-2 right-2 p-1 bg-white bg-opacity-75 rounded-full hover:bg-opacity-100 transition"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5 text-gray-800"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5.121 19.364l-.707-.707a4 4 0 015.657-5.657L12 14.586l2.929-2.929a4 4 0 015.657 5.657l-.707.707a8 8 0 01-11.314 0z"
              />
            </svg>
          </button>
        </div>
        <!-- 텍스트 영역 -->
        <div class="px-2 py-3">
          <h3 class="text-sm font-medium text-gray-900 truncate">{{ item.title }}</h3>
          <p class="text-xs text-gray-500 mt-1 truncate">{{ item.dateRange }}</p>
          <p class="text-sm font-semibold text-gray-900 mt-1">
            {{ item.price }} · {{ item.nights }}박 · ★ {{ item.rating }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineProps } from 'vue'

export interface CardItem {
  imageSrc: string
  title: string
  dateRange: string
  price: string
  nights: number
  rating: number
  guestPreferred?: boolean
}

const props = defineProps<{ items: CardItem[] }>()
</script>

<style scoped>
/* aspect-square 사용을 위해 @tailwindcss/aspect-ratio 플러그인 활성화 필요 */
</style>
