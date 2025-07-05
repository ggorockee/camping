<script setup>
import { reactive } from "vue";
import apiClient from "@/api/index.js";
import { useRouter } from "vue-router";

const router = useRouter(); // 페이지 이동을 위해 router 인스턴스 생성

// Reactive object to manage form data via v-model
const form = reactive({
  email: "",
  nickname: "",
  password: "",
  passwordConfirm: "",
});

// Function to be executed on form submission
async function submitForm() {
  // 1. Check if the passwords match
  if (form.password !== form.passwordConfirm) {
    alert("Passwords do not match.");
    return; // Stop the function execution
  }

  // API로 보낼 데이터에서 passwordConfirm 필드 제외
  const { passwordConfirm, ...payload } = form;

  try {
    // 2. Django API로 회원가입 요청
    await apiClient.post("/users/register/", payload);
    alert("Welcome! Your registration was successful.");
    // 3. 성공 시 로그인 페이지로 이동
    router.push("/users/login");
  } catch (error) {
    console.error("Registration failed:", error.response);
    if (error.response && error.response.data) {
      // Django에서 보낸 유효성 검사 에러 메시지를 alert으로 표시
      alert(`Registration failed: ${JSON.stringify(error.response.data)}`);
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
                <h4 class="card-title">Sign Up</h4>
                <p class="text-muted">Welcome to ggorockee!</p>
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

                <div class="mb-3">
                  <label for="nickname" class="form-label"
                    >Nickname <span class="text-muted">(Optional)</span></label
                  >
                  <input
                    type="text"
                    class="form-control"
                    id="nickname"
                    placeholder="Enter your desired nickname"
                    v-model="form.nickname"
                  />
                </div>

                <div class="mb-3">
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

                <div class="mb-4">
                  <label for="password-confirm" class="form-label"
                    >Confirm Password</label
                  >
                  <input
                    type="password"
                    class="form-control"
                    id="password-confirm"
                    placeholder="Enter your password again"
                    v-model="form.passwordConfirm"
                    required
                  />
                </div>

                <div class="d-grid">
                  <button type="submit" class="btn btn-lg btn-signup">
                    Sign Up
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
/* Styles specific to this component */
.card-title {
  font-weight: 600;
}

/* Custom button style */
.btn-signup {
  background-color: #212529;
  border-color: #212529;
  color: white;
}

.btn-signup:hover {
  background-color: #343a40;
  border-color: #343a40;
}
</style>
