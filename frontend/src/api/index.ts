import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10_000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 요청 인터셉터 설정
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 로컬 스토리지에서 accessToken을 가져옵니다.
    const token = localStorage.getItem('accessToken')

    // 토큰이 존재하면 Authorization 헤더에 추가합니다.
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    // 요청 에러 처리
    return Promise.reject(error)
  },
)

export default apiClient
