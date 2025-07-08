<template>
  <div class="col-span-1">
    <div class="relative">
      <!-- 부모에서 받은 image 필드 사용 -->
      <img
        :src="listing.image"
        class="w-full h-72 object-cover rounded-xl"
        alt="숙소 이미지"
      />
      <button class="absolute top-3 right-3 text-white">
        <i
          class="fa-regular fa-heart text-2xl"
          style="-webkit-text-stroke: 1px black;"
        ></i>
      </button>
      <div
        v-if="listing.isGuestFavorite"
        class="absolute top-3 left-3 bg-white px-2 py-1 rounded-md text-sm font-bold"
      >
        게스트 선호
      </div>
    </div>
    <div class="mt-2">
      <div class="flex justify-between items-start">
        <h3 class="font-bold text-gray-800">{{ listing.title }}</h3>
        <div class="flex items-center">
          <i class="fas fa-star text-sm mr-1"></i>
          <span class="text-sm">{{ listing.rating }}</span>
        </div>
      </div>
      <!-- 부모에서 받은 location 필드 사용 -->
      <p class="text-gray-500 text-sm">{{ listing.location }}</p>
      <p class="mt-1">
        <span class="font-bold">₩{{ listing.price.toLocaleString() }}</span>
        /박
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  listing: {
    type: Object,
    required: true,
    // { id, title, location, price, rating, image, isGuestFavorite? }
  },
});
</script>

<style scoped>
/* 카드 전용 스타일이 필요하면 여기에 */
</style>
