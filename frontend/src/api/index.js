import axios from "axios";

// Axios 인스턴스 생성
const apiClient = axios.create({
  // Django 서버의 기본 URL을 입력합니다.
  baseURL: import.meta.env.VITE_API_BASE_URL,
  // 타임아웃을 10초로 설정합니다.
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
