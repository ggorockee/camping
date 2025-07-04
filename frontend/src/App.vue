<script setup>
import { RouterLink, RouterView } from "vue-router";
import { ref } from "vue"; // ref

const isSearchActive = ref(false);
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-light bg-white absolute-top">
      <div class="container">
        <button
          class="navbar-toggler order-2 order-md-1"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target=".navbar-collapse"
          aria-controls="navbar-left navbar-right"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div
          class="collapse navbar-collapse order-3 order-md-2"
          id="navbar-left"
        >
          <ul class="navbar-nav me-auto">
            <li class="nav-item dropdown active">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="dropdown01"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                >Home</a
              >
              <div class="dropdown-menu" aria-labelledby="dropdown01">
                <a class="dropdown-item" href="#">One column</a>
                <a class="dropdown-item" href="#">Two column</a>
              </div>
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="dropdown02"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                >Posts</a
              >
              <div class="dropdown-menu" aria-labelledby="dropdown02">
                <a class="dropdown-item" href="#">Image</a>
                <a class="dropdown-item" href="#">Video</a>
              </div>
            </li>
          </ul>
        </div>

        <RouterLink class="navbar-brand mx-auto order-1 order-md-3" to="/"
          >GGOROCKEE</RouterLink
        >

        <div
          class="collapse navbar-collapse order-4 order-md-4"
          id="navbar-right"
        >
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/contact">Contact</RouterLink>
            </li>
          </ul>

          <form
            class="form-inline"
            role="search"
            :class="{ 'is-active': isSearchActive }"
            @focusin="isSearchActive = true"
            @focusout="isSearchActive = false"
          >
            <input
              class="search js-search form-control form-control-rounded me-sm-2"
              type="text"
              title="Enter search query here.."
              placeholder="Search.."
              aria-label="Search"
            />
          </form>
        </div>
      </div>
    </nav>
  </header>

  <RouterView />
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
