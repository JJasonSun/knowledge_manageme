<template>
  <div class="container">
    <div class="login-container">
      <h2>中文教育资源管理系统</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">用户名:</label>
          <input 
            v-model="loginForm.username" 
            type="text" 
            class="form-input" 
            required
          >
        </div>
        
        <div class="form-group">
          <label class="form-label">密码:</label>
          <input 
            v-model="loginForm.password" 
            type="password" 
            class="form-input" 
            required
          >
        </div>
        
        <div v-if="error" class="form-group error">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div style="margin-top: 20px; font-size: 12px; color: #666;">
        <p>测试账号:</p>
        <p>管理员: admin / 123456</p>
        <p>老师1: teacher1 / 123456</p>
        <p>老师2: teacher2 / 123456</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const loginForm = ref({
      username: '',
      password: ''
    })
    
    const loading = ref(false)
    const error = ref('')
    
    const handleLogin = async () => {
      loading.value = true
      error.value = ''
      
      const result = await authStore.login(loginForm.value.username, loginForm.value.password)
      
      if (result.success) {
        router.push('/home')
      } else {
        error.value = result.error
      }
      
      loading.value = false
    }
    
    return {
      loginForm,
      loading,
      error,
      handleLogin
    }
  }
}
</script>