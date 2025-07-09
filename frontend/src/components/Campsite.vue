<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { render } from 'timeago.js'
import type { ICampsite } from '@/types/api' // Campsite 인터페이스 경로

// Prop 타입 안전성 확보
const props = defineProps<{ campsite: ICampsite }>()

// timeago용 element 레퍼런스
const timeagoElement = ref<HTMLElement | null>(null)

onMounted(() => {
  if (timeagoElement.value) {
    render(timeagoElement.value)
  }
})

const imageSrc = computed(() => props.campsite.thumbnail_url || '/img/articles/2.jpg')
const title = computed(() => props.campsite.name)
const dateRange = computed(() => `${props.campsite.check_in} ~ ${props.campsite.check_out}`)
const price = computed(() => props.campsite.price)
const nights = computed(() => props.campsite.stay_nights)
</script>

<template>
  <div class="relative rounded-lg overflow-hidden bg-white shadow mb-4">
    <!-- 이미지 (정사각 유지) -->
    <div class="relative w-full aspect-square">
      <img :src="imageSrc" :alt="title" class="absolute inset-0 w-full h-full object-cover" />
    </div>
    <!-- 텍스트 영역 -->
    <div class="px-2 py-3">
      <h3 class="text-sm font-medium text-gray-900 truncate">{{ title }}</h3>
      <p class="text-xs text-gray-500 mt-1 truncate">{{ dateRange }}</p>
      <p class="text-sm font-semibold text-gray-900 mt-1">\{{ price }} · {{ nights }}박</p>
    </div>
  </div>
</template>

<style scoped>
/* aspect-square 사용을 위해 @tailwindcss/aspect-ratio 플러그인 활성화 필요 */
</style>
