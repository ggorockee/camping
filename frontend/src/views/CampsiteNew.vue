<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

// --- 타입 정의 (TypeScript) ---
interface Site {
  id: number
  name: string
  camp_type: string
  base_price: number | null
}
interface PricingRule {
  id: number
  name: string
  start_date: string
  end_date: string
  day_of_week: string[] // "0"~"6" (일~토)
  extra_charge: number | null
}
interface ImageFile {
  id: number
  file: File
  previewSrc: string
}

// --- 기본 데이터 ---
const allAmenities = [
  { id: 'wifi', name: '무선 인터넷', icon: '📶' },
  { id: 'parking', name: '주차장', icon: '🅿️' },
  { id: 'shower', name: '샤워실', icon: '🚿' },
  { id: 'store', name: '매점', icon: '🏪' },
  { id: 'pool', name: '수영장', icon: '🏊' },
  { id: 'pet', name: '반려동물 동반', icon: '🐾' },
]
const weekDays = [
  { label: '일', val: '0' },
  { label: '월', val: '1' },
  { label: '화', val: '2' },
  { label: '수', val: '3' },
  { label: '목', val: '4' },
  { label: '금', val: '5' },
  { label: '토', val: '6' },
]

// --- 반응형 상태 (Reactive State) ---
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
const sites = ref<Site[]>([])
const pricingRules = ref<PricingRule[]>([])
const selectedAmenities = ref<string[]>([])
const images = ref<ImageFile[]>([])
const isLoading = ref(false)
const dateError = ref('')

// --- 동적 리스트 관리 ---
const addSite = () => {
  sites.value.push({ id: Date.now(), name: '', camp_type: '오토캠핑', base_price: null })
}
const removeSite = (index: number) => {
  sites.value.splice(index, 1)
}
const addRule = () => {
  pricingRules.value.push({
    id: Date.now(),
    name: '',
    start_date: '',
    end_date: '',
    day_of_week: [],
    extra_charge: null,
  })
}
const removeRule = (index: number) => {
  pricingRules.value.splice(index, 1)
}

// --- 파일 핸들링 ---
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = Array.from(target.files || [])
  files.forEach((file) => {
    images.value.push({
      id: Date.now() + Math.random(),
      file,
      previewSrc: URL.createObjectURL(file),
    })
  })
}

// --- 유효성 검사 및 제출 ---
const validateDates = () => {
  const today = new Date()
  today.setHours(0, 0, 0, 0) // 시간 정보를 제거하여 날짜만 비교

  const checkInDate = campsiteData.check_in ? new Date(campsiteData.check_in) : null
  const checkOutDate = campsiteData.check_out ? new Date(campsiteData.check_out) : null

  dateError.value = '' // 에러 메시지 초기화

  if (checkInDate && checkOutDate && checkInDate >= checkOutDate) {
    dateError.value = '체크아웃 날짜는 체크인 날짜보다 이후여야 합니다.'
    return false
  }
  if (checkInDate && checkInDate >= today) {
    dateError.value = '체크인 날짜는 오늘 이전이어야 합니다.'
    return false
  }
  if (checkOutDate && checkOutDate >= today) {
    dateError.value = '체크아웃 날짜는 오늘 이전이어야 합니다.'
    return false
  }
  return true
}

const isFormValid = computed(() => {
  const basicInfoValid = campsiteData.name && campsiteData.address && campsiteData.price
  return basicInfoValid && validateDates()
})

const handleSubmit = () => {
  if (!isFormValid.value) {
    alert('필수 항목을 모두 입력하고 날짜를 올바르게 선택해주세요.')
    return
  }
  isLoading.value = true

  // 백엔드로 보낼 데이터 최종 조합
  const finalData = {
    ...campsiteData,
    policy: { ...policy },
    sites: [...sites.value],
    amenities: [...selectedAmenities.value],
    pricing_rules: pricingRules.value.map((rule) => ({
      ...rule,
      day_of_week: rule.day_of_week.join(','), // 배열을 쉼표로 구분된 문자열로 변환
    })),
    // images는 별도로 FormData로 처리 필요
  }

  console.log('Submitting Data:', JSON.stringify(finalData, null, 2))

  // API 호출 시뮬레이션
  setTimeout(() => {
    isLoading.value = false
    alert('캠핑장 후기 등록이 완료되었습니다! (콘솔 로그 확인)')
  }, 2000)
}
</script>

<template>
  <div class="bg-gray-50 font-sans">
    <div class="container mx-auto max-w-5xl py-12 px-4 mt-12">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-gray-900">캠핑 후기 등록</h1>
        <p class="mt-4 text-lg text-gray-600">다녀오신 캠핑장의 정보를 상세히 기록해주세요.</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-10">
        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">🏕️ 기본 정보</h2>
          <p class="text-gray-600 mb-6">캠핑을 다녀온 경험을 바탕으로 정보를 입력해주세요.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <input
              v-model="campsiteData.name"
              type="text"
              placeholder="캠핑장 이름"
              class="input-field"
              required
            />
            <input
              v-model="campsiteData.address"
              type="text"
              placeholder="주소"
              class="input-field"
              required
            />
            <div class="md:col-span-2">
              <textarea
                v-model="campsiteData.description"
                rows="4"
                placeholder="캠핑장 설명 (특징, 주변 경관 등)"
                class="input-field"
              ></textarea>
            </div>
            <input
              v-model.number="campsiteData.price"
              type="number"
              placeholder="총 숙박 요금 (원)"
              class="input-field"
              required
            />
            <input
              v-model="campsiteData.contact_number"
              type="tel"
              placeholder="대표 연락처 (선택)"
              class="input-field"
            />

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크인 날짜</label>
              <input
                v-model="campsiteData.check_in"
                @change="validateDates"
                type="date"
                class="input-field"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크아웃 날짜</label>
              <input
                v-model="campsiteData.check_out"
                @change="validateDates"
                type="date"
                class="input-field"
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
                class="input-field"
              />
            </div>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">🕒 운영 정책</h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크인 시간</label>
              <input v-model="policy.check_in_time" type="time" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">체크아웃 시간</label>
              <input v-model="policy.check_out_time" type="time" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">매너타임 시작</label>
              <input v-model="policy.manner_time_start" type="time" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">매너타임 종료</label>
              <input v-model="policy.manner_time_end" type="time" class="input-field" />
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
              <span class="text-gray-700">{{ amenity.icon }} {{ amenity.name }}</span>
            </label>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">🖼️ 사진 등록</h2>
          <input
            type="file"
            multiple
            @change="handleFileSelect"
            class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
          />
          <div v-if="images.length" class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="image in images" :key="image.id" class="relative">
              <img :src="image.previewSrc" class="w-full h-40 object-cover rounded-lg shadow-md" />
            </div>
          </div>
        </section>

        <section class="p-8 bg-white rounded-xl shadow-lg border border-gray-200">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">⛺ 사이트 관리</h2>
            <button type="button" @click="addSite" class="btn btn-secondary">+ 사이트 추가</button>
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
                class="input-field"
              />
              <input
                v-model="site.camp_type"
                type="text"
                placeholder="캠프 타입 (예: 글램핑)"
                class="input-field"
              />
              <input
                v-model.number="site.base_price"
                type="number"
                placeholder="기본 요금"
                class="input-field"
              />
              <button
                type="button"
                @click="removeSite(index)"
                class="btn btn-danger justify-self-end"
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
            <button type="button" @click="addRule" class="btn btn-secondary">+ 규칙 추가</button>
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
                  class="input-field md:col-span-1"
                />
                <input
                  v-model.number="rule.extra_charge"
                  type="number"
                  placeholder="추가 요금"
                  class="input-field md:col-span-1"
                />
                <button
                  type="button"
                  @click="removeRule(index)"
                  class="btn btn-danger md:col-span-1 md:justify-self-end"
                >
                  삭제
                </button>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  v-model="rule.start_date"
                  type="date"
                  placeholder="시작일"
                  class="input-field"
                />
                <input
                  v-model="rule.end_date"
                  type="date"
                  placeholder="종료일"
                  class="input-field"
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
            class="w-full btn btn-primary text-lg"
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

<style></style>
