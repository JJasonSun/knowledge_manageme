import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/main',
    name: 'Main',
    component: () => import('../views/Main.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chengyu',
    name: 'ChengyuList',
    component: () => import('../views/ChengyuList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ciyu',
    name: 'CiyuList',
    component: () => import('../views/CiyuList.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/main')
  } else {
    next()
  }
})

export default router