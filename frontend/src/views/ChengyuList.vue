<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <h2>成语管理</h2>
        <div class="header-actions">
          <div class="permission-info">
            <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
          </div>
          <button class="btn btn-primary" @click="showCreateModal = true">+ 添加成语</button>
        </div>
      </div>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          placeholder="搜索成语..."
        >
      </div>
      
      <table class="table" v-if="!loading && chengyuList.length > 0">
        <thead>
          <tr>
            <th>成语</th>
            <th>拼音</th>
            <th>情感色彩</th>
            <th>解释</th>
            <th>创建者</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in chengyuList" :key="item.id">
            <td>{{ item.chengyu }}</td>
            <td>{{ item.pinyin }}</td>
            <td>{{ item.emotion || '-' }}</td>
            <td class="text-ellipsis">{{ item.explanation }}</td>
            <td>
              <span class="owner-pill" :class="getOwnerClass(item)">
                {{ getOwnerText(item.created_by) }}
              </span>
            </td>
            <td>
              <div class="action-btns">
                <button v-if="item.can_edit === true" class="btn-small" @click="openEditModal(item)">编辑</button>
                <button v-if="item.can_delete === true" class="btn-small btn-danger" @click="handleDelete(item)">删除</button>
                <span v-if="item.can_edit !== true && item.can_delete !== true" class="text-muted">-</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="loading" class="loading-text">加载中...</div>
      <div v-if="!loading && chengyuList.length === 0" class="empty-text">暂无数据</div>
      
      <div class="pagination" v-if="totalPages > 1">
        <button class="btn" @click="goToPage(1)" :disabled="currentPage <= 1">首页</button>
        <button class="btn" @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1">上一页</button>
        
        <div class="page-jump">
          <span>第</span>
          <input 
            v-model.number="jumpPage" 
            type="number" 
            :min="1" 
            :max="totalPages"
            class="page-input"
            @keyup.enter="handleJumpPage"
          >
          <span>页，共 {{ totalPages }} 页</span>
          <button class="btn btn-small" @click="handleJumpPage">跳转</button>
        </div>
        
        <button class="btn" @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages">下一页</button>
        <button class="btn" @click="goToPage(totalPages)" :disabled="currentPage >= totalPages">末页</button>
      </div>
    </div>

    <!-- 创建/编辑弹窗 -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-wide">
        <h3>{{ showEditModal ? '编辑成语' : '添加成语' }}</h3>
        <form @submit.prevent="showEditModal ? handleUpdate() : handleCreate()">
          <div class="form-grid">
            <div class="form-column">
              <div class="form-group">
                <label class="form-label">成语 *</label>
                <input v-model="formData.chengyu" type="text" class="form-input" required :disabled="showEditModal">
              </div>
              <div class="form-group">
                <label class="form-label">拼音</label>
                <input v-model="formData.pinyin" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label class="form-label">注音</label>
                <input v-model="formData.zhuyin" type="text" class="form-input">
              </div>
              <div class="form-group">
                <label class="form-label">情感色彩</label>
                <select v-model="formData.emotion" class="form-input">
                  <option value="">请选择</option>
                  <option value="褒义">褒义</option>
                  <option value="贬义">贬义</option>
                  <option value="中性">中性</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">翻译</label>
                <textarea v-model="formData.translation" class="form-input" rows="2"></textarea>
              </div>
            </div>
            
            <div class="form-column">
              <div class="form-group">
                <label class="form-label">解释</label>
                <textarea v-model="formData.explanation" class="form-input" rows="3"></textarea>
              </div>
              <div class="form-group">
                <label class="form-label">来源</label>
                <textarea v-model="formData.source" class="form-input" rows="2"></textarea>
              </div>
              <div class="form-group">
                <label class="form-label">用法</label>
                <textarea v-model="formData.usage" class="form-input" rows="2"></textarea>
              </div>
              <div class="form-group">
                <label class="form-label">例句</label>
                <textarea v-model="formData.example" class="form-input" rows="2"></textarea>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="button" class="btn" @click="closeModal">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? '提交中...' : '确定' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Header from '../components/Header.vue'
import request from '../utils/request'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'ChengyuList',
  components: { Header },
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    const chengyuList = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(20)
    const total = ref(0)
    const jumpPage = ref(1)
    
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const submitting = ref(false)
    const editingId = ref(null)
    const searchTimeout = ref(null)
    
    const formData = ref({
      chengyu: '',
      pinyin: '',
      zhuyin: '',
      emotion: '',
      explanation: '',
      source: '',
      usage: '',
      example: '',
      translation: ''
    })
    
    const totalPages = computed(() => Math.ceil(total.value / pageSize.value))
    
    const fetchChengyu = async () => {
      loading.value = true
      try {
        const params = { page: currentPage.value, size: pageSize.value }
        if (searchQuery.value) params.search = searchQuery.value
        
        const response = await request.get('/v1/chengyu', { params })
        chengyuList.value = response.data.items
        total.value = response.data.total
      } catch (error) {
        console.error('获取成语列表失败:', error)
        alert('获取数据失败')
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      // 清除之前的定时器
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
      }
      
      // 设置新的定时器，500ms 后执行搜索
      searchTimeout.value = setTimeout(() => {
        currentPage.value = 1
        fetchChengyu()
      }, 500)
    }
    
    // 监听搜索框变化
    watch(searchQuery, () => {
      handleSearch()
    })
    
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        jumpPage.value = page
        fetchChengyu()
      }
    }

    const handleJumpPage = () => {
      if (jumpPage.value >= 1 && jumpPage.value <= totalPages.value) {
        goToPage(jumpPage.value)
      } else {
        alert(`请输入1到${totalPages.value}之间的页码`)
        jumpPage.value = currentPage.value
      }
    }

    const resetForm = () => {
      formData.value = { 
        chengyu: '', pinyin: '', zhuyin: '', emotion: '', 
        explanation: '', source: '', usage: '', example: '', translation: '' 
      }
      editingId.value = null
    }

    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      resetForm()
    }

    const openEditModal = (item) => {
      formData.value = {
        chengyu: item.chengyu,
        pinyin: item.pinyin,
        zhuyin: item.zhuyin || '',
        emotion: item.emotion || '',
        explanation: item.explanation,
        source: item.source || '',
        usage: item.usage || '',
        example: item.example || '',
        translation: item.translation || ''
      }
      editingId.value = item.id
      showEditModal.value = true
    }

    const handleCreate = async () => {
      submitting.value = true
      try {
        await request.post('/v1/chengyu', formData.value)
        alert('创建成功')
        closeModal()
        fetchChengyu()
      } catch (error) {
        alert(error.response?.data?.detail || '创建失败')
      } finally {
        submitting.value = false
      }
    }

    const handleUpdate = async () => {
      submitting.value = true
      try {
        const { chengyu, ...updateData } = formData.value
        await request.put(`/v1/chengyu/${editingId.value}`, updateData)
        alert('更新成功')
        closeModal()
        fetchChengyu()
      } catch (error) {
        alert(error.response?.data?.detail || '更新失败')
      } finally {
        submitting.value = false
      }
    }

    const handleDelete = async (item) => {
      if (!confirm(`确定要删除"${item.chengyu}"吗？`)) return
      try {
        await request.delete(`/v1/chengyu/${item.id}`)
        alert('删除成功')
        fetchChengyu()
      } catch (error) {
        console.error('删除失败:', error)
        alert(error.response?.data?.detail || '删除失败')
      }
    }

    const getOwnerText = (createdBy) => {
      if (!createdBy || createdBy === 'system') return '系统'
      if (createdBy === 'admin') return '管理员'
      return createdBy
    }

    const getOwnerClass = (item) => {
      return {
        'owner-pill--me': item.can_delete,
        'owner-pill--admin': item.created_by === 'admin',
        'owner-pill--system': !item.created_by || item.created_by === 'system'
      }
    }
    
    onMounted(() => {
      fetchChengyu()
    })
    
    return {
      authStore, chengyuList, loading, searchQuery, currentPage, totalPages, jumpPage,
      showCreateModal, showEditModal, submitting, formData,
      handleSearch, goToPage, handleJumpPage, openEditModal, closeModal,
      handleCreate, handleUpdate, handleDelete, getOwnerText, getOwnerClass
    }
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.permission-info {
  color: #666;
  font-style: italic;
}
.text-ellipsis {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.action-btns {
  display: flex;
  gap: 8px;
}
.btn-small {
  padding: 4px 12px;
  font-size: 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}
.btn-small:hover { background: #f5f5f5; }
.btn-danger { color: #dc3545; border-color: #dc3545; }
.btn-danger:hover { background: #dc3545; color: white; }
.text-muted { color: #999; font-size: 12px; }
.loading-text, .empty-text { text-align: center; padding: 40px; color: #666; }
.page-info { padding: 0 15px; }

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
}

.modal-wide {
  width: 800px;
  max-width: 95%;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 20px;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.modal h3 { margin-bottom: 20px; }
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.owner-pill--admin {
  background-color: #fff3e0;
  color: #e65100;
  border-color: #ffb74d;
}

.owner-pill--system {
  background-color: #f3e5f5;
  color: #7b1fa2;
  border-color: #ce93d8;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.page-jump {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 15px;
}

.page-input {
  width: 60px;
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}
</style>
