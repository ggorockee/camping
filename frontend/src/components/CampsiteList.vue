<script setup>
// nextTick과 render는 더 이상 필요 없으므로 import에서 제거합니다.
import { ref, onMounted } from 'vue';
import CampsiteCard from '@/components/CampsiteCard.vue';
import apiClient from '@/api/index.js';

const campsites = ref([]);

const fetchCampsites = async () => {
  try {
    const response = await apiClient.get('/campsites/');
    campsites.value = response.data.results;

    // ✅ nextTick과 render(timeago) 관련 코드를 모두 삭제합니다.
    // 자식 컴포넌트가 각자 알아서 처리하므로 부모는 신경쓰지 않아도 됩니다.

  } catch (error) {
    console.error('캠핑장 데이터를 불러오는 중 오류가 발생했습니다:', error);
  }
};

onMounted(() => {
  fetchCampsites();
});
</script>

<template>
  <main class="main pt-4">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-9 main-content">
          <div class="row">
            <div
              v-for="campsite in campsites"
              :key="campsite.id"
              class="col-md-4"
            >
              <CampsiteCard :campsite="campsite" />
            </div>
          </div>
        </div>
        <div class="col-md-3 ms-auto">
          <aside class="sidebar sidebar-sticky">
            </aside>
        </div>
      </div>
    </div>
  </main>
</template>
<style scoped>
.main-content {
  position: relative;
}
</style>