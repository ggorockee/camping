<script setup lang="ts">
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import { ref, reactive, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/index'
import type { IAmenity, ISite, IPricingRule, IImageFile } from '@/types/api'

// --- 1. 상태 관리 ---
const router = useRouter()
const dateRange = ref<[Date, Date] | null>(null)
const campsiteData = reactive({
  name: '',
  address: '',
  description: '',
  price: null as number | null,
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
const isLoading = ref(false) // 전체 제출 로딩
const isUploading = ref(false) // 이미지 업로드 중
const errorMessage = ref('')
const dateError = ref('')
const showSuccessToast = ref(false)
const successMessage = ref('')
const uploadProgress = ref(0)
const totalImagesToUpload = ref(0)
const uploadedImageCount = ref(0)
const weekDays = [
  { label: '일', val: '0' },
  { label: '월', val: '1' },
  { label: '화', val: '2' },
  { label: '수', val: '3' },
  { label: '목', val: '4' },
  { label: '금', val: '5' },
  { label: '토', val: '6' },
]

// --- 2. Computed 및 Watchers ---
const isFormValid = computed(() => {
  return (
    campsiteData.name.trim() !== '' &&
    campsiteData.address.trim() !== '' &&
    images.value.length >= 1 &&
    dateRange.value !== null
  )
})

// dateRange가 변경되면 campsiteData.check_in/out 값을 업데이트
watch(dateRange, (newRange) => {
  if (newRange && newRange[0] && newRange[1]) {
    // 날짜를 'YYYY-MM-DD' 형식의 문자열로 변환
    const formatDate = (date: Date) => date.toISOString().split('T')[0]
    campsiteData.check_in = formatDate(newRange[0])
    campsiteData.check_out = formatDate(newRange[1])
    dateError.value = ''
  } else {
    campsiteData.check_in = ''
    campsiteData.check_out = ''
  }
})

watch(uploadedImageCount, (currentCount) => {
  if (totalImagesToUpload.value > 0) {
    uploadProgress.value = Math.round((currentCount / totalImagesToUpload.value) * 100)
  } else {
    uploadProgress.value = 0
  }
})

watch(isUploading, (isUploadingNow) => {
  document.body.style.overflow = isUploadingNow ? 'hidden' : ''
})

onUnmounted(() => {
  document.body.style.overflow = ''
})

// --- 3. 함수 ---
onMounted(async () => {
  try {
    const response = await apiClient.get<IAmenity[]>('/amenities/')
    allAmenities.value = response.data
  } catch (error) {
    console.error('편의시설 목록 로딩 실패:', error)
  }
})

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

const addFiles = (files: FileList | null) => {
  if (!files) return
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
const handleFileSelect = (event: Event) => addFiles((event.target as HTMLInputElement).files)

// const validateDates = () => {
//   if (campsiteData.check_in && campsiteData.check_out) {
//     const checkInDate = new Date(campsiteData.check_in)
//     const checkOutDate = new Date(campsiteData.check_out)
//     dateError.value =
//       checkOutDate < checkInDate ? '체크아웃 날짜는 체크인 날짜보다 빠를 수 없습니다.' : ''
//   }
// }

const formatDateRange = (dates: Date[]) => {
  if (dates && dates.length === 2) {
    const start = dates[0]
    const end = dates[1]

    const startYear = start.getFullYear()
    const startMonth = start.getMonth() + 1
    const startDate = start.getDate()

    const endYear = end.getFullYear()
    const endMonth = end.getMonth() + 1
    const endDate = end.getDate()

    // 시작일과 종료일이 같은 해, 같은 월일 경우 더 간결하게 표시
    if (startYear === endYear && startMonth === endMonth) {
      return `${startYear}년 ${startMonth}월 ${startDate}일 ~ ${endDate}일`
    }
    // 시작일과 종료일이 같은 해일 경우
    else if (startYear === endYear) {
      return `${startYear}년 ${startMonth}월 ${startDate}일 ~ ${endMonth}월 ${endDate}일`
    }
    // 그 외
    return `${startYear}년 ${startMonth}월 ${startDate}일 ~ ${endYear}년 ${endMonth}월 ${endDate}일`
  }
  return ''
}

async function createCampsite() {
  if (!isFormValid.value) {
    errorMessage.value = '캠핑장 이름, 주소, 그리고 최소 1개 이상의 이미지는 필수입니다.'
    return
  }

  errorMessage.value = ''
  isLoading.value = true
  isUploading.value = true

  try {
    const pendingImages = images.value.filter((img) => img.status === 'pending')
    totalImagesToUpload.value = pendingImages.length
    uploadedImageCount.value = 0
    let uploadedImageIds: string[] = []

    if (pendingImages.length > 0) {
      const urlPromises = pendingImages.map(() =>
        apiClient
          .post<{ id: string; uploadURL: string }>('/campsites/images/upload-url/')
          .then((res) => res.data),
      )
      const urlResults = await Promise.all(urlPromises)

      const uploadPromises = urlResults.map((result, index) => {
        const formData = new FormData()
        formData.append('file', pendingImages[index].file)
        return fetch(result.uploadURL, { method: 'POST', body: formData }).then((res) => {
          if (!res.ok) throw new Error(`'${pendingImages[index].file.name}' 업로드 실패`)

          // ⭐️ [핵심 수정] 이 부분이 누락되었습니다! 각 이미지 업로드 성공 시 카운터를 증가시킵니다.
          uploadedImageCount.value++

          return result.id
        })
      })
      uploadedImageIds = await Promise.all(uploadPromises)
    }

    const finalPayload = {
      ...campsiteData,
      policy: { ...policy },
      sites: [...sites.value],
      amenities: [...selectedAmenities.value],
      pricing_rules: pricingRules.value.map((r) => ({
        ...r,
        day_of_week: r.day_of_week.join(','),
      })),
      image_ids: uploadedImageIds,
    }

    const response = await apiClient.post<{ id: number }>('/campsites/', finalPayload)
    const newCampsiteId = response.data.id

    if (!newCampsiteId) {
      throw new Error('서버 응답에 생성된 캠핑장 ID가 없습니다.')
    }

    isUploading.value = false // 업로드 오버레이 숨김
    successMessage.value = `🎉 '${campsiteData.name}' 캠핑장이 성공적으로 등록되었습니다!`
    showSuccessToast.value = true // 성공 토스트 표시

    // 1.5초 후 토스트를 숨기고 상세 페이지로 이동
    setTimeout(() => {
      showSuccessToast.value = false
      router.push({ name: 'campsite-detail', params: { id: newCampsiteId } })
    }, 1500)
  } catch (error: any) {
    console.error('캠핑장 생성 실패:', error)
    errorMessage.value =
      error.response?.data?.detail || error.message || '알 수 없는 오류가 발생했습니다.'
  } finally {
    // 최종 로딩 상태는 catch 블록 이후, setTimeout과 관계없이 바로 해제
    isLoading.value = false
    // isUploading은 성공/실패 시점에 맞춰 제어되므로 여기서 false로 설정
    isUploading.value = false
  }
}
</script>
<template>
  <div class="bg-gray-50 font-sans">
    <div
      v-if="isUploading"
      class="fixed inset-0 bg-white/50 backdrop-blur-sm flex flex-col items-center justify-center z-50 transition-opacity duration-300"
    >
      <div class="w-full max-w-md text-center">
        <h3 class="text-2xl font-bold text-gray-800 mb-4">이미지 업로드 중...</h3>
        <p class="text-gray-600 mb-6">
          잠시만 기다려 주세요. ({{ uploadedImageCount }} / {{ totalImagesToUpload }})
        </p>

        <div class="w-full bg-gray-200 rounded-full h-6 overflow-hidden shadow-inner">
          <div
            class="bg-indigo-600 h-full rounded-full text-center text-white text-sm leading-6 transition-all duration-500"
            :style="{ width: uploadProgress + '%' }"
          >
            {{ uploadProgress }}%
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showSuccessToast"
      class="fixed top-5 right-5 bg-green-500 text-white py-3 px-6 rounded-lg shadow-xl z-50 flex items-center space-x-3"
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
        ></path>
      </svg>
      <span>{{ successMessage }}</span>
    </div>

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

            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">방문 날짜</label>
              <VueDatePicker
                v-model="dateRange"
                range
                :enable-time-picker="false"
                placeholder="캠핑을 다녀온 날짜를 선택하세요"
                :format="formatDateRange"
                auto-apply
                locale="ko"
                month-name-format="long"
                :max-date="new Date()"
                :teleport="true"
              />
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
:deep(.dp__input) {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  line-height: 1.5rem; /* 라인 높이 추가 */
  transition: all 0.2s;
}

/* 아이콘을 위한 왼쪽 여백 추가 */
:deep(.dp__input_icon) {
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
}

/* 플레이스홀더와 선택된 값 모두를 포함하는 input 자체에 패딩을 적용합니다. */
:deep(.dp__input_icon) {
  left: 5px;
  top: 50%;
  transform: translateY(-50%);
}

/* 플레이스홀더와 선택된 값 모두를 포함하는 input 자체에 패딩을 적용합니다. */
:deep(.dp__input) {
  /* ⭐️ 핵심: 아이콘 너비와 여유 공간만큼 왼쪽 패딩을 강제로 확보합니다. */
  padding-left: 40px !important;

  /* 기존 input 스타일 유지 */
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  padding-right: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
}
/* 템플릿의 가독성을 위해 공통 스타일을 @apply로 정의 */
/* input-field */
/* .btn */
/* btn-primary
btn-secondary
danger */
</style>
