<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <h2>字管理</h2>
        <div class="header-actions">
          <div class="permission-info">
            <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
          </div>
          <button class="btn btn-primary" @click="showCreateModal = true">+ 添加汉字</button>
        </div>
      </div>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          placeholder="搜索汉字..."
        >
      </div>
      
      <div class="placeholder-content">
        <div class="placeholder-icon">📚</div>
        <h3>功能开发中</h3>
        <p>汉字管理模块正在开发中，敬请期待！</p>
        <div class="placeholder-tips">
          <p>计划功能：</p>
          <ul>
            <li>汉字基本信息管理（字形、拼音、笔画等）</li>
            <li>汉字部件拆解与分析</li>
            <li>汉字书写顺序演示</li>
            <li>汉字组词与例句</li>
          </ul>
        </div>
      </div>
      
      <!-- 分页（预留） -->
      <div class="pagination" v-if="false">
        <button class="btn" disabled>首页</button>
        <button class="btn" disabled>上一页</button>
        <div class="page-jump">
          <span>第</span>
          <input type="number" value="1" class="page-input">
          <span>页，共 1 页</span>
        </div>
        <button class="btn" disabled>下一页</button>
        <button class="btn" disabled>末页</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Header from '../../components/Header.vue'

export default {
  name: 'HanziList',
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

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 30px;
}

.page-jump {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-input {
  width: 60px;
  padding: 8px;
  text-align: center;
  border: 2px solid #ddd;
  border-radius: 6px;
}
</style>
