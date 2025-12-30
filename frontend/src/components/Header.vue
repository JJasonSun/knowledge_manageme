<template>
  <div class="header">
    <div class="title">中文教育资源管理系统</div>
    
    <div class="nav-links">
      <!-- 首页 -->
      <router-link to="/home" class="nav-link">首页</router-link>
      
      <!-- 汉字模块下拉菜单 -->
      <div class="dropdown" @mouseenter="showDropdown('hanzi')" @mouseleave="hideDropdown">
        <button class="nav-link dropdown-btn">
          汉字模块 <span class="arrow">▼</span>
        </button>
        <div class="dropdown-menu" :class="{ show: activeDropdown === 'hanzi' }">
          <router-link to="/hanzi/zi" class="dropdown-item">字</router-link>
          <router-link to="/hanzi/ciyu" class="dropdown-item">词</router-link>
          <router-link to="/hanzi/chengyu" class="dropdown-item">成语</router-link>
        </div>
      </div>
      
      <!-- 题目模块下拉菜单 -->
      <div class="dropdown" @mouseenter="showDropdown('exam')" @mouseleave="hideDropdown">
        <button class="nav-link dropdown-btn">
          题目模块 <span class="arrow">▼</span>
        </button>
        <div class="dropdown-menu dropdown-menu-large" :class="{ show: activeDropdown === 'exam' }">
          <div class="dropdown-column">
            <div class="dropdown-title">HSK</div>
            <router-link to="/exam/hsk/listening" class="dropdown-item">听力题</router-link>
            <router-link to="/exam/hsk/reading" class="dropdown-item">阅读题</router-link>
            <router-link to="/exam/hsk/writing" class="dropdown-item">书写题</router-link>
            <router-link to="/exam/hsk/essay" class="dropdown-item">写作题</router-link>
          </div>
          <div class="dropdown-column">
            <div class="dropdown-title">YCT</div>
            <router-link to="/exam/yct/listening" class="dropdown-item">听力题</router-link>
            <router-link to="/exam/yct/reading" class="dropdown-item">阅读题</router-link>
            <router-link to="/exam/yct/writing" class="dropdown-item">书写题</router-link>
            <router-link to="/exam/yct/essay" class="dropdown-item">写作题</router-link>
          </div>
        </div>
      </div>
      
      <!-- 音视频资源模块下拉菜单 -->
      <div class="dropdown" @mouseenter="showDropdown('media')" @mouseleave="hideDropdown">
        <button class="nav-link dropdown-btn">
          音视频模块 <span class="arrow">▼</span>
        </button>
        <div class="dropdown-menu" :class="{ show: activeDropdown === 'media' }">
          <router-link to="/media/audio" class="dropdown-item">音频</router-link>
          <router-link to="/media/video" class="dropdown-item">视频</router-link>
        </div>
      </div>
    </div>
    
    <div class="user-info">
      <span>{{ authStore.user?.username }} ({{ getRoleText(authStore.user?.role) }})</span>
      <button @click="handleLogout" class="btn">退出登录</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Header',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const activeDropdown = ref(null)
    
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
    
    const showDropdown = (dropdown) => {
      activeDropdown.value = dropdown
    }
    
    const hideDropdown = () => {
      activeDropdown.value = null
    }
    
    return {
      authStore,
      activeDropdown,
      getRoleText,
      handleLogout,
      showDropdown,
      hideDropdown
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 1.4rem;
  font-weight: bold;
  color: white;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-link {
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.3s;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.nav-link:hover, .nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.dropdown {
  position: relative;
}

.dropdown-btn {
  display: flex;
  align-items: center;
  gap: 5px;
}

.arrow {
  font-size: 0.8rem;
  transition: transform 0.3s;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  min-width: 120px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1000;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu-large {
  display: flex;
  gap: 30px;
  min-width: 300px;
  padding: 10px 20px;
}

.dropdown-column {
  display: flex;
  flex-direction: column;
}

.dropdown-title {
  color: #667eea;
  font-weight: bold;
  padding: 8px 0;
  font-size: 0.9rem;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 8px;
}

.dropdown-item {
  display: block;
  padding: 10px 15px;
  color: #333;
  text-decoration: none;
  transition: all 0.2s;
  border-radius: 4px;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
  color: #667eea;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
  color: white;
}

.btn {
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>