<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <h2>词语管理</h2>
        <div class="header-actions">
          <div class="permission-info">
            <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
          </div>
          <button class="btn btn-primary" @click="showCreateModal = true">+ 添加词语</button>
        </div>
      </div>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          placeholder="搜索词语..."
        >
      </div>
      
      <table class="table" v-if="!loading && ciyuList.length > 0">
        <thead>
          <tr>
            <th>词语</th>
            <th>拼音</th>
            <th>词性</th>
            <th>常用程度</th>
            <th>定义</th>
            <th>创建者</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in ciyuList" :key="item.id">
            <td>{{ item.word }}</td>
            <td>{{ item.pinyin }}</td>
            <td>{{ item.part_of_speech || '-' }}</td>
            <td>
              <span v-if="item.is_common !== null" class="common-badge" :class="{ 'common': item.is_common }">
                {{ item.is_common ? '常用' : '非常用' }}
              </span>
              <span v-else>-</span>
            </td>
            <td class="text-ellipsis">{{ item.definition }}</td>
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
      <div v-if="!loading && ciyuList.length === 0" class="empty-text">暂无数据</div>
      
      <div class="pagination" v-if="totalPages > 1">
        <button class="btn" @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1">上一页</button>
        <span class="page-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
        <button class="btn" @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages">下一页</button>
      </div>
    </div>

    <!-- 创建/编辑弹窗 -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h3>{{ showEditModal ? '编辑词语' : '添加词语' }}</h3>
        <form @submit.prevent="showEditModal ? handleUpdate() : handleCreate()">
          <div class="form-group">
            <label class="form-label">词语 *</label>
            <input v-model="formData.word" type="text" class="form-input" required :disabled="showEditModal">
          </div>
          <div class="form-group">
            <label class="form-label">拼音 *</label>
            <input v-model="formData.pinyin" type="text" class="form-input" required>
          </div>
          <div class="form-group">
            <label class="form-label">注音</label>
            <input v-model="formData.zhuyin" type="text" class="form-input">
          </div>
          <div class="form-group">
            <label class="form-label">词性</label>
            <select v-model="formData.part_of_speech" class="form-input">
              <option value="">请选择</option>
              <option value="名词">名词</option>
              <option value="动词">动词</option>
              <option value="形容词">形容词</option>
              <option value="副词">副词</option>
              <option value="介词">介词</option>
              <option value="连词">连词</option>
              <option value="助词">助词</option>
              <option value="叹词">叹词</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">是否常用词</label>
            <select v-model="formData.is_common" class="form-input">
              <option :value="null">请选择</option>
              <option :value="true">常用词</option>
              <option :value="false">非常用词</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">定义 *</label>
            <textarea v-model="formData.definition" class="form-input" rows="3" required></textarea>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Header from '../components/Header.vue'
import request from '../utils/request'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'CiyuList',
  components: { Header },
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    const ciyuList = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(20)
    const total = ref(0)
    
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const submitting = ref(false)
    const editingId = ref(null)
    const searchTimeout = ref(null)
    
    const formData = ref({
      word: '',
      pinyin: '',
      zhuyin: '',
      part_of_speech: '',
      is_common: null,
      definition: ''
    })
    
    const totalPages = computed(() => Math.ceil(total.value / pageSize.value))
    
    const fetchCiyu = async () => {
      loading.value = true
      try {
        const params = { page: currentPage.value, size: pageSize.value }
        if (searchQuery.value) params.search = searchQuery.value
        
        const response = await request.get('/v1/ciyu', { params })
        ciyuList.value = response.data.items
        total.value = response.data.total
      } catch (error) {
        console.error('获取词语列表失败:', error)
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
        fetchCiyu()
      }, 500)
    }
    
    // 监听搜索框变化
    watch(searchQuery, () => {
      handleSearch()
    })
    
    const goToPage = (page) => {
      currentPage.value = page
      fetchCiyu()
    }

    const resetForm = () => {
      formData.value = { 
        word: '', pinyin: '', zhuyin: '', part_of_speech: '', 
        is_common: null, definition: '' 
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
        word: item.word,
        pinyin: item.pinyin,
        zhuyin: item.zhuyin || '',
        part_of_speech: item.part_of_speech || '',
        is_common: item.is_common,
        definition: item.definition
      }
      editingId.value = item.id
      showEditModal.value = true
    }

    const handleCreate = async () => {
      submitting.value = true
      try {
        await request.post('/v1/ciyu', formData.value)
        alert('创建成功')
        closeModal()
        fetchCiyu()
      } catch (error) {
        alert(error.response?.data?.detail || '创建失败')
      } finally {
        submitting.value = false
      }
    }

    const handleUpdate = async () => {
      submitting.value = true
      try {
        const { word, ...updateData } = formData.value
        await request.put(`/v1/ciyu/${editingId.value}`, updateData)
        alert('更新成功')
        closeModal()
        fetchCiyu()
      } catch (error) {
        alert(error.response?.data?.detail || '更新失败')
      } finally {
        submitting.value = false
      }
    }

    const handleDelete = async (item) => {
      if (!confirm(`确定要删除"${item.word}"吗？`)) return
      try {
        await request.delete(`/v1/ciyu/${item.id}`)
        alert('删除成功')
        fetchCiyu()
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
      fetchCiyu()
    })
    
    return {
      authStore, ciyuList, loading, searchQuery, currentPage, totalPages,
      showCreateModal, showEditModal, submitting, formData,
      handleSearch, goToPage, openEditModal, closeModal,
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
  max-width: 250px;
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
.modal h3 { margin-bottom: 20px; }
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.common-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  background: #f5f5f5;
  color: #666;
}

.common-badge.common {
  background: #e8f5e9;
  color: #2e7d32;
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
</style>
