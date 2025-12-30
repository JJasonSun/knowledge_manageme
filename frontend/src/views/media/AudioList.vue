<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <h2>音频资源管理</h2>
        <div class="header-actions">
          <div class="permission-info">
            <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
          </div>
          <button class="btn btn-add" @click="showCreateModal = true">+ 添加音频</button>
        </div>
      </div>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          placeholder="搜索音频资源..."
        >
      </div>
      
      <div class="placeholder-content">
        <div class="placeholder-icon">🎵</div>
        <h3>功能开发中</h3>
        <p>音频资源管理模块正在开发中，敬请期待！</p>
      </div>
      
      <!-- 示例音频卡片（预留） -->
      <div class="media-grid" v-if="false">
        <div class="media-card" v-for="i in 6" :key="i">
          <div class="media-icon">🎵</div>
          <div class="media-info">
            <div class="media-title">示例音频 {{ i }}</div>
            <div class="media-meta">时长: 00:00 | 格式: MP3</div>
          </div>
          <div class="media-actions">
            <button class="btn-small">播放</button>
            <button class="btn-small">编辑</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Header from '../../components/Header.vue'

export default {
  name: 'AudioList',
  components: {
    Header
  },
  setup() {
    const searchQuery = ref('')
    const showCreateModal = ref(false)
    
    return {
      searchQuery,
      showCreateModal
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
}


.search-box {
  margin-bottom: 30px;
}

.search-input {
  width: 100%;
  padding: 12px 20px;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #66bb6a;
}


.btn-small {
  padding: 6px 12px;
  font-size: 0.9rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.btn-small:hover {
  background-color: #5a6268;
}

.placeholder-content {
  text-align: center;
  padding: 60px 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
}

.placeholder-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.placeholder-content h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.8rem;
}

.placeholder-content > p {
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.media-card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.media-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.media-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.media-info {
  margin-bottom: 15px;
}

.media-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-size: 1.1rem;
}

.media-meta {
  color: #666;
  font-size: 0.9rem;
}

.media-actions {
  display: flex;
  gap: 8px;
}
</style>
