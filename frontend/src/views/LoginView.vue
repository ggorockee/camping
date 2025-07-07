<script setup>
import { reactive } from "vue";
import apiClient from "@/api/index.js"; // 기존과 동일한 API 클라이언트 사용
import { useRouter } from "vue-router";

const router = useRouter(); // 페이지 이동을 위해 router 인스턴스 생성

// v-model을 통해 폼 데이터를 관리하는 반응형 객체
const form = reactive({
  email: "",
  password: "",
});

// 폼 제출 시 실행될 함수
async function submitForm() {
  try {
    // 1. Django API로 로그인(토큰 발급) 요청
    // 요청 본문(payload)은 form 객체 전체를 보냅니다.
    const response = await apiClient.post("/users/token/", form);

    // 2. 응답 데이터에서 access 토큰 추출
    const accessToken = response.data.access;

    // 3. 토큰을 localStorage에 저장
    localStorage.setItem("accessToken", accessToken);

    // 4. (중요) 향후 다른 API 요청 시 인증 헤더에 토큰을 자동으로 포함하도록 설정
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

    alert("Login successful! Welcome back.");

    // 5. 로그인 성공 시 메인 페이지로 이동
    router.push("/");
    
  } catch (error) {
    console.error("Login failed:", error.response);

    // 에러 처리
    if (error.response && error.response.data) {
      // Django에서 보낸 에러 메시지를 alert으로 표시
      alert(`Login failed: ${JSON.stringify(error.response.data)}`);
    } else {
      alert("An unexpected error occurred. Please try again.");
    }
  }
}
</script>

<template>
  <main class="main pt-4">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <article class="card card-outline mb-4">
            <div class="card-body">
              <header class="text-center">
                <h4 class="card-title">Login</h4>
                <p class="text-muted">Please enter your credentials to log in.</p>
              </header>

              <form @submit.prevent="submitForm">
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    placeholder="name@example.com"
                    v-model="form.email"
                    required
                  />
                </div>

                <div class="mb-4">
                  <label for="password" class="form-label">Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    placeholder="Enter your password"
                    v-model="form.password"
                    required
                  />
                </div>

                <div class="d-grid">
                  <button type="submit" class="btn btn-lg btn-login">
                    Login
                  </button>
                </div>
              </form>
            </div>
          </article>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* 이 컴포넌트에만 적용되는 스타일 */
.card-title {
  font-weight: 600;
}

/* 커스텀 버튼 스타일 */
.btn-login {
  background-color: #212529;
  border-color: #212529;
  color: white;
}

.btn-login:hover {
  background-color: #343a40;
  border-color: #343a40;
}
</style>