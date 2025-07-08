<!-- src/views/HomeView.vue -->
<script setup lang="ts">
import CardList from '@/components/CardList.vue'
import type { CardItem } from '@/components/CardList.vue'

// 샘플 데이터 (실제론 API 호출이나 스토어 데이터 사용)
const items: CardItem[] = [
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTQwMjkwNjAxMDQ4MjU1ODA1MA==/original/13f32aa4-22e2-43cc-9ab7-f6c3fcde1cb3.jpeg?im_w=1200',
    title: '서울의 부티크 호텔',
    dateRange: '8월 15일~17일',
    price: '₩51,353',
    nights: 2,
    rating: 4.88,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  {
    imageSrc:
      'https://a0.muscache.com/im/pictures/hosting/Hosting-1052369788257986423/original/c46d29b3-0c51-4cd4-9324-145fb3988c2d.jpeg?im_w=1200',
    title: '서울의 아파트',
    dateRange: '3월 6일~8일',
    price: '₩79,883',
    nights: 2,
    rating: 4.96,
    guestPreferred: true,
  },
  // ...다른 아이템들
]
</script>

<template>
  <div>
    <!-- 기존 헤더 등 컴포넌트 -->
    <AppHeader />

    <main class="pt-16 px-6">
      <section class="mb-8">
        <CardList :items="items" />
      </section>
    </main>
  </div>
</template>
