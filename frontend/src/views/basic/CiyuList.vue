<template>
  <div>
    <Header />
    <div class="container">
      <PageHeader
        icon="📖"
        title="词语管理"
        subtitle="词语基础知识库"
        variant="green"
        :showAddButton="true"
        addButtonText="添加词语"
        :showPermissionTip="true"
        @add="showCreateModal = true"
      />
      
      <SearchBar
        v-model="searchQuery"
        placeholder="搜索词语..."
        variant="green"
        :loading="loading"
        @search="handleSearch"
      />
      
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
              <span v-if="item.is_common !== null" class="status-pill common-badge" :class="item.is_common ? 'common' : 'rare'">
                {{ item.is_common ? '常用' : '非常用' }}
              </span>
              <span v-else>-</span>
            </td>
            <td class="text-ellipsis">{{ item.definition }}</td>
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
      <div v-if="!loading && ciyuList.length === 0" class="empty-text">暂无数据</div>
      
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
        <h3>{{ showEditModal ? '编辑词语' : '添加词语' }}</h3>
        <form @submit.prevent="showEditModal ? handleUpdate() : handleCreate()">
          <div class="form-grid">
            <div class="form-column">
              <div class="form-group">
                <label class="form-label">词语 *</label>
                <input v-model="formData.word" type="text" class="form-input" required :disabled="showEditModal">
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
            </div>
            
            <div class="form-column">
              <div class="form-group">
                <label class="form-label">是否常用词</label>
                <select v-model="formData.is_common" class="form-input">
                  <option :value="null">请选择</option>
                  <option :value="true">常用词</option>
                  <option :value="false">非常用词</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">定义</label>
                <textarea v-model="formData.definition" class="form-input" rows="4"></textarea>
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

    <!-- 详情查看弹窗 - 与首页搜索结果样式一致 -->
    <div v-if="showDetailModal" class="results-modal" @click.self="closeDetailModal">
      <div class="results-modal-content">
        <div class="results-modal-header">
          <h3>词语详情</h3>
          <button class="close-btn" @click="closeDetailModal">×</button>
        </div>
        <div class="results-modal-body">
          <div class="result-card">
            <div class="result-header">
              <span class="result-word">{{ detailItem?.word }}</span>
              <span class="result-type type-ciyu">词语</span>
              <span v-if="canModify(detailItem)" class="result-mine">我的</span>
              <span v-else-if="detailItem?.created_by === 'admin'" class="result-admin">管理员</span>
              <span v-else-if="!detailItem?.created_by || detailItem?.created_by === 'system'" class="result-system">系统</span>
            </div>
            
            <!-- 拼音和注音 -->
            <div class="result-phonetic">
              <span v-if="detailItem?.pinyin" class="pinyin">拼音：{{ detailItem.pinyin }}</span>
              <span v-if="detailItem?.zhuyin" class="zhuyin">注音：{{ detailItem.zhuyin }}</span>
            </div>
            
            <!-- 词语特有字段 -->
            <div class="result-details">
              <div v-if="detailItem?.part_of_speech" class="detail-item">
                <span class="label">词性：</span>{{ detailItem.part_of_speech }}
              </div>
              <div v-if="detailItem?.is_common !== null" class="detail-item">
                <span class="label">常用程度：</span>{{ detailItem.is_common ? '常用词' : '非常用词' }}
              </div>
            </div>
            
            <!-- 定义 -->
            <div v-if="detailItem?.definition" class="result-definition">
              <span class="label">定义：</span>{{ detailItem.definition }}
            </div>
            
            <!-- 同义词和反义词 -->
            <div v-if="detailItem?.synonyms && detailItem.synonyms.length > 0" class="result-relations">
              <span class="label">同义词：</span>
              <span class="relation-tags">
                <span v-for="s in detailItem.synonyms" :key="s" class="relation-tag synonym">{{ s }}</span>
              </span>
            </div>
            <div v-if="detailItem?.antonyms && detailItem.antonyms.length > 0" class="result-relations">
              <span class="label">反义词：</span>
              <span class="relation-tags">
                <span v-for="a in detailItem.antonyms" :key="a" class="relation-tag antonym">{{ a }}</span>
              </span>
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
import { ref, computed, onMounted } from 'vue'
import Header from '../../components/Header.vue'
import PageHeader from '../../components/PageHeader.vue'
import SearchBar from '../../components/SearchBar.vue'
import request from '../../utils/request'
import { useAuthStore } from '../../stores/auth'

export default {
  name: 'CiyuList',
  components: { Header, PageHeader, SearchBar },
  setup() {
    const authStore = useAuthStore()
    const ciyuList = ref([])
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
      currentPage.value = 1
      fetchCiyu()
    }
    
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        jumpPage.value = page
        fetchCiyu()
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

    const openDetailModal = (item) => {
      detailItem.value = item
      showDetailModal.value = true
    }

    const closeDetailModal = () => {
      showDetailModal.value = false
      detailItem.value = null
    }

    const handleCreate = async () => {
      submitting.value = true
      try {
        // 处理常用程度默认值：如果未选择，默认为非常用词
        const submitData = { ...formData.value }
        if (submitData.is_common === null) {
          submitData.is_common = false
        }
        
        await request.post('/v1/ciyu', submitData)
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
      fetchCiyu()
    })
    
    return {
      authStore, ciyuList, loading, searchQuery, currentPage, totalPages, jumpPage,
      showCreateModal, showEditModal, showDetailModal, submitting, formData, detailItem,
      handleSearch, goToPage, handleJumpPage, openEditModal, openDetailModal, closeModal, closeDetailModal,
      handleCreate, handleUpdate, handleDelete, getOwnerText, getOwnerClass, canModify
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-box {
  margin-bottom: 24px;
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #66bb6a;
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

/* 详情弹窗样式 - 与首页一致 */
.results-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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

.results-modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
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
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f0f0f0;
  color: #333;
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.result-word {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.result-type {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.type-ciyu {
  background: #e8f5e9;
  color: #2e7d32;
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

.result-phonetic {
  display: flex;
  gap: 20px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
}

.pinyin, .zhuyin {
  display: flex;
  align-items: center;
}

.result-details {
  margin-bottom: 12px;
}

.detail-item {
  margin-bottom: 6px;
  font-size: 14px;
  line-height: 1.5;
}

.label {
  font-weight: bold;
  color: #555;
  margin-right: 4px;
}

.result-definition {
  color: #444;
  line-height: 1.6;
  margin-bottom: 12px;
}

.result-relations {
  margin-bottom: 8px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.relation-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.relation-tag {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.relation-tag.synonym {
  background: #e8f5e9;
  color: #2e7d32;
}

.relation-tag.antonym {
  background: #ffebee;
  color: #c62828;
}

.result-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
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

.btn-small:hover {
  background: #66bb6a;
  color: white;
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

.btn-danger-header:hover {
  background: #dc3545;
  color: white;
}
</style>
