<template>
  <div class="header">
    <div class="title">中文教育资源管理系统</div>
    
    <div class="nav-links">
      <router-link to="/main" class="nav-link">首页</router-link>
      <router-link to="/chengyu" class="nav-link">成语管理</router-link>
      <router-link to="/ciyu" class="nav-link">词语管理</router-link>
    </div>
    
    <div class="user-info">
      <span>{{ authStore.user?.username }} ({{ getRoleText(authStore.user?.role) }})</span>
      <button @click="handleLogout" class="btn">退出登录</button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Header',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const getRoleText = (role) => {
      const roleMap = {
        admin: '管理员',
        teacher: '老师'
      }
      return roleMap[role] || role
    }
    
    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return {
      authStore,
      getRoleText,
      handleLogout
    }
  }
}
</script>

<style scoped>
.nav-link.active {
  background-color: #007bff;
  color: white;
}
</style>