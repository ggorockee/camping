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
          <input
            id="email"
            v-model="email"
            type="text"
            placeholder="Enter email"
            class="w-full h-10 px-3 rounded-md bg-gray-100 text-gray-700 placeholder-gray-500 focus:outline-none"
            :class="{ 'border border-red-500': emailError || loginError }"
          />
          <span v-if="emailError" class="block mt-1 text-xs text-red-500 text-left">
            {{ emailError }}
          </span>
        </div>

        <div class="mb-6">
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="input your password"
            class="w-full h-10 px-3 rounded-md bg-gray-100 text-gray-700 placeholder-gray-500 focus:outline-none"
            :class="{ 'border border-red-500': passwordError || loginError }"
          />
          <span v-if="passwordError" class="block mt-1 text-xs text-red-500 text-left">
            {{ passwordError }}
          </span>
        </div>
        <button
          type="submit"
          class="w-full h-10 mb-6 bg-black text-white rounded-md font-medium hover:bg-gray-800 transition"
        >
          Continue
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
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'

import { useAuthStore } from '@/stores/useAuthStore'
import type { ILoginPayload } from '@/types/api'

// 1) 스키마 정의 (동일)
const schema = yup.object({
  email: yup.string().required('Email is required').email('Invalid email address'),
  password: yup.string().required('Password is required'),
})

// 2) useForm으로 전체 컨텍스트 생성 (동일)
const { handleSubmit } = useForm<ILoginPayload>({
  validationSchema: schema,
})

// 3) useField로 각 필드 바인딩 (동일)
const { value: email, errorMessage: emailError } = useField<string>('email')
const { value: password, errorMessage: passwordError } = useField<string>('password')

// 👇 [추가] 서버로부터 받은 로그인 에러 메시지를 저장할 ref
const loginError = ref<string | null>(null)

const authStore = useAuthStore()
// 👇 [수정] onSubmit 함수를 try...catch로 감싸 에러를 처리합니다.
const onSubmit = handleSubmit(async (values) => {
  // 에러 메시지 초기화
  loginError.value = null
  try {
    await authStore.login(values)
    alert('Login successful! Welcome back.')
    // 실제 서비스에서는 보통 alert 대신 라우터로 메인 페이지로 이동시킵니다.
    // router.push('/')
  } catch (error) {
    // 로그인 실패 시 에러 메시지 설정
    loginError.value = '이메일 또는 비밀번호를 확인해주세요.'
    console.error(error) // 실제 에러 내용 확인용
  }
})

// 👇 [추가] 사용자가 이메일이나 비밀번호를 다시 입력하면 에러 메시지를 지웁니다.
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
