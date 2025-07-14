<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-white px-4">
    <div class="w-full max-w-sm">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Create your account</h1>
      <p class="text-gray-600 mb-8">Let's get started with a free account.</p>
      <form @submit.prevent="onSubmit" novalidate>
        <div class="mb-4">
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your email"
            class="w-full h-11 px-4 rounded-md bg-gray-100 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black"
            aria-label="Email"
          />
          <span v-if="emailError" class="block mt-1.5 text-xs text-red-500 text-left">
            {{ emailError }}
          </span>
        </div>

        <div class="mb-4">
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Enter your Nickname"
            class="w-full h-11 px-4 rounded-md bg-gray-100 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black"
            aria-label="Username"
          />
          <span v-if="usernameError" class="block mt-1.5 text-xs text-red-500 text-left">
            {{ usernameError }}
          </span>
        </div>

        <div class="mb-4">
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Create a password"
            class="w-full h-11 px-4 rounded-md bg-gray-100 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black"
            aria-label="Password"
          />
          <span v-if="passwordError" class="block mt-1.5 text-xs text-red-500 text-left">
            {{ passwordError }}
          </span>
        </div>

        <div class="mb-8">
          <input
            id="passwordConfirmation"
            v-model="passwordConfirmation"
            type="password"
            placeholder="Confirm Password"
            class="w-full h-11 px-4 rounded-md bg-gray-100 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black"
            aria-label="Confirm Password"
          />
          <span
            v-if="passwordConfirmationError"
            class="block mt-1.5 text-xs text-red-500 text-left"
          >
            {{ passwordConfirmationError }}
          </span>
        </div>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full h-11 mb-6 bg-black text-white rounded-md font-medium hover:bg-gray-800 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          <svg
            v-if="isSubmitting"
            class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
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
          {{ isSubmitting ? 'Processing...' : 'Sign Up' }}
        </button>
      </form>

      <p class="text-sm text-center text-gray-500">
        Already have an account?
        <RouterLink to="/login" class="font-medium text-black hover:underline">Log in</RouterLink>
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import apiClient from '@/api'
import axios from 'axios'
import type { IRegisterPayload, IRegisterResponse } from '@/types/api'

// ⭐️ [기능 구현] phone_number 필드 제거
const schema = yup.object({
  email: yup.string().required('Email is required').email('Invalid email format'),
  username: yup.string().required('Username is required').min(2, 'Must be at least 2 characters'),
  password: yup
    .string()
    .required('Password is required')
    .min(8, 'Password must be at least 8 characters'),
  // ⭐️ [기능 구현] 비밀번호 확인 필드 유효성 검사 추가
  passwordConfirmation: yup
    .string()
    .required('Please confirm your password')
    .oneOf([yup.ref('password')], 'Passwords must match'),
})

// const router = useRouter()
const authStore = useAuthStore()

const { handleSubmit, isSubmitting } = useForm<IRegisterPayload>({
  validationSchema: schema,
})

const { value: email, errorMessage: emailError } = useField<string>('email')
const { value: username, errorMessage: usernameError } = useField<string>('username')
const { value: password, errorMessage: passwordError } = useField<string>('password')
const { value: passwordConfirmation, errorMessage: passwordConfirmationError } =
  useField<string>('passwordConfirmation')

const onSubmit = handleSubmit(async (values) => {
  try {
    // API 응답 타입을 IRegisterResponse로 지정
    const response = await apiClient.post<IRegisterResponse>('/users/register/', values)

    // 스토어의 액션을 호출하여 로그인 상태 처리 및 리디렉션
    authStore.registerSuccess(response.data)

    alert('회원가입 및 로그인이 완료되었습니다. 환영합니다!')
  } catch (error: unknown) {
    console.error('Registration failed:', error)
    if (axios.isAxiosError(error) && error.response) {
      alert(`회원가입 실패: ${JSON.stringify(error.response.data)}`)
    } else {
      alert('회원가입 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
    }
  }
})

// function onGoogleLogin() {
//   // TODO: Google OAuth
// }
</script>
