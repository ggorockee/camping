<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { render } from 'timeago.js'
import type { ICampsiteListItem } from '@/types/api' // Campsite 인터페이스 경로
import { RouterLink } from 'vue-router'

// Prop 타입 안전성 확보
const props = defineProps<{ campsite: ICampsiteListItem }>()

/**
 * 날짜 범위를 규칙에 따라 포맷팅하는 computed 속성
 */
const formattedDateRange = computed(() => {
  // 날짜 데이터가 없으면 빈 문자열 반환
  if (!props.campsite.check_in || !props.campsite.check_out) {
    return ''
  }

  const startDate = new Date(props.campsite.check_in)
  const endDate = new Date(props.campsite.check_out)

  const startYear = startDate.getFullYear()
  const startMonth = startDate.toLocaleString('en-US', { month: 'short' }) // 'Jun'
  const startDay = startDate.getDate()

  const endYear = endDate.getFullYear()
  const endMonth = endDate.toLocaleString('en-US', { month: 'short' }) // 'Jun'
  const endDay = endDate.getDate()

  // 1. 연도가 다른 경우
  if (startYear !== endYear) {
    return `${startMonth} ${startDay}, ${startYear} - ${endMonth} ${endDay}, ${endYear}`
  }

  // 2. 월이 다른 경우
  if (startMonth !== endMonth) {
    return `${startMonth} ${startDay} - ${endMonth} ${endDay}`
  }

  // 3. 연도와 월이 모두 같은 경우
  return `${startMonth} ${startDay} - ${endDay}`
})

// timeago용 element 레퍼런스
const timeagoElement = ref<HTMLElement | null>(null)

onMounted(() => {
  if (timeagoElement.value) {
    render(timeagoElement.value)
  }
})

const imageSrc = computed(() => props.campsite.thumbnail_url || '/img/articles/2.jpg')
const title = computed(() => props.campsite.name)

const formattedPrice = computed(() => {
  const priceNumber = Number(props.campsite.price)
  // price가 숫자가 아닐 경우 '0' 또는 다른 기본값 반환
  if (isNaN(priceNumber)) {
    return '0'
  }
  // 'ko-KR' 로케일 기준으로 숫자 형식 변환 (예: 120000 -> "120,000")
  return priceNumber.toLocaleString('ko-KR')
})
const nights = computed(() => props.campsite.stay_nights)
</script>

<template>
  <RouterLink :to="{ name: 'campsite-detail', params: { id: campsite.id } }">
    <div class="relative rounded-lg overflow-hidden bg-white shadow mb-4">
      <!-- 이미지 (정사각 유지) -->
      <div class="relative w-full aspect-square">
        <img :src="imageSrc" :alt="title" class="absolute inset-0 w-full h-full object-cover" />
      </div>
      <!-- 텍스트 영역 -->
      <div class="px-2 py-3">
        <h3 class="text-sm font-medium text-gray-900 truncate">{{ title }}</h3>
        <p class="text-xs text-gray-500 mt-1 truncate">{{ formattedDateRange }}</p>
        <p class="text-sm font-semibold text-gray-900 mt-1">
          ₩{{ formattedPrice }} · {{ nights }}박
        </p>
      </div>
    </div>
  </RouterLink>
</template>

<style scoped>
/* aspect-square 사용을 위해 @tailwindcss/aspect-ratio 플러그인 활성화 필요 */
</style>
