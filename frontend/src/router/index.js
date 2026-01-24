import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/main',
    redirect: '/home'
  },
  // 基础知识模块路由
  {
    path: '/basic/zi',
    name: 'HanziList',
    component: () => import('../views/basic/HanziList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/basic/ciyu',
    name: 'CiyuList',
    component: () => import('../views/basic/CiyuList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ciyu',
    redirect: '/basic/ciyu'
  },

  {
    path: '/basic/chengyu',
    name: 'ChengyuList',
    component: () => import('../views/basic/ChengyuList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chengyu',
    redirect: '/basic/chengyu'
  },


  // 题目模块路由
  {
    path: '/exam/content-system',
    name: 'ContentSystemExercises',
    component: () => import('../views/exam/ContentSystemExercises.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/scenario-system',
    name: 'ScenarioSystemExercises',
    component: () => import('../views/exam/ScenarioSystemExercises.vue'),
    meta: { requiresAuth: true }
  },
  // 音视频模块路由
  {
    path: '/media/audio',
    name: 'AudioList',
    component: () => import('../views/media/AudioList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/media/video',
    name: 'VideoList',
    component: () => import('../views/media/VideoList.vue'),
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
    next('/home')
  } else {
    next()
  }
})

export default router