<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-white px-4">
    <div class="w-full max-w-sm">
      <h1 class="text-2xl font-semibold text-gray-900 mb-6">What's your phone number or email?</h1>
      <!-- Input Field -->
      <input
        v-model="identifier"
        type="text"
        placeholder="Enter phone number or email"
        class="w-full h-10 px-3 mb-4 rounded-md bg-gray-100 text-gray-700 placeholder-gray-500 focus:outline-none"
      />
      <!-- Continue Button -->
      <button
        @click="onContinue"
        class="w-full h-10 mb-6 bg-black text-white rounded-md font-medium hover:bg-gray-800 transition"
      >
        Continue
      </button>

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
import { ref } from 'vue'

const identifier = ref<string>('')

function onContinue() {
  // TODO: handle continue action
  console.log('Continue with', identifier.value)
}

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
