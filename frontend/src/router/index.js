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
  // 汉字模块路由
  {
    path: '/hanzi/zi',
    name: 'HanziList',
    component: () => import('../views/hanzi/HanziList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/hanzi/ciyu',
    name: 'CiyuList',
    component: () => import('../views/CiyuList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ciyu',
    redirect: '/hanzi/ciyu'
  },
  {
    path: '/hanzi/chengyu',
    name: 'ChengyuList',
    component: () => import('../views/ChengyuList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chengyu',
    redirect: '/hanzi/chengyu'
  },
  // 题目模块路由 - HSK
  {
    path: '/exam/hsk/listening',
    name: 'HSKListening',
    component: () => import('../views/exam/HSKListening.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/hsk/reading',
    name: 'HSKReading',
    component: () => import('../views/exam/HSKReading.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/hsk/writing',
    name: 'HSKWriting',
    component: () => import('../views/exam/HSKWriting.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/hsk/essay',
    name: 'HSKEssay',
    component: () => import('../views/exam/HSKEssay.vue'),
    meta: { requiresAuth: true }
  },
  // 题目模块路由 - YCT
  {
    path: '/exam/yct/listening',
    name: 'YCTListening',
    component: () => import('../views/exam/YCTListening.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/yct/reading',
    name: 'YCTReading',
    component: () => import('../views/exam/YCTReading.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/yct/writing',
    name: 'YCTWriting',
    component: () => import('../views/exam/YCTWriting.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam/yct/essay',
    name: 'YCTEssay',
    component: () => import('../views/exam/YCTEssay.vue'),
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