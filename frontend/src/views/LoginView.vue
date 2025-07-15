<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-white px-4">
    <div class="w-full max-w-sm">
      <h1 class="text-2xl font-semibold text-gray-900 mb-6">What's your email?</h1>
      <form @submit.prevent="onSubmit">
        <!-- Input Field -->
        <div class="mb-6">
          <input
            id="email"
            v-model="email"
            type="text"
            placeholder="Enter email"
            class="w-full h-10 px-3 rounded-md bg-gray-100 text-gray-700 placeholder-gray-500 focus:outline-none"
          />
          <span v-if="emailError" class="block mt-1 text-xs text-red-500 text-left">
            {{ emailError }}
          </span>
        </div>

        <div class="mb-4">
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="input your password"
            class="w-full h-10 px-3 rounded-md bg-gray-100 text-gray-700 placeholder-gray-500 focus:outline-none"
          />
          <span v-if="passwordError" class="block mt-1 text-xs text-red-500 text-left">
            {{ passwordError }}
          </span>
        </div>
        <!-- Continue Button -->
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
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'

import { useAuthStore } from '@/stores/useAuthStore'
import type { ILoginPayload } from '@/types/api'

// 1) 스키마 정의
const schema = yup.object({
  email: yup.string().required('Email is required').email('Invalid email address'),
  password: yup.string().required('Password is required'),
  // .min(1, 'Password must be more than 8 chars'),
})

// 2) useForm으로 전체 컨텍스트 생성
const { handleSubmit } = useForm<ILoginPayload>({
  validationSchema: schema,
})

// 3) useField로 각 필드 바인딩
const { value: email, errorMessage: emailError } = useField<string>('email')
const { value: password, errorMessage: passwordError } = useField<string>('password')

const authStore = useAuthStore()
const onSubmit = handleSubmit(async (values) => {
  await authStore.login(values)
  alert('Login successful! Welcome back.')
})

// const identifier = ref<string>('')

// function onContinue() {
//   // TODO: handle continue action
//   console.log('Continue with', identifier.value)
// }

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
