<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <h2>视频资源管理</h2>
        <div class="header-actions">
          <div class="permission-info">
            <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
          </div>
          <button class="btn btn-primary" @click="showCreateModal = true">+ 添加视频</button>
        </div>
      </div>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          placeholder="搜索视频资源..."
        >
      </div>
      
      <div class="placeholder-content">
        <div class="placeholder-icon">🎬</div>
        <h3>功能开发中</h3>
        <p>视频资源管理模块正在开发中，敬请期待！</p>
        <div class="placeholder-tips">
          <p>计划功能：</p>
          <ul>
            <li>视频文件上传与管理</li>
            <li>视频元数据编辑（标题、时长、格式、分辨率等）</li>
            <li>视频在线播放</li>
            <li>视频缩略图预览</li>
            <li>视频分类与标签</li>
            <li>与汉字、词语、成语的关联</li>
          </ul>
        </div>
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

export default {
  name: 'VideoList',
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h2 {
  margin: 0;
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.permission-info {
  color: #666;
  background-color: #fff3cd;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ffc107;
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
  border-color: #667eea;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
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
  border: 2px dashed #ddd;
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

.placeholder-tips {
  text-align: left;
  max-width: 500px;
  margin: 0 auto;
  background-color: white;
  padding: 25px;
  border-radius: 8px;
}

.placeholder-tips p {
  color: #667eea;
  font-weight: bold;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.placeholder-tips ul {
  list-style: none;
  padding: 0;
}

.placeholder-tips li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 25px;
}

.placeholder-tips li:before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #28a745;
  font-weight: bold;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
