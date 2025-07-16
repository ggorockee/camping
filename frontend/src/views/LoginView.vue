<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-white px-4">
    <div class="w-full max-w-sm">
      <h1 class="text-2xl font-semibold text-gray-900 mb-6">What's your email?</h1>
      <div
        v-if="loginError"
        class="mb-4 p-3 rounded-md bg-red-100 text-red-700 text-sm text-center"
      >
        {{ loginError }}
      </div>
      <form @submit.prevent="onSubmit">
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">이메일</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="example@email.com"
            class="w-full h-10 px-3 rounded-md bg-gray-100 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-400"
            :class="{ 'border border-red-500': emailError || loginError }"
            :disabled="isLoading"
          />
          <span v-if="emailError" class="block mt-1 text-xs text-red-500 text-left">
            {{ emailError }}
          </span>
        </div>

        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1"
            >비밀번호</label
          >
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="비밀번호를 입력하세요"
            class="w-full h-10 px-3 rounded-md bg-gray-100 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-400"
            :class="{ 'border border-red-500': passwordError || loginError }"
            :disabled="isLoading"
          />
          <span v-if="passwordError" class="block mt-1 text-xs text-red-500 text-left">
            {{ passwordError }}
          </span>
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full h-10 mb-6 flex items-center justify-center bg-black text-white rounded-md font-medium hover:bg-gray-800 transition disabled:bg-gray-400"
        >
          <span v-if="!isLoading">계속하기</span>
          <svg
            v-else
            class="animate-spin h-5 w-5 text-white"
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
        </button>
      </form>

      <!-- Separator -->
      <div class="flex items-center mb-6">
        <div class="flex-grow h-px bg-gray-300"></div>
        <span class="px-2 text-xs text-gray-500">or</span>
        <div class="flex-grow h-px bg-gray-300"></div>
      </div>

      <!-- Social Buttons -->
      <button
        @click="onGoogleLogin"
        class="w-full h-10 mb-3 flex items-center justify-center bg-gray-100 rounded-md font-medium hover:bg-gray-200 transition"
      >
        <img src="/google-icon.svg" alt="Google" class="w-5 h-5 mr-2" />
        Continue with Google
      </button>
      <button
        @click="onAppleLogin"
        class="w-full h-10 mb-6 flex items-center justify-center bg-gray-100 rounded-md font-medium hover:bg-gray-200 transition"
      >
        <img src="/apple-icon.svg" alt="Apple" class="w-5 h-5 mr-2" />
        Continue with Apple
      </button>

      <!-- Separator -->
      <div class="flex items-center mb-6">
        <div class="flex-grow h-px bg-gray-300"></div>
        <span class="px-2 text-xs text-gray-500">or</span>
        <div class="flex-grow h-px bg-gray-300"></div>
      </div>

      <!-- QR Code Login -->
      <button
        @click="onQrLogin"
        class="w-full h-10 mb-6 bg-gray-100 rounded-md font-medium hover:bg-gray-200 transition flex items-center justify-center"
      >
        <img src="/qr-icon.svg" alt="QR" class="w-5 h-5 mr-2" />
        Log in with QR code
      </button>

      <!-- Disclaimer -->
      <p class="text-xs text-gray-500">
        By proceeding, you consent to get calls, WhatsApp or SMS/RCS messages, including by
        automated means, from Uber and its affiliates to the number provided.
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue' // ref와 watch를 import 합니다.
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'

import { useAuthStore } from '@/stores/useAuthStore'
import type { ILoginPayload } from '@/types/api'

// 1) 스키마 정의 (동일)
const schema = yup.object({
  email: yup.string().required('이메일을 입력해주세요.').email('올바른 이메일 형식이 아닙니다.'),
  password: yup.string().required('비밀번호를 입력해주세요.'),
})
// 2) useForm으로 전체 컨텍스트 생성 (동일)
const { handleSubmit } = useForm<ILoginPayload>({
  validationSchema: schema,
})

// 3) useField로 각 필드 바인딩 (동일)
const { value: email, errorMessage: emailError } = useField<string>('email')
const { value: password, errorMessage: passwordError } = useField<string>('password')

const authStore = useAuthStore()
const router = useRouter()
const loginError = ref<string | null>(null)
const isLoading = ref(false) // 로딩 상태 ref 추가

// onSubmit 함수 로직 개선 ---
const onSubmit = handleSubmit(async (values) => {
  loginError.value = null
  isLoading.value = true // 로딩 시작

  try {
    await authStore.login(values)
    router.push('/') // 로그인 성공 시 홈으로 이동
  } catch (error: any) {
    // 서버가 구체적인 에러 메시지를 주면 그것을 사용, 아니면 기본 메시지 사용
    loginError.value = error.response?.data?.detail || '이메일 또는 비밀번호를 확인해주세요.'
    console.error('로그인 실패:', error)
  } finally {
    isLoading.value = false // 로딩 종료 (성공/실패 무관)
  }
})

// --- 수정: watch 로직은 그대로 유지 (좋은 기능!) ---
watch([email, password], () => {
  if (loginError.value) {
    loginError.value = null
  }
})

function onGoogleLogin() {
  // TODO: Google OAuth
}

function onAppleLogin() {
  // TODO: Apple OAuth
}

function onQrLogin() {
  // TODO: QR login
}
</script>

<style scoped>
/* 스타일은 Tailwind CSS 유틸리티로 관리합니다 */
</style>
