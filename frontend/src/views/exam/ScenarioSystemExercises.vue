<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <div class="header-left">
          <h2>🤖 Scenario Learning System - AI生成题目</h2>
          <p class="subtitle">基于AI动态生成的情境学习题目库</p>
        </div>
      </div>

      <!-- 筛选区域 -->
      <ExerciseFilterBar
        variant="purple"
        v-model:filters="filters"
        v-model:searchQuery="searchQuery"
        :skillCategories="slSkillCategories"
        :exerciseTypes="filteredExerciseTypes"
        :lessons="generatedLessons"
        :showSkillCategory="true"
        :showLesson="true"
        @search="handleSearch"
      />

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
          <SkeletonCard v-for="i in 6" :key="'skeleton-' + i" variant="purple" />
        </div>
        
        <div v-else-if="filteredExercises.length > 0" class="cards-grid">
          <ExerciseCard
            v-for="exercise in filteredExercises"
            :key="exercise.id"
            variant="purple"
          >
            <template #left>
              <span class="type-badge">{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
            </template>
            <template #right>
              <span class="difficulty-badge" :class="getDifficultyClass(exercise.difficulty_level)">
                {{ getDifficultyText(exercise.difficulty_level) }}
              </span>
            </template>

            <div class="exercise-prompt">
              {{ getExercisePrompt(exercise) }}
            </div>

            <div class="word-info">
              <div class="info-label">📘 来源课程：{{ getLessonName(exercise) }}</div>
              <div class="info-label">🔤 关联单词：{{ getVocabDisplay(exercise) }}</div>
            </div>

            <div class="exercise-info">
              <div class="info-row">
                <span class="info-icon">📘</span>
                <span class="info-text">来源课程：{{ getLessonName(exercise) }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">🏷️</span>
                <span class="info-text">题型：{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">📂</span>
                <span class="info-text">技能分类：{{ getSkillCategoryName(exercise) }}</span>
              </div>
              <div class="info-row">
                <span class="info-icon">📊</span>
                <span class="info-text">难度：{{ getDifficultyText(exercise.difficulty_level) }}</span>
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
                <div class="id-item"><span>课程ID:</span><code>{{ exercise.source_lesson_db_id }}</code></div>
                <div class="id-item" v-if="exercise.vocab_package_db_id"><span>词汇包ID:</span><code>{{ exercise.vocab_package_db_id }}</code></div>
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
              <div class="info-label">🎬 关联媒体</div>
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

        <div v-else-if="!loading" class="empty-state">
          <div class="empty-icon">🤖</div>
          <h3>暂无AI生成的题目</h3>
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
  name: 'ScenarioSystemExercises',
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
      lessonId: '',
      exerciseType: '',
      difficulty: ''
    })
    
    // 数据
    const slExercises = ref([])
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
          source: 'scenario_system',
          page: currentPage.value,
          size: pageSize.value
        }
        if (filters.value.exerciseType) {
          params.type_id = filters.value.exerciseType
        }
        if (filters.value.difficulty) {
          params.difficulty = filters.value.difficulty
        }
        if (filters.value.lessonId) {
          params.lesson_id = filters.value.lessonId
        }
        if (searchQuery.value) {
          params.search = searchQuery.value
        }
        const res = await request.get('/v1/questions', { params })
        if (res.data) {
          slExercises.value = res.data.items || []
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
    const allLessons = ref([])
    const allExerciseTypes = ref([])
    const allSkillCategories = ref([])
    
    const fetchFilterOptions = async () => {
      filtersLoading.value = true
      try {
        const res = await request.get('/v1/questions/filters', { 
          params: { source: 'scenario_system' } 
        })
        if (res.data) {
          allExerciseTypes.value = res.data.exercise_types || []
          allLessons.value = res.data.lessons || []
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
      [() => filters.value.exerciseType, () => filters.value.difficulty, () => filters.value.lessonId],
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

    // 直接使用后端返回的数据，不再前端筛选
    const filteredExercises = computed(() => {
      return slExercises.value
    })

    const totalPages = computed(() => {
      return Math.max(1, Math.ceil(total.value / pageSize.value))
    })

    const goToPage = (page) => {
      if (page < 1 || page > totalPages.value) return
      currentPage.value = page
      fetchExercises()
    }
    
    // 使用预加载的筛选选项
    const slExerciseTypes = computed(() => allExerciseTypes.value)
    const generatedLessons = computed(() => allLessons.value)
    const slSkillCategories = computed(() => allSkillCategories.value)
    
    // 根据技能分类筛选题型
    const filteredExerciseTypes = computed(() => {
      if (!filters.value.skillCategory) return slExerciseTypes.value
      return slExerciseTypes.value.filter(type => type.skill_category_id === filters.value.skillCategory)
    })

    const getExerciseTypeName = (typeId) => {
      const type = slExerciseTypes.value.find(ex => ex.id === typeId)
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

    const getLessonName = (exercise) => {
      const lesson = exercise?.source_lesson || exercise?.lesson || exercise?.generated_lesson
      if (lesson) {
        return lesson.lesson_name || lesson.name || '无来源课程信息'
      }
      return exercise?.source_lesson_name || '无来源课程信息'
    }

    const getVocabDisplay = (exercise) => {
      const vocab = exercise?.vocab_package?.vocab
      if (!vocab) return '无关联单词信息'
      if (vocab.hsk_level) return `${vocab.word} (HSK${vocab.hsk_level})`
      return vocab.word || '无关联单词信息'
    }
    
    const getExercisePrompt = (exercise) => {
      return exercise.prompt || '无题干信息'
    }

    const getExerciseMedia = (exerciseId) => {
      const exercise = slExercises.value.find(e => e.id === exerciseId);
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
      slExercises.value.forEach(ex => {
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
          { params: { source: 'scenario_system' } }
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

    const getDifficultyText = (level) => {
      if (level === undefined || level === null || level === '') return '无难度信息'
      const map = { 1: '简单', 2: '中等', 3: '困难' }
      return map[level] || level
    }

    const getDifficultyClass = (level) => {
      const map = { 1: 'easy', 2: 'medium', 3: 'hard' }
      return map[level] || ''
    }

    return {
      searchQuery,
      filters,
      loading,
      filtersLoading,
      generatedLessons,
      slExerciseTypes,
      slSkillCategories,
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
      getLessonName,
      getVocabDisplay,
      getExercisePrompt,
      getExerciseMedia,
      getMediaRoleName,
      getMediaName,
      getDifficultyClass,
      getDifficultyText,
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
  color: #6a1b9a;
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
  background: linear-gradient(135deg, #f5f5f5 0%, #f3e5f5 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #6a1b9a;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 0.95rem;
}

.exercises-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.exercises-section h3 {
  margin: 0 0 20px 0;
  color: #6a1b9a;
}

.exercise-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 520px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: linear-gradient(135deg, #f3e5f5 0%, #ede7f6 100%);
  border-bottom: 2px solid #e0e0e0;
  flex-shrink: 0;
}

.header-left,
.header-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.type-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: #e1bee7;
  color: #4a148c;
}

.difficulty-badge {
  font-size: 0.85rem;
  font-weight: 600;
}

.card-body {
  padding: 15px;
  overflow-y: auto;
  flex: 1;
}

.exercise-prompt {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.6;
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
  color: #6a1b9a;
  font-weight: 600;
}

.meta-value {
  color: #333;
}

/* 已移至 ExerciseCard 组件的样式已删除 */

/* 卡片网格与分页样式 */
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
  border: 1px solid #ab47bc;
  background: white;
  color: #6a1b9a;
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

.difficulty-badge.easy {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 4px 10px;
  border-radius: 12px;
}
.difficulty-badge.medium {
  background: #fff3e0;
  color: #ef6c00;
  padding: 4px 10px;
  border-radius: 12px;
}
.difficulty-badge.hard {
  background: #ffebee;
  color: #c62828;
  padding: 4px 10px;
  border-radius: 12px;
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
  background: #f3e5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #6a1b9a;
}

.btn-small {
  padding: 4px 12px;
  border: 1px solid #ab47bc;
  background: white;
  color: #ab47bc;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-small:hover {
  background: #ab47bc;
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
  color: #6a1b9a;
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
}

.detail-section {
  margin-bottom: 24px;
}

.info-label {
  font-weight: 600;
  color: #6a1b9a;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.detail-text {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  line-height: 1.6;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.meta-block {
  margin-bottom: 12px;
}

.meta-title {
  font-weight: 600;
  color: #6a1b9a;
  margin-bottom: 6px;
  font-size: 0.95rem;
}

.meta-text {
  background: #f9f9f9;
  padding: 12px;
  border-radius: 8px;
  line-height: 1.6;
}

.media-section {
  background: #f3e5f5;
  padding: 12px;
  border-radius: 8px;
  margin-top: 12px;
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
  color: #7b1fa2;
  font-size: 0.85rem;
}

.media-type {
  color: #666;
  font-size: 0.8rem;
  margin-left: auto;
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
  background: #f5f5f5;
  border-radius: 6px;
  padding: 10px;
}

.meta-subtitle {
  font-weight: 600;
  color: #6a1b9a;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 6px;
}

.option-key {
  font-weight: bold;
  margin-right: 10px;
  color: #6a1b9a;
}

.correct-mark {
  margin-left: auto;
  color: #4caf50;
  font-weight: bold;
}

.explanation-box {
  padding: 10px;
  background: #fff3e0;
  border-radius: 6px;
  border-left: 4px solid #ff9800;
  color: #e65100;
  margin-top: 10px;
}

.json-view {
  background: #282c34;
  color: #abb2bf;
  padding: 15px;
  border-radius: 8px;
  overflow-x: auto;
}

.media-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.media-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 6px;
  gap: 10px;
}

.media-name {
  font-weight: 500;
  color: #333;
  max-width: 260px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.media-role {
  font-weight: 500;
  color: #1565c0;
}

.media-type {
  margin-left: auto;
  color: #666;
  font-size: 0.85rem;
}

.detail-footer {
  padding: 20px;
  border-top: 1px solid #eee;
  text-align: right;
}

.btn-primary {
  padding: 8px 24px;
  background: #ab47bc;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover {
  background: #8e24aa;
}
</style>
