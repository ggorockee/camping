<script setup>
import { RouterLink, RouterView } from "vue-router";
import { ref } from "vue"; // ref

const isSearchActive = ref(false);

// 로그인 상태 관리 ---
const isLoggedIn = ref(false); // true이면 로그인된 상태, false이면 로그아웃된 상태

// 실제 앱에서는 API 호출로 로그인/로그아웃을 처리
// 여기서는 상태 변경을 시뮬레이션하기 위한 함수
function login() {
  alert("로그인 되었습니다. (데모)");
  isLoggedIn.value = true;
}

function logout() {
  alert("로그아웃 되었습니다. (데모)");
  isLoggedIn.value = false;
}
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-light bg-white absolute-top">
      <div class="container">
        <div
          class="collapse navbar-collapse order-3 order-md-2"
          id="navbar-left"
        ></div>

        <RouterLink class="navbar-brand mx-auto order-1 order-md-3" to="/">
          ggorockee
        </RouterLink>

        <div
          class="collapse navbar-collapse order-4 order-md-4"
          id="navbar-right"
        >
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="page-about.html">About</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="page-contact.html">Contact</a>
            </li>

            <template v-if="!isLoggedIn">
              <li class="nav-item">
                <RouterLink to="/register" class="nav-link"
                  >register</RouterLink
                >
              </li>
              <li class="nav-item">
                <RouterLink to="/login" class="nav-link"
                  >login</RouterLink
                >
              </li>
            </template>

            <template v-else>
              <li class="nav-item">
                <a href="#" class="nav-link" @click.prevent="logout">logout</a>
              </li>
            </template>
          </ul>

          <form class="form-inline" role="search"></form>
        </div>
      </div>
    </nav>
  </header>

  <RouterView />

  <footer class="site-footer bg-dark">
    <div class="container">
      <ul class="nav justify-content-center">
        <li class="nav-item">
          <a class="nav-link" href="#">Privacy policy</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Terms</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Feedback</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Advertise</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="page-contact.html">Contact</a>
        </li>
      </ul>
      <div class="copy">
        &copy; Milo 2022<br />
        All rights reserved
      </div>
    </div>
  </footer>
</template>

<style scoped>
.form-inline .form-control {
  width: 100px;
  transition: width 0.25s ease-in-out;
}
.form-inline.is-active .form-control {
  width: 200px; /* 활성화 시 넓이 */
}
</style>
