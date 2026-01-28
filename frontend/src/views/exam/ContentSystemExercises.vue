<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <div class="header-left">
          <h2>📚 Content System - 题目管理</h2>
          <p class="subtitle">基础课程体系题目库</p>
        </div>
      </div>

      <!-- 筛选区域 -->
      <ExerciseFilterBar
        variant="green"
        v-model:filters="filters"
        v-model:searchQuery="searchQuery"
        :skillCategories="skillCategories"
        :exerciseTypes="filteredExerciseTypes"
        :showSkillCategory="true"
        :showQualityStatus="true"
        @search="handleSearch"
      />

      <!-- 统计信息 -->
      <div class="stats-section">
        <div class="stat-card">
          <div class="stat-number">{{ total }}</div>
          <div class="stat-label">题目总数</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ filteredExercises.length }}</div>
          <div class="stat-label">当前页数量</div>
        </div>
      </div>

      <div class="exercises-section">
        <h3>📝 题目详情</h3>
        
        <!-- 骨架屏加载状态 -->
        <div v-if="loading" class="cards-grid">
          <SkeletonCard v-for="i in 6" :key="'skeleton-' + i" variant="green" />
        </div>
        
        <div v-else-if="filteredExercises.length > 0" class="cards-grid">
          <ExerciseCard
            v-for="exercise in filteredExercises"
            :key="exercise.id"
            variant="green"
          >
            <template #left>
              <span class="type-badge">{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
            </template>
            <template #right>
              <span class="difficulty-badge" :class="getDifficultyClass(exercise.difficulty_level)">
                {{ getDifficultyText(exercise.difficulty_level) }}
              </span>
              <span class="status-badge" :class="getQualityClass(exercise.quality_status)">
                {{ getQualityText(exercise.quality_status) }}
              </span>
            </template>

            <div class="exercise-prompt">
              {{ getExercisePrompt(exercise) }}
            </div>

            <div class="word-info">
              <div class="info-label">
                🔤 关联单词：{{ getWordDisplay(exercise) }}
              </div>
              <div v-if="getWordPinyin(exercise)" class="word-sub">拼音：{{ getWordPinyin(exercise) }}</div>
              <div v-if="getWordTranslation(exercise)" class="word-sub">释义：{{ getWordTranslation(exercise) }}</div>
              <div v-if="getWordHskLevel(exercise)" class="word-sub">HSK：{{ getWordHskLevel(exercise) }}</div>
            </div>

            <div class="exercise-info">
              <div class="info-row">
                <span class="info-icon">📂</span>
                <span class="info-text">技能分类：{{ getSkillCategoryName(exercise) }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">🏷️</span>
                <span class="info-text">题型：{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
              </div>
              <div class="info-row" v-if="exercise.parent_exercise_id">
                <span class="info-icon">🔗</span>
                <span class="info-text">包含子题</span>
              </div>
              <div class="info-row">
                <span class="info-icon">🕐</span>
                <span class="info-text">{{ formatDate(exercise.created_at) }}</span>
              </div>
            </div>

            <details class="id-details">
              <summary class="id-summary">🔧 开发者信息</summary>
              <div class="id-content">
                <div class="id-item"><span>题目ID:</span><code>{{ exercise.id }}</code></div>
                <div class="id-item" v-if="exercise.parent_exercise_id"><span>父题ID:</span><code>{{ exercise.parent_exercise_id }}</code></div>
                <div class="id-item"><span>题型ID:</span><code>{{ exercise.exercise_type_id }}</code></div>
                <div class="id-item" v-if="exercise.word_id"><span>单词ID:</span><code>{{ exercise.word_id }}</code></div>
              </div>
            </details>

            <details class="meta-details" open>
              <summary class="meta-summary">📋 metadata (JSON)
                <span class="meta-actions">
                  <template v-if="!editingMetadata[exercise.id]">
                    <button class="btn-small" @click.stop="startEditMetadata(exercise.id)">✏️ 编辑</button>
                    <button class="btn-small" @click.stop="copyMetadata(exercise.id)">📋 复制</button>
                  </template>
                  <template v-else>
                    <button class="btn-small primary" @click.stop="saveMetadata(exercise)">💾 保存</button>
                    <button class="btn-small" @click.stop="cancelEditMetadata(exercise)">❌ 取消</button>
                  </template>
                </span>
              </summary>
              <textarea
                v-if="editingMetadata[exercise.id]"
                class="json-editor"
                :placeholder="'{}'"
                v-model="metadataDrafts[exercise.id]"
              ></textarea>
              <pre v-else class="json-preview">{{ metadataDrafts[exercise.id] || '{}' }}</pre>
              <div v-if="metadataErrors[exercise.id]" class="error-text">
                {{ metadataErrors[exercise.id] }}
              </div>
            </details>

            <div v-if="getExerciseMedia(exercise.id).length > 0" class="media-section">
              <div class="info-label">🎬 关联媒体：</div>
              <div class="media-list">
                <div v-for="media in getExerciseMedia(exercise.id)" :key="media.id" class="media-item-wrapper">
                  <div class="media-item">
                    <span class="media-icon">{{ media.file_type === 'audio' ? '🔊' : (media.file_type === 'video' ? '🎬' : '🖼️') }}</span>
                    <span class="media-name">{{ getMediaName(media) }}</span>
                    <span class="media-role">{{ getMediaRoleName(media.usage_role) }}</span>
                    <span class="media-type">{{ media.mime_type }}</span>
                  </div>
                  <div v-if="media.file_url" class="media-preview-container">
                    <img v-if="media.file_type === 'image'" :src="media.file_url" class="media-preview-img" @error="handleMediaError($event, 'image')" />
                    <audio v-else-if="media.file_type === 'audio'" :src="media.file_url" controls class="media-preview-audio" @error="handleMediaError($event, 'audio')" />
                    <video v-else-if="media.file_type === 'video'" :src="media.file_url" controls class="media-preview-video" @error="handleMediaError($event, 'video')" />
                  </div>
                  <div v-else class="media-no-url">⚠️ 无媒体地址</div>
                </div>
              </div>
            </div>
          </ExerciseCard>
        </div>
      </div>

      <div v-if="!loading" class="exercises-section">
        <div v-if="filteredExercises.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>暂无题目数据</h3>
          <p>{{ searchQuery ? '没有找到匹配的题目' : '暂无题目' }}</p>
        </div>
      </div>

      <div class="pagination" v-if="totalPages > 1 && !loading">
        <button class="btn" @click="goToPage(1)" :disabled="currentPage <= 1">首页</button>
        <button class="btn" @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1">上一页</button>
        <div class="page-info">第 {{ currentPage }} / {{ totalPages }} 页</div>
        <button class="btn" @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages">下一页</button>
        <button class="btn" @click="goToPage(totalPages)" :disabled="currentPage >= totalPages">末页</button>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import Header from '../../components/Header.vue'
import ExerciseCard from '../../components/ExerciseCard.vue'
import ExerciseFilterBar from '../../components/ExerciseFilterBar.vue'
import SkeletonCard from '../../components/SkeletonCard.vue'
import request from '../../utils/request'

export default {
  name: 'ContentSystemExercises',
  components: {
    Header,
    ExerciseCard,
    ExerciseFilterBar,
    SkeletonCard
  },
  setup() {
    const searchQuery = ref('')
    const loading = ref(true)
    const filtersLoading = ref(true)
    
    // 筛选条件
    const filters = ref({
      skillCategory: '',
      exerciseType: '',
      difficulty: '',
      qualityStatus: ''
    })
    
    // 数据
    const exercises = ref([])
    const currentPage = ref(1)
    const pageSize = ref(6)
    const total = ref(0)
    const metadataDrafts = ref({})
    const metadataOriginals = ref({})
    const metadataErrors = ref({})
    const editingMetadata = ref({})

    // 获取题目数据
    const fetchExercises = async () => {
      loading.value = true
      try {
        const params = {
          source: 'content_system',
          page: currentPage.value,
          size: pageSize.value
        }
        if (filters.value.exerciseType) {
          params.type_id = filters.value.exerciseType
        }
        if (filters.value.difficulty) {
          params.difficulty = filters.value.difficulty
        }
        if (searchQuery.value) {
          params.search = searchQuery.value
        }
        const res = await request.get('/v1/questions', {
          params
        })
        if (res.data) {
          exercises.value = res.data.items || []
          total.value = res.data.total || 0
          initMetadataDrafts()
        }
      } catch (error) {
        console.error('获取题目失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 使用专用筛选接口
    const allExerciseTypes = ref([])
    const allSkillCategories = ref([])
    
    const fetchFilterOptions = async () => {
      filtersLoading.value = true
      try {
        const res = await request.get('/v1/questions/filters', { 
          params: { source: 'content_system' } 
        })
        if (res.data) {
          allExerciseTypes.value = res.data.exercise_types || []
          allSkillCategories.value = res.data.skill_categories || []
        }
      } catch (error) {
        console.error('获取筛选选项失败:', error)
      } finally {
        filtersLoading.value = false
      }
    }

    onMounted(async () => {
      // 并行加载筛选选项和数据
      await Promise.all([fetchFilterOptions(), fetchExercises()])
    })

    // 筛选条件变化时自动搜索（不包括搜索关键词）
    watch(
      [() => filters.value.exerciseType, () => filters.value.difficulty],
      () => {
        currentPage.value = 1
        fetchExercises()
      }
    )
    
    // 搜索按钮点击处理
    const handleSearch = () => {
      currentPage.value = 1
      fetchExercises()
    }
    
    // 使用预加载的筛选选项
    const exerciseTypes = computed(() => allExerciseTypes.value)
    const skillCategories = computed(() => allSkillCategories.value)

    const filteredExerciseTypes = computed(() => {
      if (!filters.value.skillCategory) return exerciseTypes.value
      return exerciseTypes.value.filter(type => type.skill_category_id === filters.value.skillCategory)
    })
    
    // 筛选后的题目列表
    const filteredExercises = computed(() => {
      let result = exercises.value
      
      // 技能分类筛选
      if (filters.value.skillCategory) {
        result = result.filter(ex => ex.exercise_type?.skill_category_id === filters.value.skillCategory)
      }
      
      // 题型筛选
      if (filters.value.exerciseType) {
        result = result.filter(ex => ex.exercise_type_id === filters.value.exerciseType)
      }
      
      // 难度筛选
      if (filters.value.difficulty) {
        result = result.filter(ex => ex.difficulty_level === parseInt(filters.value.difficulty))
      }
      
      // 质检状态筛选
      if (filters.value.qualityStatus !== '') {
        result = result.filter(ex => ex.quality_status === parseInt(filters.value.qualityStatus))
      }
      
      return result
    })
    
    const totalPages = computed(() => {
      return Math.max(1, Math.ceil(total.value / pageSize.value))
    })
    
    const goToPage = (page) => {
      if (page < 1 || page > totalPages.value) return
      currentPage.value = page
      fetchExercises()
    }
    
    const getExerciseTypeName = (typeId) => {
      const type = exerciseTypes.value.find(ex => ex.id === typeId)
      if (type) {
        return type.display_name || type.name || '无题型信息'
      }
      return '无题型信息'
    }

    const getSkillCategoryName = (exercise) => {
      const category = exercise?.exercise_type?.skill_category
      if (category) {
        return category.description || category.name || '无技能分类信息'
      }
      return '无技能分类信息'
    }

    const getExercisePrompt = (exercise) => {
      if (!exercise) return '无题干信息'
      return exercise.prompt || '无题干信息'
    }

    const getWordDisplay = (exercise) => {
      const word = exercise?.word
      if (word) {
        return word.characters || word.word || word.text || word.name || '无关联单词信息'
      }
      return exercise?.word_text || exercise?.word_name || '无关联单词信息'
    }

    const getWordPinyin = (exercise) => {
      const word = exercise?.word
      return word?.pinyin || ''
    }

    const getWordTranslation = (exercise) => {
      const word = exercise?.word
      return word?.translation || ''
    }

    const getWordHskLevel = (exercise) => {
      const word = exercise?.word
      return word?.hsk_level || ''
    }
    
    const getDifficultyText = (level) => {
      if (level === undefined || level === null || level === '') return '无难度信息'
      const map = { 1: '简单', 2: '中等', 3: '困难' }
      return map[level] || level
    }
    
    const getDifficultyClass = (level) => {
      const map = { 1: 'easy', 2: 'medium', 3: 'hard' }
      return map[level] || ''
    }
    
    const getQualityText = (status) => {
      if (status === undefined || status === null || status === '') return '无质检信息'
      const map = { 1: '已通过', 0: '待审核', '-1': '已驳回' }
      return map[status] ?? '无质检信息'
    }
    
    const getQualityClass = (status) => {
      const map = { 1: 'approved', 0: 'pending', '-1': 'rejected' }
      return map[status] || ''
    }
    
    const getExerciseMedia = (exerciseId) => {
      const exercise = exercises.value.find(e => e.id === exerciseId);
      if (exercise && exercise.media_assets) {
        return exercise.media_assets.map(item => ({
          ...item.media_asset,
          usage_role: item.usage_role
        }));
      }
      return []
    }
    
    const getMediaRoleName = (role) => {
      const roleMap = {
        'prompt_audio': '题干音频',
        'option_image': '选项图片',
        'explanation_video': '解析视频',
        'background_audio': '背景音频'
      }
      return roleMap[role] || role
    }

    const getMediaName = (media) => {
      if (!media) return '无媒体名称信息'
      return media.title || media.file_name || media.original_name || media.name || '无媒体名称信息'
    }
    
    const normalizeMetadata = (metadata) => {
      if (!metadata) return {}
      if (typeof metadata === 'string') {
        try {
          return JSON.parse(metadata)
        } catch (error) {
          return {}
        }
      }
      return metadata
    }

    const formatJson = (metadata) => {
      const value = normalizeMetadata(metadata)
      return JSON.stringify(value ?? {}, null, 2)
    }

    const initMetadataDrafts = () => {
      exercises.value.forEach(ex => {
        const id = ex.id
        const content = formatJson(ex.metadata)
        metadataOriginals.value[id] = content
        if (!metadataDrafts.value[id]) {
          metadataDrafts.value[id] = content
        }
      })
    }

    const parseMetadataDraft = (id) => {
      const raw = metadataDrafts.value[id]
      if (!raw || raw.trim() === '') return null
      try {
        return JSON.parse(raw)
      } catch (error) {
        metadataErrors.value[id] = 'JSON 格式错误，请检查括号/逗号。'
        return undefined
      }
    }

    const formatMetadata = (id) => {
      const parsed = parseMetadataDraft(id)
      if (parsed === undefined) return
      metadataDrafts.value[id] = JSON.stringify(parsed ?? {}, null, 2)
      metadataErrors.value[id] = ''
    }

    const saveMetadata = async (exercise) => {
      const parsed = parseMetadataDraft(exercise.id)
      if (parsed === undefined) return
      try {
        const res = await request.patch(`/v1/questions/${exercise.id}/metadata`,
          { metadata: parsed },
          { params: { source: 'content_system' } }
        )
        if (res.data) {
          exercise.metadata = res.data.metadata ?? parsed
          const content = formatJson(exercise.metadata)
          metadataOriginals.value[exercise.id] = content
          metadataDrafts.value[exercise.id] = content
          metadataErrors.value[exercise.id] = ''
          editingMetadata.value[exercise.id] = false
        }
      } catch (error) {
        console.error('保存 metadata 失败:', error)
        metadataErrors.value[exercise.id] = error.response?.data?.detail || '保存失败'
      }
    }

    const startEditMetadata = (id) => {
      editingMetadata.value[id] = true
      // 进入编辑时格式化JSON
      formatMetadata(id)
    }

    const cancelEditMetadata = (exercise) => {
      resetMetadata(exercise)
      editingMetadata.value[exercise.id] = false
    }

    const handleMediaError = (event, type) => {
      console.warn(`媒体加载失败 (${type}):`, event.target.src)
      event.target.style.display = 'none'
      // 可以在这里添加错误提示
    }

    const resetMetadata = (exercise) => {
      const content = metadataOriginals.value[exercise.id] ?? formatJson(exercise.metadata)
      metadataDrafts.value[exercise.id] = content
      metadataErrors.value[exercise.id] = ''
    }

    const clearMetadata = (id) => {
      metadataDrafts.value[id] = ''
      metadataErrors.value[id] = ''
    }

    const copyMetadata = async (id) => {
      const text = metadataDrafts.value[id] ?? ''
      try {
        await navigator.clipboard.writeText(text)
      } catch (error) {
        console.error('复制失败:', error)
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }

    return {
      searchQuery,
      filters,
      loading,
      filtersLoading,
      skillCategories,
      exerciseTypes,
      filteredExerciseTypes,
      filteredExercises,
      currentPage,
      totalPages,
      total,
      metadataDrafts,
      metadataOriginals,
      metadataErrors,
      editingMetadata,
      goToPage,
      getExerciseTypeName,
      getSkillCategoryName,
      getExercisePrompt,
      getWordDisplay,
      getWordPinyin,
      getWordTranslation,
      getWordHskLevel,
      getDifficultyText,
      getDifficultyClass,
      getQualityText,
      getQualityClass,
      getExerciseMedia,
      getMediaRoleName,
      getMediaName,
      formatDate,
      formatMetadata,
      saveMetadata,
      startEditMetadata,
      cancelEditMetadata,
      handleMediaError,
      copyMetadata,
      handleSearch
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
}

.header-left h2 {
  margin: 0 0 5px 0;
  color: #1b5e20;
  font-size: 1.8rem;
}

.subtitle {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.exercises-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.exercises-section h3 {
  margin: 0 0 20px 0;
  color: #1b5e20;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 20px;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}

.btn {
  padding: 6px 14px;
  border: 1px solid #66bb6a;
  background: white;
  color: #2e7d32;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-weight: 500;
}

/* 表格样式 */
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f5f5f5;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #e0e0e0;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  color: #333;
}

.data-table tr:hover {
  background: #f9f9f9;
}

code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #d32f2f;
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
}

.status-badge.approved {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-badge.pending {
  background: #fff3e0;
  color: #ef6c00;
}

.status-badge.rejected {
  background: #ffebee;
  color: #c62828;
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

.btn-small {
  padding: 4px 12px;
  border: 1px solid #2196f3;
  background: white;
  color: #2196f3;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-small:hover {
  background: #2196f3;
  color: white;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

/* 详情弹窗样式 */
.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.detail-modal-content {
  background: white;
  width: 800px;
  max-width: 90%;
  max-height: 90vh;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.detail-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-header h3 {
  margin: 0;
  color: #1b5e20;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.detail-body {
  padding: 20px;
  overflow-y: auto;
  background: #f0f2f5; /* 让卡片在弹窗中更明显 */
}

/* 卡片样式 - 基础样式由 ExerciseCard 组件提供 */

.exercise-id {
  margin-bottom: 12px;
}

.exercise-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 20px;
  margin-bottom: 15px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.95rem;
  color: #333;
}

.meta-label {
  color: #2e7d32;
  font-weight: 600;
}

.meta-value {
  color: #333;
}

/* 已移至 ExerciseCard 组件的样式已删除 */

.metadata-content {
  margin-top: 8px;
}

.meta-block {
  margin-bottom: 12px;
}

.meta-title {
  font-weight: 600;
  color: #2e7d32;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.meta-text {
  background: white;
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  line-height: 1.6;
}

.pinyin-text {
  display: block;
  margin-top: 6px;
  color: #666;
  font-size: 0.9rem;
}

.option-pinyin {
  color: #666;
  font-size: 0.85rem;
}

.meta-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-item-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 10px 12px;
}

.meta-subtitle {
  font-weight: 600;
  color: #1b5e20;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
}

.option-key {
  font-weight: bold;
  color: #1b5e20;
  min-width: 25px;
}

.option-text {
  flex: 1;
}

.correct-mark {
  color: #4caf50;
  font-weight: bold;
  font-size: 1.2rem;
}

.audio-text {
  padding: 10px;
  background: white;
  border-radius: 6px;
  border-left: 4px solid #2196f3;
}

.answer-badge {
  display: inline-block;
  margin-left: 10px;
  padding: 4px 10px;
  background: #4caf50;
  color: white;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.passage-content {
  padding: 10px;
  background: white;
  border-radius: 6px;
}

.passage-text {
  padding: 10px;
  background: #fff9e6;
  border-radius: 6px;
  line-height: 1.8;
  margin-bottom: 12px;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.question-item {
  padding: 10px;
  background: #f0f0f0;
  border-radius: 6px;
}

.question-text {
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.question-options {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.q-option {
  padding: 4px 10px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 0.9rem;
}

.q-option.correct {
  background: #4caf50;
  color: white;
  border-color: #4caf50;
  font-weight: 600;
}

.blanks-list {
  padding: 10px;
  background: white;
  border-radius: 6px;
}

.blank-item {
  padding: 8px;
  background: #e3f2fd;
  border-radius: 6px;
  border-left: 4px solid #2196f3;
}

.hint-text {
  color: #666;
  font-size: 0.9rem;
  margin-left: 8px;
}

.sentence-content {
  padding: 10px;
  background: white;
  border-radius: 6px;
}

.sentence-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1b5e20;
  padding: 12px;
  background: #f1f8e9;
  border-radius: 6px;
  margin-bottom: 10px;
  text-align: center;
}

.tips-text {
  padding: 8px 12px;
  background: #fff3e0;
  border-radius: 6px;
  color: #e65100;
  font-size: 0.9rem;
}

.media-section {
  background: #e3f2fd;
  padding: 12px;
  border-radius: 8px;
}

.media-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 8px;
}

.media-item-wrapper {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.media-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  font-size: 0.9rem;
  border-bottom: 1px solid #f0f0f0;
}

.media-preview-container {
  padding: 10px;
  background: #fafafa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.media-preview-img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 6px;
  object-fit: contain;
}

.media-preview-audio {
  width: 100%;
  max-width: 300px;
}

.media-preview-video {
  width: 100%;
  max-width: 400px;
  border-radius: 6px;
}

.media-no-url {
  padding: 10px;
  color: #999;
  font-size: 0.85rem;
  text-align: center;
  background: #fafafa;
}

.media-icon {
  font-size: 1.2rem;
}

.media-name {
  font-weight: 500;
  color: #333;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.media-role {
  font-weight: 600;
  color: #1565c0;
  font-size: 0.85rem;
}

.media-type {
  color: #666;
  font-size: 0.8rem;
  margin-left: auto;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f9f9f9;
  border-top: 1px solid #e0e0e0;
}

.creator-info {
  display: flex;
  gap: 10px;
  align-items: center;
}

.create-time {
  color: #666;
  font-size: 0.85rem;
}

.creator-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #e2e3e5;
  color: #383d41;
}

.json-view {
  background: #282c34;
  color: #abb2bf;
  padding: 15px;
  border-radius: 8px;
  overflow-x: auto;
}

.detail-footer {
  padding: 20px;
  border-top: 1px solid #eee;
  text-align: right;
}

.btn-primary {
  padding: 8px 24px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover {
  background: #43a047;
}
</style>
