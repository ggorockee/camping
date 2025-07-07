<template>
  <v-app-bar app color="white" flat density="comfortable" class="border-b">
    <v-container class="d-flex align-center pa-0">
      <v-btn v-if="route.name !== 'home'" icon @click="goBack">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-app-bar-nav-icon
        v-else
        @click.stop="drawer = !drawer"
        class="d-md-none"
      ></v-app-bar-nav-icon>

      <v-app-bar-title
        class="font-weight-bold text-h5 ms-md-4"
        @click="goHome"
        style="cursor: pointer"
      >
        ggorockee
      </v-app-bar-title>

      <v-spacer></v-spacer>
    </v-container>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" temporary app>
    <v-list nav> </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router"; // ✅ useRoute import
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute(); // ✅ 현재 라우트 정보를 가져오기 위해 추가
const drawer = ref(false);

const goHome = () => router.push({ name: "home" });
const goBack = () => router.back(); // ✅ 뒤로가기 기능 함수 추가
const handleLogout = () => authStore.logout("/");
</script>
