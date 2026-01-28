<template>
  <div>
    <Header />
    <div class="container">
      <PageHeader
        icon="🎬"
        title="视频资源管理"
        subtitle="视频资源库"
        variant="orange"
        :showAddButton="true"
        addButtonText="添加视频"
        :showPermissionTip="true"
        @add="showCreateModal = true"
      />
      
      <SearchBar
        v-model="searchQuery"
        placeholder="搜索视频资源..."
        variant="orange"
      />
      
      <div class="placeholder-content">
        <div class="placeholder-icon">🎬</div>
        <h3>功能开发中</h3>
        <p>视频资源管理模块正在开发中，敬请期待！</p>
      </div>
      
      <!-- 示例视频卡片（预留） -->
      <div class="media-grid" v-if="false">
        <div class="media-card" v-for="i in 6" :key="i">
          <div class="media-thumbnail">
            <div class="media-icon">🎬</div>
            <div class="play-overlay">▶</div>
          </div>
          <div class="media-info">
            <div class="media-title">示例视频 {{ i }}</div>
            <div class="media-meta">时长: 00:00 | 格式: MP4 | 分辨率: 1080p</div>
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
import PageHeader from '../../components/PageHeader.vue'
import SearchBar from '../../components/SearchBar.vue'

export default {
  name: 'VideoList',
  components: {
    Header,
    PageHeader,
    SearchBar
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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.media-card {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.media-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.media-thumbnail {
  position: relative;
  height: 180px;
  background: linear-gradient(135deg, #81c784 0%, #66bb6a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-icon {
  font-size: 64px;
  color: white;
  opacity: 0.8;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 48px;
  opacity: 0;
  transition: opacity 0.3s;
  cursor: pointer;
}

.media-thumbnail:hover .play-overlay {
  opacity: 1;
}

.media-info {
  padding: 20px;
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
  padding: 0 20px 20px 20px;
}
</style>
