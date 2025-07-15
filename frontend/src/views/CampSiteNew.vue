<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/index'
import type { IAmenity, ISite, IPricingRule, IImageFile } from '@/types/api'

// --- 2. 상수 및 기본 데이터 ---
const router = useRouter()
const weekDays = [
  { label: '일', val: '0' },
  { label: '월', val: '1' },
  { label: '화', val: '2' },
  { label: '수', val: '3' },
  { label: '목', val: '4' },
  { label: '금', val: '5' },
  { label: '토', val: '6' },
]

// --- 3. 반응형 상태 (Reactive State) ---
const campsiteData = reactive({
  name: '',
  address: '',
  description: '',
  price: null,
  contact_number: '',
  check_in: '',
  check_out: '',
  layout_image_url: '',
})
const policy = reactive({
  check_in_time: '15:00',
  check_out_time: '11:00',
  manner_time_start: '22:00',
  manner_time_end: '07:00',
})
const sites = ref<ISite[]>([])
const pricingRules = ref<IPricingRule[]>([])
const allAmenities = ref<IAmenity[]>([])
const selectedAmenities = ref<number[]>([])
const images = ref<IImageFile[]>([])
const isLoading = ref(false)
const errorMessage = ref('')
const isDragOver = ref(false)
const dateError = ref('')
// --- 4. 로직 (함수) ---

const fetchAmenities = async () => {
  try {
    const response = await apiClient.get<IAmenity[]>('/amenities/')
    allAmenities.value = response.data
  } catch (error) {
    console.error('편의시설 목록 로딩 실패:', error)
  }
}

// 동적 리스트 관리
const addSite = () =>
  sites.value.push({ id: Date.now(), name: '', camp_type: '오토캠핑', base_price: '0' })
const removeSite = (index: number) => sites.value.splice(index, 1)
const addRule = () =>
  pricingRules.value.push({
    id: Date.now(),
    name: '',
    start_date: '',
    end_date: '',
    day_of_week: [],
    extra_charge: null,
  })
const removeRule = (index: number) => pricingRules.value.splice(index, 1)

// 파일 핸들링
const addFiles = (files: FileList) => {
  Array.from(files).forEach((file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      images.value.push({
        id: Date.now() + Math.random(),
        file: file,
        previewSrc: e.target?.result as string,
        status: 'pending',
        progress: 0,
      })
    }
    reader.readAsDataURL(file)
  })
}
const handleFileSelect = (event: Event) => addFiles((event.target as HTMLInputElement).files!)
const removeImage = (id: number) => {
  images.value = images.value.filter((img) => img.id !== id)
}
const drop = (event: DragEvent) => {
  isDragOver.value = false
  addFiles(event.dataTransfer!.files)
}

// 유효성 검사
const isFormValid = computed(() => {
  return (
    campsiteData.name.trim() !== '' &&
    campsiteData.address.trim() !== '' &&
    images.value.length >= 1
  )
})

const validateDates = () => {
  // 체크인과 체크아웃 날짜가 모두 선택되었는지 확인
  if (campsiteData.check_in && campsiteData.check_out) {
    const checkInDate = new Date(campsiteData.check_in)
    const checkOutDate = new Date(campsiteData.check_out)

    if (checkOutDate < checkInDate) {
      dateError.value = '체크아웃 날짜는 체크인 날짜보다 빠를 수 없습니다.'
    } else {
      dateError.value = '' // 오류가 없으면 메시지 초기화
    }
  }
}

// 폼 제출 (성공했던 로직 적용)
const createCampsite = async () => {
  if (!isFormValid.value) {
    errorMessage.value = '캠핑장 이름, 주소, 그리고 최소 1개 이상의 이미지는 필수입니다.'
    return
  }
  errorMessage.value = ''
  isLoading.value = true

  try {
    const token = localStorage.getItem('accessToken')
    if (!token) throw new Error('인증 토큰이 없습니다. 로그인 후 이용해주세요.')

    // 1. 업로드할 이미지들에 대한 URL 요청
    const pendingImages = images.value.filter((img) => img.status === 'pending')
    const urlPromises = pendingImages.map(() =>
      apiClient
        .post<{ id: string; uploadURL: string }>(
          '/campsites/images/upload-url/',
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        )
        .then((res) => res.data),
    )
    const urlResults = await Promise.all(urlPromises)

    // 2. 발급받은 URL로 각 이미지 파일 업로드
    const uploadPromises = pendingImages.map((image, index) => {
      image.status = 'uploading'
      const formData = new FormData()
      formData.append('file', image.file)
      // fetch를 사용해 직접 업로드 (CORS 설정 필요)
      return fetch(urlResults[index].uploadURL, {
        method: 'POST',
        body: formData,
      })
        .then((res) => {
          if (res.ok) {
            image.status = 'success'
            image.progress = 100
            image.cloudflareId = urlResults[index].id
          } else {
            image.status = 'error'
            throw new Error(`'${image.file.name}' 이미지 업로드 실패`)
          }
        })
        .catch((err) => {
          image.status = 'error'
          throw err
        })
    })
    await Promise.all(uploadPromises)

    if (images.value.some((img) => img.status === 'error')) {
      throw new Error(
        '일부 이미지 업로드에 실패했습니다. 실패한 이미지를 삭제 후 다시 시도해주세요.',
      )
    }

    // 3. 모든 정보 최종 제출
    const finalPayload = {
      ...campsiteData,
      policy: { ...policy },
      sites: [...sites.value],
      amenities: [...selectedAmenities.value],
      pricing_rules: pricingRules.value.map((r) => ({
        ...r,
        day_of_week: r.day_of_week.join(','),
      })),
      image_ids: images.value.map((img) => img.cloudflareId),
    }

    await apiClient.post('/campsites/', finalPayload, {
      headers: { Authorization: `Bearer ${token}` },
    })

    alert('🎉 캠핑장이 성공적으로 등록되었습니다!')
    router.push({ name: 'home' })
  } catch (error: any) {
    errorMessage.value = error.message
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchAmenities)
</script>

<template>
  <div class="bg-gray-50 font-sans">
    <div class="container mx-auto max-w-5xl py-12 px-4 mt-12">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-gray-900">캠핑 후기 등록</h1>
        <p class="mt-4 text-lg text-gray-600">다녀오신 캠핑장의 정보를 상세히 기록해주세요.</p>
      </div>

      <form @submit.prevent="createCampsite" class="space-y-10">
        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">🏕️ 기본 정보</h2>
          <p class="text-gray-600 mb-6">캠핑을 다녀온 경험을 바탕으로 정보를 입력해주세요.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input
              v-model="campsiteData.name"
              type="text"
              placeholder="캠핑장 이름"
              class="input-new-field"
              required
            />
            <input
              v-model="campsiteData.address"
              type="text"
              placeholder="주소"
              class="input-new-field"
              required
            />
            <div class="md:col-span-2">
              <textarea
                v-model="campsiteData.description"
                rows="4"
                placeholder="캠핑장 설명 (특징, 주변 경관 등)"
                class="input-new-field"
              ></textarea>
            </div>
            <input
              v-model.number="campsiteData.price"
              type="number"
              placeholder="총 숙박 요금 (원)"
              class="input-new-field"
              required
            />
            <input
              v-model="campsiteData.contact_number"
              type="tel"
              placeholder="대표 연락처 (선택)"
              class="input-new-field"
            />

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크인 날짜</label>
              <input
                v-model="campsiteData.check_in"
                @change="validateDates"
                type="date"
                class="input-new-field"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크아웃 날짜</label>
              <input
                v-model="campsiteData.check_out"
                @change="validateDates"
                type="date"
                class="input-new-field"
                required
              />
            </div>

            <div
              v-if="dateError"
              class="md:col-span-2 text-sm text-red-600 bg-red-50 p-3 rounded-md"
            >
              {{ dateError }}
            </div>

            <div class="md:col-span-2">
              <input
                v-model="campsiteData.layout_image_url"
                type="text"
                placeholder="사이트 배치도 이미지 URL (선택)"
                class="input-new-field"
              />
            </div>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">🕒 운영 정책</h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크인 시간</label>
              <input v-model="policy.check_in_time" type="time" class="input-new-field" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크아웃 시간</label>
              <input v-model="policy.check_out_time" type="time" class="input-new-field" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">매너타임 시작</label>
              <input v-model="policy.manner_time_start" type="time" class="input-new-field" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">매너타임 종료</label>
              <input v-model="policy.manner_time_end" type="time" class="input-new-field" />
            </div>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">🛁 편의시설</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            <label
              v-for="amenity in allAmenities"
              :key="amenity.id"
              class="flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-indigo-50 transition-colors"
            >
              <input
                type="checkbox"
                :value="amenity.id"
                v-model="selectedAmenities"
                class="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <img :src="amenity.icon_url" :alt="amenity.name" class="w-6 h-6" />
              <span class="text-gray-700">{{ amenity.name }}</span>
            </label>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">🖼️ 사진 등록</h2>
          <input
            type="file"
            multiple
            @change="handleFileSelect"
            accept="image/*"
            class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
          />
          <div v-if="images.length" class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="image in images" :key="image.id" class="relative">
              <img
                :src="image.previewSrc"
                :alt="image.file.name"
                class="w-full h-40 object-cover rounded-lg shadow-md"
              />
            </div>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">⛺ 사이트 관리</h2>
            <button type="button" @click="addSite" class="btn-new btn-new-secondary">
              + 사이트 추가
            </button>
          </div>
          <div class="space-y-4">
            <div
              v-for="(site, index) in sites"
              :key="site.id"
              class="p-4 grid grid-cols-1 md:grid-cols-4 gap-4 items-center border rounded-lg bg-gray-50"
            >
              <input
                v-model="site.name"
                type="text"
                placeholder="사이트 이름 (예: A1)"
                class="input-new-field"
              />
              <input
                v-model="site.camp_type"
                type="text"
                placeholder="캠프 타입 (예: 글램핑)"
                class="input-new-field"
              />
              <input
                v-model="site.base_price"
                type="text"
                placeholder="기본 요금"
                class="input-new-field"
              />
              <button
                type="button"
                @click="removeSite(index)"
                class="btn-new btn-new-danger justify-self-end"
              >
                삭제
              </button>
            </div>
            <p v-if="!sites.length" class="text-center text-gray-500 py-4">
              "사이트 추가" 버튼을 눌러 사이트를 등록하세요.
            </p>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">💰 추가 요금 규칙</h2>
            <button type="button" @click="addRule" class="btn-new btn-new-secondary">
              + 규칙 추가
            </button>
          </div>
          <div class="space-y-4">
            <div
              v-for="(rule, index) in pricingRules"
              :key="rule.id"
              class="p-4 border rounded-lg bg-gray-50 space-y-4"
            >
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input
                  v-model="rule.name"
                  type="text"
                  placeholder="규칙 이름 (예: 주말/성수기)"
                  class="input-new-field md:col-span-1"
                />
                <input
                  v-model.number="rule.extra_charge"
                  type="number"
                  placeholder="추가 요금"
                  class="input-new-field md:col-span-1"
                />
                <button
                  type="button"
                  @click="removeRule(index)"
                  class="btn-new btn-new-danger md:col-span-1 md:justify-self-end"
                >
                  삭제
                </button>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  v-model="rule.start_date"
                  type="date"
                  placeholder="시작일"
                  class="input-new-field"
                />
                <input
                  v-model="rule.end_date"
                  type="date"
                  placeholder="종료일"
                  class="input-new-field"
                />
              </div>
              <div class="flex items-center space-x-2 flex-wrap">
                <label class="text-sm font-medium text-gray-700 mr-2">적용 요일:</label>
                <label
                  v-for="day in weekDays"
                  :key="day.val"
                  class="flex items-center space-x-1 p-2 rounded-md cursor-pointer"
                  :class="
                    rule.day_of_week.includes(day.val)
                      ? 'bg-indigo-100 text-indigo-700'
                      : 'bg-gray-100'
                  "
                >
                  <input
                    type="checkbox"
                    :value="day.val"
                    v-model="rule.day_of_week"
                    class="hidden"
                  />
                  <span>{{ day.label }}</span>
                </label>
              </div>
            </div>
            <p v-if="!pricingRules.length" class="text-center text-gray-500 py-4">
              "규칙 추가" 버튼을 눌러 특정 기간/요일에 대한 추가 요금을 설정하세요.
            </p>
          </div>
        </section>

        <div class="pt-6">
          <button
            type="submit"
            :disabled="!isFormValid || isLoading"
            class="w-full btn-new btn-new-primary text-lg"
          >
            <span v-if="isLoading">
              <svg
                class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              등록 중...
            </span>
            <span v-else>✨ 캠핑 후기 등록 완료</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* 템플릿의 가독성을 위해 공통 스타일을 @apply로 정의 */
/* input-field */
/* .btn */
/* btn-primary
btn-secondary
danger */
</style>
