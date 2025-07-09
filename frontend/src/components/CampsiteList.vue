<template>
  <!-- 화면이 전체일 때 좌우 여백 확보를 위한 반응형 패딩 추가 -->
  <div class="container mx-auto px-4 mt-6">
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <Campsite v-for="c in campsites" :key="c.id" :campsite="c" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import Campsite from '@/components/Campsite.vue'
import apiClient from '@/api'
import type { ICampsite, ICampsiteResponse } from '@/types/api'

const campsites = ref<ICampsite[]>([])

const fetchCampsites = async (): Promise<void> => {
  try {
    // define response type
    const response = await apiClient.get<ICampsiteResponse>('/campsites/')
    campsites.value = response.data.results
  } catch (error: unknown) {
    console.error('캠핑장 데이터를 불러오는 중 오류가 발생:', error)
  }
}

onMounted(fetchCampsites)

// const props = defineProps<{ items: CardItem[] }>()
</script>

<style scoped>
/* aspect-square 사용을 위해 @tailwindcss/aspect-ratio 플러그인 활성화 필요 */
</style>
