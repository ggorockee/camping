// src/stores/authStore.ts (수정 후)

import { defineStore } from 'pinia'
import { ref, computed, type Ref } from 'vue'
import apiClient from '@/api/index'
import type { IUser, ILoginPayload, ITokenResponse, IRegisterResponse } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  // --- State ---
  const accessToken: Ref<string | null> = ref(localStorage.getItem('accessToken'))
  const user: Ref<IUser | null> = ref(null)

  // --- Getters ---
  const isAuthenticated = computed<boolean>(() => !!user.value && !!accessToken.value)
  const username = computed<string>(() => user.value?.username ?? 'Guest')

  // --- Helpers ---
  function setToken(token: string): void {
    accessToken.value = token
    localStorage.setItem('accessToken', token)
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  // --- Actions ---
  async function fetchUser(): Promise<void> {
    if (!accessToken.value) return

    if (!apiClient.defaults.headers.common['Authorization']) {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
    }

    try {
      const response = await apiClient.get<IUser>('/users/me/')
      user.value = response.data
    } catch (err) {
      console.error('Failed to fetch user:', err)
      // 토큰이 유효하지 않으므로 상태를 초기화합니다.
      accessToken.value = null
      user.value = null
      localStorage.removeItem('accessToken')
      delete apiClient.defaults.headers.common['Authorization']
    }
  }

  async function login(payload: ILoginPayload): Promise<void> {
    const response = await apiClient.post<ITokenResponse>('/users/token/', payload)
    setToken(response.data.access)
    await fetchUser()
    // 페이지 이동 로직은 컴포넌트에서 처리하므로 여기서는 제거
  }

  function logout(): void {
    accessToken.value = null
    user.value = null
    localStorage.removeItem('accessToken')
    delete apiClient.defaults.headers.common['Authorization']
    // alert 및 페이지 이동 로직은 컴포넌트에서 처리하므로 여기서는 제거
  }

  function registerSuccess(data: IRegisterResponse): void {
    user.value = data.user
    setToken(data.access_token)
    // 페이지 이동 로직은 컴포넌트에서 처리하므로 여기서는 제거
  }

  return {
    accessToken,
    user,
    isAuthenticated,
    username,
    fetchUser,
    login,
    logout,
    registerSuccess,
  }
})
