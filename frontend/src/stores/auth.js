import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '../utils/request'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = ref(!!token.value)

  const login = async (username, password) => {
    try {
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)

      const response = await request.post('/v1/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })

      if (response.data.access_token) {
        token.value = response.data.access_token
        user.value = {
          username: response.data.user?.username || username,
          role: response.data.user?.role || 'user'
        }
        
        localStorage.setItem('token', token.value)
        localStorage.setItem('user', JSON.stringify(user.value))
        isAuthenticated.value = true

        return { success: true }
      } else {
        return { success: false, error: '登录失败' }
      }
    } catch (error) {
      console.error('登录错误:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || '登录失败，请检查用户名和密码'
      }
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout
  }
})
