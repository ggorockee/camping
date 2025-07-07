<script setup>
import { RouterView } from "vue-router";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import AppHeader from "@/components/AppHeader.vue";

const authStore = useAuthStore();

onMounted(() => {
  if (authStore.accessToken) {
    authStore.fetchUser();
  }
});
</script>

<template>
  <v-app>
    <app-header />

    <v-main>
      <router-view />
    </v-main>

    <v-btn
      v-if="authStore.isAuthenticated"
      :to="{ name: 'campsite-create' }"
      icon="mdi-plus"
      color="primary"
      size="x-large"
      position="fixed"
      location="bottom right"
      class="ma-8"
      elevation="8"
      aria-label="새 캠핑장 등록"
    ></v-btn>

    <v-footer class="d-flex flex-column pa-0" app>
      <div class="bg-grey-darken-3 d-flex w-100 align-center px-4 py-2">
        <strong>ggorockee camping</strong>
        <v-spacer></v-spacer>
      </div>
      <div class="px-4 py-2 bg-black text-center w-100 text-caption">
        &copy; {{ new Date().getFullYear() }} Milo 2022, All rights reserved
      </div>
    </v-footer>
  </v-app>
</template>

<style scoped>
/* App.vue에만 필요한 스타일 */
</style>
