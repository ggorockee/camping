<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api'
import type { ICampsiteDetail } from '@/types/api'

// 1. 라우트 정보에 접근하기 위해 useRoute 훅 사용
const route = useRoute()
const campsite = ref<ICampsiteDetail | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// --- 이미지 갤러리 상태 ---
const mainImage = ref<string>('')

// // 썸네일 캐러셀을 위한 상태 추가
const thumbnailStartIndex = ref(1) // 썸네일은 전체 이미지 배열의 1번 인덱스부터 시작

const accountHash = import.meta.env.VITE_CLOUDFLARE_ACCOUNT_HASH
const publicVariant = import.meta.env.VITE_CLOUDFLARE_IMAGE_VARIANT || 'public'

// Cloudflare 이미지 URL을 생성하는 헬퍼 함수
const getImageUrl = (imageId: string, variant: string = publicVariant) => {
  if (!accountHash) {
    console.error('Cloudflare Account Hash가 .env 파일에 설정되지 않았습니다.')
    return ''
  }

  return `https://imagedelivery.net/${accountHash}/${imageId}/${variant}`
}

// 이미지 URL 목록을 미리 계산하는 computed 속성
const imageUrls = computed(() => {
  if (!campsite.value || !campsite.value.images) {
    return []
  }
  return campsite.value.images.map((image) => getImageUrl(image.cloudflare_id))
})

// 현재 보여줄 썸네일 4개를 계산하는 computed 속성
const visibleThumbnails = computed(() => {
  // slice(시작 인덱스, 끝 인덱스)를 동적으로 계산
  return imageUrls.value.slice(thumbnailStartIndex.value, thumbnailStartIndex.value + 4)
})

// 이전/다음 버튼 표시 여부를 결정하는 computed 속성
const showPrevButton = computed(() => {
  // 이미지가 5개 초과이고, 시작 인덱스가 1보다 클 때만 '이전' 버튼 표시
  return imageUrls.value.length > 5 && thumbnailStartIndex.value > 1
})

const showNextButton = computed(() => {
  // 현재 썸네일의 마지막 위치 + 1이 전체 이미지 수보다 작을 때만 '다음' 버튼 표시
  return imageUrls.value.length > 5 && thumbnailStartIndex.value + 4 < imageUrls.value.length
})

// 썸네일 네비게이션 함수
const nextThumbnails = () => {
  if (showNextButton.value) {
    thumbnailStartIndex.value++
  }
}

const prevThumbnails = () => {
  if (showPrevButton.value) {
    thumbnailStartIndex.value--
  }
}

// --- 데이터 로딩 ---
const fetchCampsite = async () => {
  // URL 파라미터에서 id를 가져옴 (예: /campsites/1 -> '1')
  const campsiteId = route.params.id

  try {
    const response = await apiClient.get<ICampsiteDetail>(`/campsites/${campsiteId}/`)
    campsite.value = response.data
    // 갤러리의 메인 이미지를 첫 번째 이미지로 초기화
    if (imageUrls.value.length > 0) {
      mainImage.value = imageUrls.value[0]
    }
  } catch (err) {
    console.error('캠핑장 상세 정보를 불러오는 중 오류 발생!!:', err)
    error.value = '데이터를 불러오는 데 실패했군!!.'
  } finally {
    loading.value = false
  }
}

// --- 헬퍼 함수 ---
const formatTime = (timeStr: string) => timeStr.substring(0, 5)

// 3. 컴포넌트가 마운트될 때 데이터 요청 함수 실행
onMounted(fetchCampsite)
</script>

<template>
  <div class="bg-gray-50 font-sans">
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <p class="text-lg text-gray-600">데이터를 불러오는 중입니다...</p>
    </div>
    <div v-else-if="error" class="min-h-screen flex items-center justify-center">
      <p class="text-lg text-red-500">{{ error }}</p>
    </div>

    <div v-else-if="campsite" class="container mx-auto max-w-6xl py-12 px-4 mt-16">
      <header class="mb-8">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900">{{ campsite.name }}</h1>
        <div class="mt-4 flex items-center space-x-4 text-gray-600">
          <span class="flex items-center">
            <svg class="w-5 h-5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
              ></path>
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
              ></path>
            </svg>
            {{ campsite.address }}
          </span>
          <span class="flex items-center">
            <svg class="w-5 h-5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              ></path>
            </svg>
            by {{ campsite.owner }}
          </span>
        </div>
      </header>

      <section v-if="imageUrls.length" class="mb-10">
        <div class="w-full space-y-2">
          <div class="rounded-xl overflow-hidden shadow-lg">
            <img
              :src="mainImage"
              alt="Main campsite view"
              class="w-full aspect-video object-cover"
            />
          </div>

          <div class="flex items-center space-x-2">
            <button
              v-if="showPrevButton"
              @click="prevThumbnails"
              class="flex-shrink-0 p-2 rounded-full bg-white/50 hover:bg-white/80 transition-colors shadow"
            >
              <svg
                class="w-6 h-6 text-gray-700"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 19l-7-7 7-7"
                ></path>
              </svg>
            </button>

            <div class="flex-grow grid grid-cols-2 md:grid-cols-4 gap-2">
              <div
                v-for="imageUrl in visibleThumbnails"
                :key="imageUrl"
                class="group relative rounded-xl overflow-hidden shadow-lg cursor-pointer"
                @click="mainImage = imageUrl"
              >
                <img
                  :src="imageUrl"
                  alt="Thumbnail view"
                  class="w-full h-32 md:h-40 object-cover transition-transform duration-300 group-hover:scale-110"
                />
                <div
                  class="absolute inset-0 bg-black/0 transition-all duration-300 group-hover:bg-black/40"
                ></div>
                <div
                  class="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity duration-300 group-hover:opacity-100"
                >
                  <svg
                    class="w-10 h-10 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                    />
                  </svg>
                </div>
              </div>
            </div>

            <button
              v-if="showNextButton"
              @click="nextThumbnails"
              class="flex-shrink-0 p-2 rounded-full bg-white/50 hover:bg-white/80 transition-colors shadow"
            >
              <svg
                class="w-6 h-6 text-gray-700"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </section>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10"></div>
    </div>
  </div>
</template>

<style scoped></style>
