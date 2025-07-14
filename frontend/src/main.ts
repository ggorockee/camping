import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import apiClient from '@/api' // apiClient import

const app = createApp(App)

app.use(createPinia())
app.use(router)

const accessToken = localStorage.getItem('accessToken')
if (accessToken) {
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
}

app.mount('#app')
