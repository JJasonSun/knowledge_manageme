<template>
  <div>
    <Header />
    <div class="container">
      <h2>欢迎使用中文教育资源管理系统</h2>
      <div style="margin-top: 20px;">
        <p>当前用户: {{ authStore.user?.username }} ({{ authStore.user?.role }})</p>
        <div style="margin-top: 20px;">
          <router-link to="/chengyu" class="btn btn-primary" style="margin-right: 10px;">
            成语管理
          </router-link>
          <router-link to="/ciyu" class="btn btn-primary">
            词语管理
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import Header from '../components/Header.vue'

export default {
  name: 'Main',
  components: {
    Header
  },
  setup() {
    const authStore = useAuthStore()
    
    return {
      authStore
    }
  }
}
</script>