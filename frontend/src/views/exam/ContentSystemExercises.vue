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
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-item">
            <label>技能分类：</label>
            <select v-model="filters.skillCategory" class="filter-select">
              <option value="">全部</option>
              <option v-for="cat in skillCategories" :key="cat.id" :value="cat.id">
                {{ cat.description }}
              </option>
            </select>
          </div>
          
          <div class="filter-item">
            <label>题型：</label>
            <select v-model="filters.exerciseType" class="filter-select">
              <option value="">全部</option>
              <option v-for="type in filteredExerciseTypes" :key="type.id" :value="type.id">
                {{ type.display_name }}
              </option>
            </select>
          </div>
          
          <div class="filter-item">
            <label>难度：</label>
            <select v-model="filters.difficulty" class="filter-select">
              <option value="">全部</option>
              <option value="1">简单</option>
              <option value="2">中等</option>
              <option value="3">困难</option>
            </select>
          </div>
          
          <div class="filter-item">
            <label>质检状态：</label>
            <select v-model="filters.qualityStatus" class="filter-select">
              <option value="">全部</option>
              <option value="1">已通过</option>
              <option value="0">待审核</option>
              <option value="-1">已驳回</option>
            </select>
          </div>
        </div>
        
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            class="search-input"
            placeholder="搜索题目内容..."
          >
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="stats-section">
        <div class="stat-card">
          <div class="stat-number">{{ filteredExercises.length }}</div>
          <div class="stat-label">题目总数</div>
        </div>
      </div>

      <!-- 题目列表 (表格形式) -->
      <div class="exercises-section">
        <h3>📝 题目列表</h3>
        <div v-if="filteredExercises.length > 0" class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th style="width: 80px;">ID</th>
                <th style="width: 35%;">题目内容</th>
                <th style="width: 12%;">题型</th>
                <th style="width: 12%;">技能分类</th>
                <th style="width: 8%;">难度</th>
                <th style="width: 8%;">状态</th>
                <th style="width: 10%;">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="exercise in filteredExercises" :key="exercise.id">
                <td><code>{{ exercise.id }}</code></td>
                <td class="col-content" :title="getExercisePrompt(exercise)">
                  {{ getTruncatedPrompt(exercise) }}
                </td>
                <td>{{ getExerciseTypeName(exercise.exercise_type_id) }}</td>
                <td>{{ getSkillCategoryName(exercise) }}</td>
                <td>
                  <span v-if="exercise.difficulty_level" v-for="n in exercise.difficulty_level" :key="n" style="color: #ff9800;">★</span>
                  <span v-else>{{ getDifficultyText(exercise.difficulty_level) }}</span>
                </td>
                <td>
                  <span class="status-badge" :class="getQualityClass(exercise.quality_status)">
                    {{ getQualityText(exercise.quality_status) }}
                  </span>
                </td>
                <td>
                  <button class="btn-small btn-view" @click="openDetail(exercise)">详情</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>暂无题目数据</h3>
          <p>{{ searchQuery ? '没有找到匹配的题目' : '暂无题目' }}</p>
        </div>
      </div>

      <!-- 详情弹窗 -->
      <div v-if="showDetailModal" class="detail-modal" @click.self="closeDetailModal">
        <div class="detail-modal-content">
          <div class="detail-header">
            <h3>题目详情</h3>
            <button class="close-btn" @click="closeDetailModal">×</button>
          </div>
          <div class="detail-body" v-if="selectedExercise">
            <!-- 恢复原有的卡片样式展示 -->
            <div class="exercise-card detail-card">
              <!-- 卡片头部 -->
              <div class="card-header">
                <div class="header-left">
                  <span class="type-badge">{{ getExerciseTypeName(selectedExercise.exercise_type_id) }}</span>
                </div>
                <div class="header-right">
                  <span class="difficulty-badge" :class="getDifficultyClass(selectedExercise.difficulty_level)">
                    {{ getDifficultyText(selectedExercise.difficulty_level) }}
                  </span>
                  <span class="status-badge" :class="getQualityClass(selectedExercise.quality_status)">
                    {{ getQualityText(selectedExercise.quality_status) }}
                  </span>
                </div>
              </div>

              <!-- 题目内容 -->
              <div class="card-body">
                <div class="exercise-prompt">
                  {{ getExercisePrompt(selectedExercise) }}
                </div>

                <div class="word-info">
                  <div class="info-label">
                    🔤 关联单词：{{ getWordDisplay(selectedExercise) }}
                  </div>
                </div>

                <div class="exercise-meta">
                  <div class="meta-item">
                    <span class="meta-label">题型：</span>
                    <span class="meta-value">{{ getExerciseTypeName(selectedExercise.exercise_type_id) }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">技能分类：</span>
                    <span class="meta-value">{{ getSkillCategoryName(selectedExercise) }}</span>
                  </div>
                </div>

                <div class="metadata-section" v-if="selectedExercise.metadata">
                  <div class="info-label">📋 题目详情：</div>
                  <div class="metadata-content">
                    <!-- 选择题选项 -->
                    <div v-if="selectedExercise.metadata.options" class="options-list">
                      <div v-for="option in selectedExercise.metadata.options" :key="option.key" class="option-item">
                        <span class="option-key">{{ option.key }}.</span>
                        <span class="option-text">{{ option.text }}</span>
                        <span v-if="option.key === selectedExercise.metadata.correct_answer" class="correct-mark">✓</span>
                      </div>
                    </div>
                    
                    <!-- 判断题 -->
                    <div v-else-if="selectedExercise.metadata.audio_text" class="audio-text">
                      <strong>音频文本：</strong>{{ selectedExercise.metadata.audio_text }}
                      <span class="answer-badge">答案: {{ selectedExercise.metadata.correct_answer ? '正确' : '错误' }}</span>
                    </div>
                    
                    <!-- 阅读理解 -->
                    <div v-else-if="selectedExercise.metadata.passage" class="passage-content">
                      <div class="passage-text">{{ selectedExercise.metadata.passage }}</div>
                      <div v-if="selectedExercise.metadata.questions" class="questions-list">
                        <div v-for="(q, idx) in selectedExercise.metadata.questions" :key="idx" class="question-item">
                          <div class="question-text">{{ q.question }}</div>
                          <div class="question-options">
                            <span v-for="opt in q.options" :key="opt" class="q-option" :class="{ correct: opt === q.correct_answer }">
                              {{ opt }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- 填空题 -->
                    <div v-else-if="selectedExercise.metadata.blanks" class="blanks-list">
                      <div v-for="blank in selectedExercise.metadata.blanks" :key="blank.position" class="blank-item">
                        <strong>答案：</strong>{{ blank.correct_answer }}
                        <span class="hint-text">（提示：{{ blank.hints }}）</span>
                      </div>
                    </div>
                    
                    <!-- 朗读题 -->
                    <div v-else-if="selectedExercise.metadata.sentence" class="sentence-content">
                      <div class="sentence-text">{{ selectedExercise.metadata.sentence }}</div>
                      <div v-if="selectedExercise.metadata.pronunciation_tips" class="tips-text">
                        💡 {{ selectedExercise.metadata.pronunciation_tips }}
                      </div>
                    </div>

                    <!-- 通用展示 (如果没有匹配的特定结构) -->
                    <pre class="json-view" v-else>{{ JSON.stringify(selectedExercise.metadata, null, 2) }}</pre>
                  </div>
                </div>

                <div v-if="getExerciseMedia(selectedExercise.id).length > 0" class="media-section">
                  <div class="info-label">🎬 关联媒体：</div>
                  <div class="media-list">
                    <div v-for="media in getExerciseMedia(selectedExercise.id)" :key="media.id" class="media-item">
                      <span class="media-icon">{{ media.file_type === 'audio' ? '🔊' : '🖼️' }}</span>
                      <span class="media-name">{{ getMediaName(media) }}</span>
                      <span class="media-role">{{ getMediaRoleName(media.usage_role) }}</span>
                      <span class="media-type">{{ media.mime_type }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 卡片底部 -->
              <div class="card-footer">
                <div class="creator-info">
                  <span class="creator-badge">
                    {{ selectedExercise.created_by ? selectedExercise.created_by : '无创建者信息' }}
                  </span>
                  <span class="create-time">
                    {{ selectedExercise.created_at ? formatDate(selectedExercise.created_at) : '无创建时间信息' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div class="detail-footer">
            <button class="btn-primary" @click="closeDetailModal">关闭</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import Header from '../../components/Header.vue'
import request from '../../utils/request'

export default {
  name: 'ContentSystemExercises',
  components: {
    Header
  },
  setup() {
    const searchQuery = ref('')
    const showDetailModal = ref(false)
    const selectedExercise = ref(null)
    
    // 筛选条件
    const filters = ref({
      skillCategory: '',
      exerciseType: '',
      difficulty: '',
      qualityStatus: ''
    })
    
    // 数据
    const exercises = ref([])

    // 获取题目数据
    const fetchExercises = async () => {
      try {
        const res = await request.get('/v1/questions', {
          params: {
            source: 'content_system',
            size: 10
          }
        })
        if (res.data && res.data.items) {
          exercises.value = res.data.items
        }
      } catch (error) {
        console.error('获取题目失败:', error)
      }
    }

    onMounted(() => {
      fetchExercises()
    })
    
    // 根据技能分类筛选题型
    const exerciseTypes = computed(() => {
      const map = new Map()
      exercises.value.forEach(ex => {
        const type = ex.exercise_type
        if (type && type.id !== undefined && type.id !== null && !map.has(type.id)) {
          map.set(type.id, type)
        }
      })
      return Array.from(map.values())
    })

    const skillCategories = computed(() => {
      const map = new Map()
      exercises.value.forEach(ex => {
        const category = ex.exercise_type?.skill_category || ex.skill_category
        if (category && category.id !== undefined && category.id !== null && !map.has(category.id)) {
          map.set(category.id, category)
        }
      })
      return Array.from(map.values())
    })

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
      
      // 搜索筛选
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(ex => ex.prompt && ex.prompt.toLowerCase().includes(query))
      }
      
      return result
    })
    
    const getExerciseTypeName = (typeId) => {
      const type = exerciseTypes.value.find(ex => ex.id === typeId)
      if (type) {
        return type.display_name || type.name || '无题型信息'
      }
      return '无题型信息'
    }

    const getSkillCategoryName = (exercise) => {
      const category = exercise?.exercise_type?.skill_category || exercise?.skill_category
      if (category) {
        return category.description || category.name || '无技能分类信息'
      }
      return '无技能分类信息'
    }

    const getExercisePrompt = (exercise) => {
      if (!exercise) return '无题干信息'
      if (exercise.metadata && exercise.metadata.question) return exercise.metadata.question
      if (exercise.metadata && exercise.metadata.prompt) return exercise.metadata.prompt
      return exercise.prompt || '无题干信息'
    }

    const getTruncatedPrompt = (exercise) => {
      const prompt = getExercisePrompt(exercise)
      return prompt.length > 40 ? prompt.substring(0, 40) + '...' : prompt
    }

    const getWordDisplay = (exercise) => {
      const word = exercise?.word
      if (word) {
        return word.text || word.word || word.name || '无关联单词信息'
      }
      return exercise?.word_text || exercise?.word_name || '无关联单词信息'
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
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }

    const openDetail = (exercise) => {
      selectedExercise.value = exercise
      showDetailModal.value = true
    }

    const closeDetailModal = () => {
      showDetailModal.value = false
      selectedExercise.value = null
    }
    
    return {
      searchQuery,
      filters,
      skillCategories,
      exerciseTypes,
      filteredExerciseTypes,
      filteredExercises,
      showDetailModal,
      selectedExercise,
      getExerciseTypeName,
      getSkillCategoryName,
      getExercisePrompt,
      getTruncatedPrompt,
      getWordDisplay,
      getDifficultyText,
      getDifficultyClass,
      getQualityText,
      getQualityClass,
      getExerciseMedia,
      getMediaRoleName,
      getMediaName,
      formatDate,
      openDetail,
      closeDetailModal
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

.filter-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.filter-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-item label {
  font-weight: 500;
  color: #555;
  white-space: nowrap;
}

.filter-select {
  padding: 8px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.95rem;
  min-width: 120px;
  transition: border-color 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #66bb6a;
}

.search-box {
  margin-top: 15px;
}

.search-input {
  width: 100%;
  padding: 12px 20px;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #66bb6a;
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

/* 卡片样式还原 */
.exercise-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
  border-bottom: 2px solid #e0e0e0;
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

.card-body {
  padding: 20px;
}

.exercise-id {
  margin-bottom: 12px;
}

.exercise-prompt {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.6;
}

.word-info {
  background: #e8f5e9;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
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

.info-label {
  font-weight: 600;
  color: #2e7d32;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.metadata-section {
  background: #f9f9f9;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.metadata-content {
  margin-top: 8px;
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
  gap: 8px;
  margin-top: 8px;
}

.media-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: white;
  border-radius: 6px;
  font-size: 0.9rem;
}

.media-icon {
  font-size: 1.2rem;
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
  font-weight: 600;
  color: #1565c0;
}

.media-type {
  color: #666;
  font-size: 0.85rem;
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
