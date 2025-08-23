import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/ChatView.vue'),
    },
    {
      path: '/auth/login',
      name: 'login',
      component: () => import('../views/auth/Login.vue'),
    },
    {
      path: '/auth/register',
      name: 'register',
      component: () => import('../views/auth/Register.vue'),
    },
    {
      path: '/account/profile',
      name: 'account-profile',
      component: () => import('../views/account/Profile.vue'),
    },
    {
      path: '/swipe',
      name: 'swipe',
      component: () => import('../views/swipe/Swipe.vue'),
    },
    {
      path: '/household/week',
      name: 'menu-plan',
      component: () => import('../views/household/WeekPlan.vue'),
    },
  ],
})

export default router
