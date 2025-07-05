<script setup>
import { reactive } from "vue";

// Reactive object to manage form data via v-model
const form = reactive({
  email: "",
  nickname: "",
  password: "",
  passwordConfirm: "",
});

// Function to be executed on form submission
function submitForm() {
  // 1. Check if the passwords match
  if (form.password !== form.passwordConfirm) {
    alert("Passwords do not match.");
    return; // Stop the function execution
  }

  // 2. Send the data to the server (API call)
  // You would add your API call logic here using axios or fetch.
  console.log("Form data to be submitted:", form);
  alert(
    "Registration form submitted. (In a real app, an API call would be made)"
  );
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
