import { defineStore } from "pinia";
import { ref, computed } from "vue";
import apiClient from "@/api/index.js"; 
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", () => {
  const router = useRouter();

  // 1. State (상태): 컴포넌트의 data와 유사
  // localStorage에서 토큰을 가져와 초기값으로 설정 (페이지 새로고침 시 로그인 유지)
  const accessToken = ref(localStorage.getItem("accessToken"));
  const user = ref(null);

  // 2. Getters (컴퓨티드): 계산된 상태
  const isAuthenticated = computed(() => !!accessToken.value);
  const username = computed(() => user.value?.username || "Guest");

  // 3. Actions (메서드): 상태를 변경하는 로직
  /**
   * 토큰을 상태와 localStorage에 저장하고, API 클라이언트 헤더를 설정
   */
  function setToken(token) {
    accessToken.value = token;
    localStorage.setItem("accessToken", token);
    apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }

  /**
   * 저장된 토큰을 사용하여 서버에서 사용자 정보를 가져옴
   */
  async function fetchUser() {
    if (!accessToken.value) return;

    // API 헤더가 설정 안된 경우를 대비 (페이지 새로고침 등)
    if (!apiClient.defaults.headers.common["Authorization"]) {
      apiClient.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${accessToken.value}`;
    }

    try {
      const response = await apiClient.get("/users/me/");
      user.value = response.data;
    } catch (error) {
      console.error("Failed to fetch user:", error);
      // 토큰이 유효하지 않은 경우일 수 있으므로 로그아웃 처리
      logout();
    }
  }

  /**
   * 로그인 처리를 통합한 액션
   */
  async function login(payload) {
    // 1. Django API로 로그인(토큰 발급) 요청
    const response = await apiClient.post("/users/token/", payload);

    // 2. 토큰 저장 및 API 헤더 설정
    setToken(response.data.access);

    // 3. 사용자 정보 가져오기
    await fetchUser();

    // 4. 메인 페이지로 이동
    router.push("/");
  }

  /**
   * 로그아웃 처리
   */
  function logout(redirectPath = "/login") {
    accessToken.value = null;
    user.value = null;
    localStorage.removeItem("accessToken");
    delete apiClient.defaults.headers.common["Authorization"];
    alert("Logged out successfully.");
    router.push(redirectPath); // 로그아웃 후 로그인 페이지로 이동
  }

  return {
    // State
    accessToken,
    user,
    // Getters
    isAuthenticated,
    username,
    // Actions
    login,
    logout,
    fetchUser,
  };
});
