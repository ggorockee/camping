import { defineStore } from 'pinia'
import { ref, computed, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/index'
import type { IUser, ILoginPayload, ITokenResponse } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()

  // State
  const accessToken: Ref<string | null> = ref(localStorage.getItem('accessToken'))
  const user: Ref<IUser | null> = ref(null)

  // Getters
  const isAuthenticated = computed<boolean>(() => Boolean(accessToken.value))
  const username = computed<string>(() => user.value?.username ?? 'Guest')

  // Helpers
  function setToken(token: string): void {
    accessToken.value = token
    localStorage.setItem('accessToken', token)
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  // Actions
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
      logout()
    }
  }

  async function login(payload: ILoginPayload): Promise<void> {
    const response = await apiClient.post<ITokenResponse>('/users/token/', payload)
    setToken(response.data.access)
    await fetchUser()
    await router.push('/')
  }

  function logout(redirectPath = '/login'): void {
    accessToken.value = null
    user.value = null
    localStorage.removeItem('accessToken')
    delete apiClient.defaults.headers.common['Authorization']
    alert('Logged out successfully.')
    void router.push(redirectPath)
  }

  return {
    accessToken,
    user,
    isAuthenticated,
    username,
    fetchUser,
    login,
    logout,
  }
})
