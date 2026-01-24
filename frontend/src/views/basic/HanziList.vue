<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <h2>汉字管理</h2>
        <div class="header-actions">
          <div class="permission-info">
            <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
          </div>
          <button class="btn btn-add" @click="showCreateModal = true">+ 添加汉字</button>
        </div>
      </div>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          placeholder="搜索汉字..."
          @keyup.enter="handleSearch"
        >
        <button class="btn btn-primary" @click="handleSearch" :disabled="loading">搜索</button>
      </div>
      
      <table class="table" v-if="!loading && hanziList.length > 0">
        <thead>
          <tr>
            <th>汉字</th>
            <th>Unicode</th>
            <th>URL</th>
            <th>创建者</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in hanziList" :key="item.id">
            <td class="char-cell">{{ item.character }}</td>
            <td>{{ item.unicode_decimal || '-' }}</td>
            <td class="text-ellipsis">
              <a v-if="item.url" :href="item.url" target="_blank" class="link">{{ item.url }}</a>
              <span v-else>-</span>
            </td>
            <td>
              <span class="status-pill owner-pill" :class="getOwnerClass(item)">
                {{ getOwnerText(item.created_by) }}
              </span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action btn-view" @click="openDetailModal(item)">查看</button>
                <button v-if="canModify(item)" class="btn-action btn-edit" @click="openEditModal(item)">编辑</button>
                <button v-if="canModify(item)" class="btn-action btn-delete" @click="handleDelete(item)">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="loading" class="loading-text">加载中...</div>
      <div v-if="!loading && hanziList.length === 0" class="empty-text">暂无数据</div>
      
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
        <h3>{{ showEditModal ? '编辑汉字' : '添加汉字' }}</h3>
        <form @submit.prevent="showEditModal ? handleUpdate() : handleCreate()">
          <div class="form-grid">
            <div class="form-column">
              <div class="form-group">
                <label class="form-label">汉字 *</label>
                <input v-model="formData.character" type="text" class="form-input" required :disabled="showEditModal" maxlength="1">
              </div>
              <div class="form-group">
                <label class="form-label">Unicode (十进制)</label>
                <input v-model.number="formData.unicode_decimal" type="number" class="form-input">
              </div>
              <div class="form-group">
                <label class="form-label">URL 链接</label>
                <input v-model="formData.url" type="text" class="form-input" placeholder="http://...">
              </div>
            </div>
            
            <div class="form-column">
              <div class="form-group">
                <label class="form-label">基本信息 (JSON)</label>
                <textarea 
                  v-model="jsonInputs.basic_info" 
                  class="form-input code-input" 
                  rows="5"
                  placeholder='{"pinyin": "..."}'
                ></textarea>
                <small class="form-hint">请输入有效的 JSON 格式</small>
              </div>
              <div class="form-group">
                <label class="form-label">意思信息 (JSON)</label>
                <textarea 
                  v-model="jsonInputs.yisi_info" 
                  class="form-input code-input" 
                  rows="5"
                  placeholder='{"meanings": [...] }'
                ></textarea>
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

    <!-- 详情查看弹窗 -->
    <div v-if="showDetailModal" class="results-modal" @click.self="closeDetailModal">
      <div class="results-modal-content">
        <div class="results-modal-header">
          <h3>汉字详情</h3>
          <button class="close-btn" @click="closeDetailModal">×</button>
        </div>
        <div class="results-modal-body">
          <div class="result-card">
            <div class="result-header">
              <span class="result-word hanzi-char">{{ detailItem?.character }}</span>
              <span class="result-type type-hanzi">汉字</span>
              <span v-if="canModify(detailItem)" class="result-mine">我的</span>
              <span v-else-if="detailItem?.created_by === 'admin'" class="result-admin">管理员</span>
              <span v-else-if="!detailItem?.created_by || detailItem?.created_by === 'system'" class="result-system">系统</span>
            </div>
            
            <div class="result-phonetic" v-if="detailItem?.unicode_decimal">
              <span class="unicode">Unicode: {{ detailItem.unicode_decimal }}</span>
            </div>
            
            <div class="result-details">
              <div v-if="detailItem?.url" class="detail-item">
                <span class="label">链接：</span>
                <a :href="detailItem.url" target="_blank" class="link">{{ detailItem.url }}</a>
              </div>
            </div>

            <!-- JSON 数据展示 -->
            <div class="json-sections">
              <div v-if="detailItem?.basic_info" class="json-section">
                <h4>基本信息</h4>
                <pre>{{ JSON.stringify(detailItem.basic_info, null, 2) }}</pre>
              </div>
              <div v-if="detailItem?.yisi_info" class="json-section">
                <h4>意思信息</h4>
                <pre>{{ JSON.stringify(detailItem.yisi_info, null, 2) }}</pre>
              </div>
              <div v-if="detailItem?.evolution_data" class="json-section">
                <h4>演变数据</h4>
                <pre>{{ JSON.stringify(detailItem.evolution_data, null, 2) }}</pre>
              </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="result-actions" v-if="canModify(detailItem)">
              <button class="btn-small btn-header" @click="closeDetailModal(); openEditModal(detailItem)">编辑</button>
              <button class="btn-small btn-header btn-danger-header" @click="handleDelete(detailItem); closeDetailModal()">删除</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import Header from '../../components/Header.vue'
import request from '../../utils/request'
import { useAuthStore } from '../../stores/auth'

export default {
  name: 'HanziList',
  components: { Header },
  setup() {
    const authStore = useAuthStore()
    const hanziList = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(20)
    const total = ref(0)
    const jumpPage = ref(1)
    
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const showDetailModal = ref(false)
    const submitting = ref(false)
    const editingId = ref(null)
    const detailItem = ref(null)
    
    const formData = ref({
      character: '',
      unicode_decimal: null,
      url: ''
    })
    
    // 用于处理 JSON 字段的文本输入
    const jsonInputs = ref({
      basic_info: '',
      yisi_info: ''
    })
    
    const totalPages = computed(() => Math.ceil(total.value / pageSize.value))
    
    const fetchHanzi = async () => {
      loading.value = true
      try {
        const params = { page: currentPage.value, size: pageSize.value }
        if (searchQuery.value) params.search = searchQuery.value
        
        const response = await request.get('/v1/hanzi', { params })
        hanziList.value = response.data.items
        total.value = response.data.total
      } catch (error) {
        console.error('获取汉字列表失败:', error)
        alert('获取数据失败')
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      currentPage.value = 1
      fetchHanzi()
    }
    
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        jumpPage.value = page
        fetchHanzi()
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
        character: '', unicode_decimal: null, url: ''
      }
      jsonInputs.value = { basic_info: '', yisi_info: '' }
      editingId.value = null
    }

    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      resetForm()
    }

    const openEditModal = (item) => {
      formData.value = {
        character: item.character,
        unicode_decimal: item.unicode_decimal,
        url: item.url || ''
      }
      // 填充 JSON 字符串
      jsonInputs.value = {
        basic_info: item.basic_info ? JSON.stringify(item.basic_info, null, 2) : '',
        yisi_info: item.yisi_info ? JSON.stringify(item.yisi_info, null, 2) : ''
      }
      editingId.value = item.id
      showEditModal.value = true
    }

    const openDetailModal = (item) => {
      detailItem.value = item
      showDetailModal.value = true
    }

    const closeDetailModal = () => {
      showDetailModal.value = false
      detailItem.value = null
    }

    // 辅助函数：解析 JSON 输入
    const parseJsonInput = (input) => {
      if (!input || input.trim() === '') return null
      try {
        return JSON.parse(input)
      } catch (e) {
        throw new Error('JSON 格式错误')
      }
    }

    const handleCreate = async () => {
      submitting.value = true
      try {
        const payload = { ...formData.value }
        // 处理 JSON 字段
        if (jsonInputs.value.basic_info) {
          payload.basic_info = parseJsonInput(jsonInputs.value.basic_info)
        }
        if (jsonInputs.value.yisi_info) {
          payload.yisi_info = parseJsonInput(jsonInputs.value.yisi_info)
        }

        await request.post('/v1/hanzi', payload)
        alert('创建成功')
        closeModal()
        fetchHanzi()
      } catch (error) {
        const msg = error.message === 'JSON 格式错误' ? 'JSON 格式错误，请检查输入' : (error.response?.data?.detail || '创建失败')
        alert(msg)
      } finally {
        submitting.value = false
      }
    }

    const handleUpdate = async () => {
      submitting.value = true
      try {
        const { character, ...updateData } = formData.value
        const payload = { ...updateData }
        
        // 处理 JSON 字段
        if (jsonInputs.value.basic_info) {
          payload.basic_info = parseJsonInput(jsonInputs.value.basic_info)
        } else {
          // 如果清空了，是否需要发送 null？视后端 API 而定，这里假设如果不填就不更新或者更新为 null
          // 为了简单，这里如果为空字符串则视为 null
          payload.basic_info = null
        }
        
        if (jsonInputs.value.yisi_info) {
          payload.yisi_info = parseJsonInput(jsonInputs.value.yisi_info)
        } else {
          payload.yisi_info = null
        }

        await request.put(`/v1/hanzi/${editingId.value}`, payload)
        alert('更新成功')
        closeModal()
        fetchHanzi()
      } catch (error) {
        const msg = error.message === 'JSON 格式错误' ? 'JSON 格式错误，请检查输入' : (error.response?.data?.detail || '更新失败')
        alert(msg)
      } finally {
        submitting.value = false
      }
    }

    const handleDelete = async (item) => {
      if (!confirm(`确定要删除"${item.character}"吗？`)) return
      try {
        await request.delete(`/v1/hanzi/${item.id}`)
        alert('删除成功')
        fetchHanzi()
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
        'owner-pill--me': canModify(item),
        'owner-pill--admin': item.created_by === 'admin',
        'owner-pill--system': !item.created_by || item.created_by === 'system'
      }
    }

    const canModify = (item) => {
      // 管理员可以修改所有资源
      if (authStore.user?.role === 'admin') {
        return true
      }
      // 老师只能修改自己创建的资源（不能修改系统资源和管理员资源）
      if (authStore.user?.role === 'teacher') {
        return item.created_by === authStore.user.username
      }
      return false
    }
    
    onMounted(() => {
      fetchHanzi()
    })
    
    return {
      authStore, hanziList, loading, searchQuery, currentPage, totalPages, jumpPage,
      showCreateModal, showEditModal, showDetailModal, submitting, formData, jsonInputs, detailItem,
      handleSearch, goToPage, handleJumpPage, openEditModal, openDetailModal, closeModal, closeDetailModal,
      handleCreate, handleUpdate, handleDelete, getOwnerText, getOwnerClass, canModify
    }
  }
}
</script>

<style scoped>
/* 复用 ChengyuList 的样式 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
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

.loading-text, .empty-text { text-align: center; padding: 40px; color: #666; }

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
  border-radius: 16px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
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
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-weight: 500;
  font-size: 14px;
  color: #333;
}

.form-input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.code-input {
  font-family: monospace;
  font-size: 12px;
}

.form-hint {
  font-size: 12px;
  color: #999;
}

/* 分页样式 */
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
  color: #777;
}

/* 按钮样式 */
.btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  background: #f0f0f0;
  color: #333;
}

.btn-primary {
  background: #66bb6a;
  color: white;
}
.btn-primary:hover {
  background: #5ca660;
}

.btn-add {
  background: #66bb6a;
  color: white;
  padding: 8px 20px;
}
.btn-add:hover {
  background: #5ca660;
}

/* 操作按钮样式 */
.btn-action {
  padding: 4px 12px;
  font-size: 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  border: 1px solid;
}

.btn-view {
  background: white;
  color: #66bb6a;
  border-color: #66bb6a;
}
.btn-view:hover {
  background: #66bb6a;
  color: white;
}

.btn-edit {
  background: white;
  color: #ff9800;
  border-color: #ff9800;
}
.btn-edit:hover {
  background: #ff9800;
  color: white;
}

.btn-delete {
  background: white;
  color: #f44336;
  border-color: #f44336;
}
.btn-delete:hover {
  background: #f44336;
  color: white;
}

/* 详情弹窗样式 */
.results-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.results-modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.results-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #999;
  cursor: pointer;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover {
  background: #f0f0f0;
}

.results-modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.result-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.hanzi-char {
  font-size: 32px;
  font-weight: bold;
  color: #333;
}

.type-hanzi {
  background: #e3f2fd;
  color: #2196f3;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.result-mine {
  padding: 2px 8px;
  background: #e8f5e9;
  color: #66bb6a;
  border-radius: 4px;
  font-size: 12px;
}
.result-admin {
  padding: 2px 8px;
  background: #e8f5e9;
  color: #66bb6a;
  border-radius: 4px;
  font-size: 12px;
}
.result-system {
  padding: 2px 8px;
  background: #e8f5e9;
  color: #888;
  border-radius: 4px;
  font-size: 12px;
}

.json-sections {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.json-section h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #555;
  border-left: 3px solid #66bb6a;
  padding-left: 8px;
}

.json-section pre {
  background: #282c34;
  color: #abb2bf;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
  font-family: monospace;
  font-size: 13px;
  margin: 0;
}

.link {
  color: #2196f3;
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}

/* 头部样式 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.search-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

/* 表格样式 */
.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.table th, .table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table th {
  background: #f5f5f5;
  font-weight: 600;
  color: #555;
}

.char-cell {
  font-size: 18px;
  font-weight: bold;
}

.owner-pill {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  display: inline-block;
}

.owner-pill--me {
  background: #e8f5e9;
  color: #2e7d32;
}

.owner-pill--admin {
  background: #fff3e0;
  color: #ef6c00;
}

.owner-pill--system {
  background: #f5f5f5;
  color: #616161;
}

.btn-header {
  background: white;
  color: #66bb6a;
  border: 1px solid #66bb6a;
}
.btn-danger-header {
  color: #dc3545;
  border-color: #dc3545;
}
.btn-small {
  padding: 4px 12px;
  font-size: 12px;
  border: 1px solid #66bb6a;
  background: white;
  color: #66bb6a;
  border-radius: 4px;
  cursor: pointer;
}
.result-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}
</style>