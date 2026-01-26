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
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-item">
            <label>来源课程：</label>
            <select v-model="filters.lessonId" class="filter-select">
              <option value="">全部</option>
              <option v-for="lesson in generatedLessons" :key="lesson.lesson_db_id" :value="lesson.lesson_db_id">
                {{ lesson.lesson_name }}
              </option>
            </select>
          </div>
          
          <div class="filter-item">
            <label>题型：</label>
            <select v-model="filters.exerciseType" class="filter-select">
              <option value="">全部</option>
              <option v-for="type in slExerciseTypes" :key="type.id" :value="type.id">
                {{ type.name }}
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

      <!-- 题目列表 (表格形式) -->
      <div class="exercises-section">
        <h3>🎯 AI生成的题目</h3>
        <div v-if="filteredExercises.length > 0" class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th style="width: 80px;">ID</th>
                <th style="width: 34%;">题目内容</th>
                <th style="width: 16%;">来源课程</th>
                <th style="width: 12%;">题型</th>
                <th style="width: 12%;">技能分类</th>
                <th style="width: 8%;">难度</th>
                <th style="width: 10%;">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="exercise in filteredExercises" :key="exercise.id">
                <td><code>{{ exercise.id }}</code></td>
                <td class="col-content" :title="getExercisePrompt(exercise)">
                  {{ getTruncatedPrompt(exercise) }}
                </td>
                <td>{{ getLessonName(exercise) }}</td>
                <td>{{ getExerciseTypeName(exercise.exercise_type_id) }}</td>
                <td>{{ getSkillCategoryName(exercise) }}</td>
                <td>
                  <span v-if="exercise.difficulty_level" v-for="n in exercise.difficulty_level" :key="n" style="color: #ab47bc;">★</span>
                  <span v-else>{{ getDifficultyText(exercise.difficulty_level) }}</span>
                </td>
                <td>
                  <button class="btn-small btn-view" @click="openDetail(exercise)">详情</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="empty-state">
          <div class="empty-icon">🤖</div>
          <h3>暂无AI生成的题目</h3>
          <p>{{ searchQuery ? '没有找到匹配的题目' : '暂无题目' }}</p>
        </div>
      </div>

      <!-- 详情弹窗 -->
      <div v-if="showDetailModal" class="detail-modal" @click.self="closeDetailModal">
        <div class="detail-modal-content">
          <div class="detail-header">
            <h3>AI题目详情</h3>
            <button class="close-btn" @click="closeDetailModal">×</button>
          </div>
          <div class="detail-body" v-if="selectedExercise">
            <div class="detail-section">
              <div class="info-label">题干</div>
              <div class="detail-text">{{ getExercisePrompt(selectedExercise) }}</div>
            </div>

            <div class="detail-section">
              <div class="info-label">基本信息</div>
              <div class="detail-grid">
                <div class="detail-item">
                  <span class="label">来源课程:</span> {{ getLessonName(selectedExercise) }}
                </div>
                <div class="detail-item">
                  <span class="label">题型:</span> {{ getExerciseTypeName(selectedExercise.exercise_type_id) }}
                </div>
                <div class="detail-item">
                  <span class="label">技能分类:</span> {{ getSkillCategoryName(selectedExercise) }}
                </div>
                <div class="detail-item">
                  <span class="label">难度:</span> {{ getDifficultyText(selectedExercise.difficulty_level) }}
                </div>
              </div>
            </div>

            <!-- 元数据展示 -->
            <div class="detail-section" v-if="selectedExercise.metadata">
              <div class="info-label">题目详情</div>
              <div class="metadata-content">
                <!-- 选择题 -->
                <div v-if="selectedExercise.metadata.options" class="options-list">
                   <div class="question-text" v-if="selectedExercise.metadata.question">{{ selectedExercise.metadata.question }}</div>
                   <div v-for="(option, idx) in selectedExercise.metadata.options" :key="idx" class="option-item">
                     <span class="option-key">{{ String.fromCharCode(65 + idx) }}.</span>
                     <span class="option-text">{{ option }}</span>
                     <span v-if="option === selectedExercise.metadata.correct_answer" class="correct-mark">✓</span>
                   </div>
                   <div v-if="selectedExercise.metadata.explanation" class="explanation-box">
                     <strong>💡 AI解析：</strong>{{ selectedExercise.metadata.explanation }}
                   </div>
                </div>
                <!-- 通用元数据 -->
                <pre class="json-view" v-else>{{ JSON.stringify(selectedExercise.metadata, null, 2) }}</pre>
              </div>
            </div>

            <!-- 媒体关联 -->
            <div class="detail-section" v-if="getExerciseMedia(selectedExercise.id).length > 0">
              <div class="info-label">关联媒体</div>
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
  name: 'ScenarioSystemExercises',
  components: {
    Header
  },
  setup() {
    const searchQuery = ref('')
    const showDetailModal = ref(false)
    const selectedExercise = ref(null)
    
    // 筛选条件
    const filters = ref({
      lessonId: '',
      exerciseType: '',
      difficulty: ''
    })
    
    // 数据
    const slExercises = ref([])
    
    // 获取题目数据
    const fetchExercises = async () => {
      try {
        const res = await request.get('/v1/questions', {
          params: {
            source: 'scenario_system',
            size: 10
          }
        })
        if (res.data && res.data.items) {
          slExercises.value = res.data.items
        }
      } catch (error) {
        console.error('获取题目失败:', error)
      }
    }

    onMounted(() => {
      fetchExercises()
    })

    // 筛选后的题目列表
    const filteredExercises = computed(() => {
      let result = slExercises.value
      
      // 课程筛选
      if (filters.value.lessonId) {
        result = result.filter(ex => ex.source_lesson_db_id === parseInt(filters.value.lessonId))
      }
      
      // 题型筛选
      if (filters.value.exerciseType) {
        result = result.filter(ex => ex.exercise_type_id === filters.value.exerciseType)
      }
      
      // 难度筛选
      if (filters.value.difficulty) {
        result = result.filter(ex => ex.difficulty_level === parseInt(filters.value.difficulty))
      }
      
      // 搜索筛选
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(ex => {
          const prompt = getExercisePrompt(ex).toLowerCase()
          return prompt.includes(query)
        })
      }
      
      return result
    })
    
    const slExerciseTypes = computed(() => {
      const map = new Map()
      slExercises.value.forEach(ex => {
        const type = ex.exercise_type
        if (type && type.id !== undefined && type.id !== null && !map.has(type.id)) {
          map.set(type.id, type)
        }
      })
      return Array.from(map.values())
    })

    const generatedLessons = computed(() => {
      const map = new Map()
      slExercises.value.forEach(ex => {
        const lesson = ex.source_lesson || ex.lesson || ex.generated_lesson
        const lessonId = ex.source_lesson_db_id ?? lesson?.lesson_db_id ?? lesson?.id
        const lessonName = lesson?.lesson_name || lesson?.name || ex.source_lesson_name
        if (lessonId === undefined || lessonId === null) return
        if (!map.has(lessonId)) {
          map.set(lessonId, {
            lesson_db_id: lessonId,
            lesson_name: lessonName || '未命名课程'
          })
        }
      })
      return Array.from(map.values())
    })

    const getExerciseTypeName = (typeId) => {
      const type = slExerciseTypes.value.find(ex => ex.id === typeId)
      if (type) {
        return type.name || type.display_name || '无题型信息'
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

    const getLessonName = (exercise) => {
      const lesson = exercise?.source_lesson || exercise?.lesson || exercise?.generated_lesson
      if (lesson) {
        return lesson.lesson_name || lesson.name || '无来源课程信息'
      }
      return exercise?.source_lesson_name || '无来源课程信息'
    }
    
    const getExercisePrompt = (exercise) => {
      if (exercise.metadata && exercise.metadata.question) return exercise.metadata.question
      if (exercise.metadata && exercise.metadata.prompt) return exercise.metadata.prompt
      return exercise.prompt || '无题干信息'
    }

    const getTruncatedPrompt = (exercise) => {
      const prompt = getExercisePrompt(exercise)
      return prompt.length > 40 ? prompt.substring(0, 40) + '...' : prompt
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
    
    const getDifficultyText = (level) => {
      if (level === undefined || level === null || level === '') return '无难度信息'
      const map = { 1: '简单', 2: '中等', 3: '困难' }
      return map[level] || level
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
      generatedLessons,
      slExerciseTypes,
      filteredExercises,
      showDetailModal,
      selectedExercise,
      getExerciseTypeName,
      getSkillCategoryName,
      getLessonName,
      getExercisePrompt,
      getTruncatedPrompt,
      getExerciseMedia,
      getMediaRoleName,
      getMediaName,
      getDifficultyText,
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
  color: #6a1b9a;
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
  min-width: 150px;
  transition: border-color 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #ab47bc;
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
  border-color: #ab47bc;
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
