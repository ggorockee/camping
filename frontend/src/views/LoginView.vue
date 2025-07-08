<script setup>
import { reactive } from "vue";
import { useAuthStore } from "@/stores/auth"; // 1. auth 스토어 import

const authStore = useAuthStore(); // 2. 스토어 인스턴스 생성
const form = reactive({
  email: "",
  password: "",
});
// 폼 제출 시 실행될 함수
async function submitForm() {
  try {
    // 3. 스토어의 login 액션을 호출하고 form 데이터를 전달
    await authStore.login(form);

    alert("Login successful! Welcome back.");
  } catch (error) {
    console.error("Login failed:", error.response);

    // 에러 처리는 기존과 동일하게 유지
    if (error.response && error.response.data) {
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
                <p class="text-muted">
                  Please enter your credentials to log in.
                </p>
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