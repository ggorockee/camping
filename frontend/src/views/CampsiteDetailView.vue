<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api'
import type { ICampsite } from '@/types/api'

// 1. 라우트 정보에 접근하기 위해 useRoute 훅 사용
const route = useRoute()
const campsite = ref<ICampsite | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// 2. 단일 캠핑장 데이터를 불러오는 함수
const fetchCampsite = async () => {
  // URL 파라미터에서 id를 가져옴 (예: /campsites/1 -> '1')
  const campsiteId = route.params.id

  try {
    const response = await apiClient.get<ICampsite>(`/campsites/${campsiteId}/`)
    campsite.value = response.data
  } catch (err) {
    console.error('캠핑장 상세 정보를 불러오는 중 오류 발생!!:', err)
    error.value = '데이터를 불러오는 데 실패했군!!.'
  } finally {
    loading.value = false
  }
}

// 3. 컴포넌트가 마운트될 때 데이터 요청 함수 실행
onMounted(fetchCampsite)
</script>

<template>
  <main class="pt-24 px-6">
    <div v-if="loading" class="text-center">
      <p>데이터를 불러오는 중입니다...</p>
    </div>

    <div v-else-if="error" class="text-center text-red-500">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="campsite">
      <h1 class="text-4xl font-bold">{{ campsite.name }}</h1>
    </div>
  </main>
</template>
