<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <h2>{{ title }}</h2>
        <div class="header-actions">
          <div class="permission-info">
            <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
          </div>
          <button class="btn btn-add" @click="showCreateModal = true">+ 添加{{ typeName }}</button>
        </div>
      </div>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          :placeholder="`搜索${typeName}...`"
        >
      </div>
      
      <table class="table" v-if="!loading && list.length > 0">
        <thead>
          <tr>
            <th>题号</th>
            <th>内容</th>
            <th>难度</th>
            <th>来源</th>
            <th>创建者</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in list" :key="item.id">
            <td>{{ item.id }}</td>
            <td class="text-ellipsis">{{ item.content }}</td>
            <td>
              <span class="difficulty-badge" :class="getDifficultyClass(item.difficulty)">
                {{ getDifficultyText(item.difficulty) }}
              </span>
            </td>
            <td>{{ item.source || '-' }}</td>
            <td>
              <span class="status-pill owner-pill" :class="getOwnerClass(item)">
                {{ getOwnerText(item.created_by) }}
              </span>
            </td>
            <td>
              <div class="action-btns">
                <button v-if="canModify(item)" class="btn-small" @click="openEditModal(item)">编辑</button>
                <button v-if="canModify(item)" class="btn-small btn-danger" @click="handleDelete(item)">删除</button>
                <span v-if="!canModify(item)" class="text-muted">-</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="loading" class="loading-text">加载中...</div>
      <div v-if="!loading && list.length === 0" class="empty-text">
        <div class="placeholder-content">
          <div class="placeholder-icon">📝</div>
          <h3>{{ typeName }}管理</h3>
          <p>{{ typeName }}模块正在开发中，敬请期待！</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Header from '../../components/Header.vue'
import { useAuthStore } from '../../stores/auth'

export default {
  name: 'ExamTemplate',
  components: {
    Header
  },
  props: {
    examType: {
      type: String,
      required: true  // HSK 或 YCT
    },
    questionType: {
      type: String,
      required: true  // listening, reading, writing, essay
    },
    title: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const authStore = useAuthStore()
    const searchQuery = ref('')
    const showCreateModal = ref(false)
    const loading = ref(false)
    const list = ref([])
    
    const typeName = {
      'listening': '听力题',
      'reading': '阅读题',
      'writing': '书写题',
      'essay': '写作题'
    }[props.questionType]
    
    const getDifficultyText = (difficulty) => {
      const map = {
        'easy': '简单',
        'medium': '中等',
        'hard': '困难'
      }
      return map[difficulty] || difficulty
    }
    
    const getDifficultyClass = (difficulty) => {
      const map = {
        'easy': 'easy',
        'medium': 'medium',
        'hard': 'hard'
      }
      return map[difficulty] || ''
    }
    
    const getOwnerText = (createdBy) => {
      if (!createdBy || createdBy === 'system') return '系统'
      if (createdBy === 'admin') return '管理员'
      if (createdBy === authStore.user?.username) return '我的'
      return createdBy
    }
    
    const getOwnerClass = (item) => {
      if (item.created_by === authStore.user?.username) return 'owner-me'
      if (item.created_by === 'admin') return 'owner-admin'
      return 'owner-system'
    }
    
    const canModify = (item) => {
      return item.created_by === authStore.user?.username
    }
    
    const openEditModal = (item) => {
      // 编辑逻辑
      console.log('Edit item:', item)
    }
    
    const handleDelete = (item) => {
      // 删除逻辑
      console.log('Delete item:', item)
    }
    
    return {
      authStore,
      searchQuery,
      showCreateModal,
      loading,
      list,
      typeName,
      getDifficultyText,
      getDifficultyClass,
      getOwnerText,
      getOwnerClass,
      canModify,
      openEditModal,
      handleDelete
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

.btn-danger {
  background-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table thead {
  background: linear-gradient(135deg, #81c784 0%, #66bb6a 100%);
  color: white;
}

.table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
}

.table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}

.text-ellipsis {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.difficulty-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.difficulty-badge.easy {
  background-color: #d4edda;
  color: #155724;
}

.difficulty-badge.medium {
  background-color: #fff3cd;
  color: #856404;
}

.difficulty-badge.hard {
  background-color: #f8d7da;
  color: #721c24;
}

.owner-pill {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.owner-me {
  background-color: #cce5ff;
  color: #004085;
}

.owner-admin {
  background-color: #e2e3e5;
  color: #383d41;
}

.owner-system {
  background-color: #d6d8db;
  color: #1b1e21;
}

.action-btns {
  display: flex;
  align-items: center;
}

.text-muted {
  color: #6c757d;
}

.loading-text,
.empty-text {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.placeholder-content {
  background-color: #f9f9f9;

  border-radius: 12px;
  padding: 40px;
  text-align: center;
}


.placeholder-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.placeholder-content h3 {
  margin: 0;
  font-size: 1.4rem;
}

.placeholder-content p {
  margin: 8px 0 0;
  color: #6c757d;
}

</style>
