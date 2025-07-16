import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import CampSiteNew from '../views/CampSiteNew.vue'
import RegisterView from '../views/RegisterView.vue'
import CampSiteDetailView from '../views/CampSiteDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/new',
      name: 'new',
      component: CampSiteNew,
    },
    {
      path: '/campsites/:id', // :id 부분이 동적으로 변경됩니다.
      name: 'campsite-detail', // 이 이름으로 링크를 쉽게 만들 수 있습니다.
      component: () => import('@/views/CampSiteDetailView.vue'),
    },
  ],
})

export default router
