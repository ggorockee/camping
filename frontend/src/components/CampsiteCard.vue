<script setup>
import { ref, onMounted } from 'vue';
import { render } from 'timeago.js';

defineProps({
  campsite: {
    type: Object,
    required: true,
  },
});

const timeagoElement = ref(null);

onMounted(() => {
  if (timeagoElement.value) {
    render(timeagoElement.value);
  }
});
</script>

<template>
  <article class="card mb-4">
    <header class="card-header">
      <div class="card-meta">
        <time
          ref="timeagoElement"
          class="timeago"
          :datetime="campsite.created_at"
        >{{ campsite.created_at }}</time>
        in {{ campsite.address }}
      </div>
      <a href="#">
        <h4 class="card-title">{{ campsite.name }}</h4>
      </a>
    </header>
    <a href="#">
      <img
        class="card-img"
        :src="campsite.thumbnail_url || '/img/articles/2.jpg'"
        :alt="campsite.name"
      />
    </a>
    <div class="card-body">
      <p class="card-text">
        {{ campsite.description }}
      </p>
    </div>
  </article>
</template>

<style scoped>
.card-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>