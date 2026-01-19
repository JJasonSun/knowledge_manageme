<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <div class="header-left">
          <h2>📚 Content System - 题目管理</h2>
          <p class="subtitle">基础课程体系题目库</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-add" @click="showCreateModal = true">+ 添加题目</button>
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
        <div class="stat-card">
          <div class="stat-number">{{ exercisesBySkill.listening }}</div>
          <div class="stat-label">听力题</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ exercisesBySkill.reading }}</div>
          <div class="stat-label">阅读题</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ exercisesBySkill.writing }}</div>
          <div class="stat-label">写作题</div>
        </div>
      </div>

      <!-- 题目卡片列表 -->
      <div class="exercises-section">
        <h3>📝 题目列表</h3>
        <div v-if="filteredExercises.length > 0" class="exercises-grid">
          <div v-for="exercise in filteredExercises" :key="exercise.id" class="exercise-card">
            <!-- 卡片头部 -->
            <div class="card-header">
              <div class="header-left">
                <span class="skill-badge" :class="getSkillClass(exercise)">
                  {{ getSkillName(exercise) }}
                </span>
                <span class="type-badge">{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
              </div>
              <div class="header-right">
                <span class="difficulty-badge" :class="getDifficultyClass(exercise.difficulty_level)">
                  {{ getDifficultyText(exercise.difficulty_level) }}
                </span>
                <span class="status-badge" :class="getQualityClass(exercise.quality_status)">
                  {{ getQualityText(exercise.quality_status) }}
                </span>
              </div>
            </div>

            <!-- 题目内容 -->
            <div class="card-body">
              <div class="exercise-id">
                <code>{{ exercise.id }}</code>
              </div>
              <div class="exercise-prompt">
                {{ exercise.prompt }}
              </div>

              <!-- 关联单词信息 -->
              <div v-if="exercise.word_id" class="word-info">
                <div class="info-label">🔤 关联单词：</div>
                <div class="word-details">
                  <span class="word-char">{{ getWordInfo(exercise.word_id).characters }}</span>
                  <span class="word-pinyin">{{ getWordInfo(exercise.word_id).pinyin }}</span>
                  <span class="word-translation">{{ getWordInfo(exercise.word_id).translation }}</span>
                  <span class="hsk-badge">HSK{{ getWordInfo(exercise.word_id).hsk_level }}</span>
                </div>
              </div>

              <!-- 题目元数据 -->
              <div class="metadata-section">
                <div class="info-label">📋 题目详情：</div>
                <div class="metadata-content">
                  <!-- 选择题选项 -->
                  <div v-if="exercise.metadata.options" class="options-list">
                    <div v-for="option in exercise.metadata.options" :key="option.key" class="option-item">
                      <span class="option-key">{{ option.key }}.</span>
                      <span class="option-text">{{ option.text }}</span>
                      <span v-if="option.key === exercise.metadata.correct_answer" class="correct-mark">✓</span>
                    </div>
                  </div>
                  
                  <!-- 判断题 -->
                  <div v-if="exercise.metadata.audio_text" class="audio-text">
                    <strong>音频文本：</strong>{{ exercise.metadata.audio_text }}
                    <span class="answer-badge">答案: {{ exercise.metadata.correct_answer ? '正确' : '错误' }}</span>
                  </div>
                  
                  <!-- 阅读理解 -->
                  <div v-if="exercise.metadata.passage" class="passage-content">
                    <div class="passage-text">{{ exercise.metadata.passage }}</div>
                    <div v-if="exercise.metadata.questions" class="questions-list">
                      <div v-for="(q, idx) in exercise.metadata.questions" :key="idx" class="question-item">
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
                  <div v-if="exercise.metadata.blanks" class="blanks-list">
                    <div v-for="blank in exercise.metadata.blanks" :key="blank.position" class="blank-item">
                      <strong>答案：</strong>{{ blank.correct_answer }}
                      <span class="hint-text">（提示：{{ blank.hints }}）</span>
                    </div>
                  </div>
                  
                  <!-- 朗读题 -->
                  <div v-if="exercise.metadata.sentence" class="sentence-content">
                    <div class="sentence-text">{{ exercise.metadata.sentence }}</div>
                    <div v-if="exercise.metadata.pronunciation_tips" class="tips-text">
                      💡 {{ exercise.metadata.pronunciation_tips }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- 关联媒体 -->
              <div v-if="getExerciseMedia(exercise.id).length > 0" class="media-section">
                <div class="info-label">🎬 关联媒体：</div>
                <div class="media-list">
                  <div v-for="media in getExerciseMedia(exercise.id)" :key="media.id" class="media-item">
                    <span class="media-icon">{{ media.file_type === 'audio' ? '🔊' : '🖼️' }}</span>
                    <span class="media-role">{{ getMediaRoleName(media.usage_role) }}</span>
                    <span class="media-type">{{ media.mime_type }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 卡片底部 -->
            <div class="card-footer">
              <div class="creator-info">
                <span class="creator-badge" :class="getCreatorClass(exercise.created_by)">
                  {{ getCreatorText(exercise.created_by) }}
                </span>
                <span class="create-time">{{ formatDate(exercise.created_at) }}</span>
              </div>
              <div class="action-btns">
                <button class="btn-small btn-view" @click="viewExercise(exercise)">详情</button>
                <button v-if="canModify(exercise)" class="btn-small btn-edit" @click="editExercise(exercise)">编辑</button>
                <button v-if="canModify(exercise)" class="btn-small btn-danger" @click="deleteExercise(exercise)">删除</button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>暂无题目数据</h3>
          <p>{{ searchQuery ? '没有找到匹配的题目' : '开始添加第一道题目吧' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import Header from '../../components/Header.vue'
import { useAuthStore } from '../../stores/auth'
import { contentSystemMock } from '../../mock/exerciseData'

export default {
  name: 'ContentSystemExercises',
  components: {
    Header
  },
  setup() {
    const authStore = useAuthStore()
    const searchQuery = ref('')
    const showCreateModal = ref(false)
    
    // 筛选条件
    const filters = ref({
      skillCategory: '',
      exerciseType: '',
      difficulty: '',
      qualityStatus: ''
    })
    
    // Mock 数据
    const skillCategories = ref(contentSystemMock.skillCategories)
    const exerciseTypes = ref(contentSystemMock.exerciseTypes)
    const exercises = ref(contentSystemMock.exercises)
    const words = ref(contentSystemMock.words)
    const mediaAssets = ref(contentSystemMock.mediaAssets)
    const exerciseMediaAssets = ref(contentSystemMock.exerciseMediaAssets)
    
    // 根据技能分类筛选题型
    const filteredExerciseTypes = computed(() => {
      if (!filters.value.skillCategory) return exerciseTypes.value
      return exerciseTypes.value.filter(type => type.skill_category_id === filters.value.skillCategory)
    })
    
    // 筛选后的题目列表
    const filteredExercises = computed(() => {
      let result = exercises.value
      
      // 技能分类筛选
      if (filters.value.skillCategory) {
        const typeIds = exerciseTypes.value
          .filter(t => t.skill_category_id === filters.value.skillCategory)
          .map(t => t.id)
        result = result.filter(ex => typeIds.includes(ex.exercise_type_id))
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
        result = result.filter(ex => ex.prompt.toLowerCase().includes(query))
      }
      
      return result
    })
    
    // 按技能统计
    const exercisesBySkill = computed(() => {
      const stats = { listening: 0, speaking: 0, reading: 0, writing: 0 }
      exercises.value.forEach(ex => {
        const type = exerciseTypes.value.find(t => t.id === ex.exercise_type_id)
        if (type) {
          const skill = skillCategories.value.find(s => s.id === type.skill_category_id)
          if (skill) {
            stats[skill.name] = (stats[skill.name] || 0) + 1
          }
        }
      })
      return stats
    })
    
    const getSkillName = (exercise) => {
      const type = exerciseTypes.value.find(t => t.id === exercise.exercise_type_id)
      if (type) {
        const skill = skillCategories.value.find(s => s.id === type.skill_category_id)
        return skill ? skill.description : '-'
      }
      return '-'
    }
    
    const getSkillClass = (exercise) => {
      const type = exerciseTypes.value.find(t => t.id === exercise.exercise_type_id)
      if (type) {
        const skill = skillCategories.value.find(s => s.id === type.skill_category_id)
        return skill ? `skill-${skill.name}` : ''
      }
      return ''
    }
    
    const getExerciseTypeName = (typeId) => {
      const type = exerciseTypes.value.find(t => t.id === typeId)
      return type ? type.display_name : '-'
    }
    
    const getDifficultyText = (level) => {
      const map = { 1: '简单', 2: '中等', 3: '困难' }
      return map[level] || level
    }
    
    const getDifficultyClass = (level) => {
      const map = { 1: 'easy', 2: 'medium', 3: 'hard' }
      return map[level] || ''
    }
    
    const getQualityText = (status) => {
      const map = { 1: '已通过', 0: '待审核', '-1': '已驳回' }
      return map[status] || status
    }
    
    const getQualityClass = (status) => {
      const map = { 1: 'approved', 0: 'pending', '-1': 'rejected' }
      return map[status] || ''
    }
    
    const getCreatorText = (creator) => {
      if (creator === 'admin') return '管理员'
      if (creator === authStore.user?.username) return '我的'
      return creator
    }
    
    const getCreatorClass = (creator) => {
      if (creator === authStore.user?.username) return 'creator-me'
      if (creator === 'admin') return 'creator-admin'
      return 'creator-other'
    }
    
    const canModify = (exercise) => {
      return exercise.created_by === authStore.user?.username || authStore.user?.role === 'admin'
    }
    
    const getWordInfo = (wordId) => {
      const word = words.value.find(w => w.id === wordId)
      return word || { characters: '-', pinyin: '-', translation: '-', hsk_level: '-' }
    }
    
    const getExerciseMedia = (exerciseId) => {
      const relations = exerciseMediaAssets.value.filter(em => em.exercise_id === exerciseId)
      return relations.map(rel => {
        const media = mediaAssets.value.find(m => m.id === rel.media_asset_id)
        return media ? { ...media, usage_role: rel.usage_role } : null
      }).filter(m => m !== null)
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
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }
    
    const viewExercise = (exercise) => {
      console.log('查看题目:', exercise)
      const wordInfo = exercise.word_id ? getWordInfo(exercise.word_id) : null
      const mediaInfo = getExerciseMedia(exercise.id)
      
      let details = `题目详情\n\n`
      details += `ID: ${exercise.id}\n`
      details += `题干: ${exercise.prompt}\n\n`
      
      if (wordInfo && wordInfo.characters !== '-') {
        details += `关联单词: ${wordInfo.characters} (${wordInfo.pinyin}) - ${wordInfo.translation}\n\n`
      }
      
      details += `元数据:\n${JSON.stringify(exercise.metadata, null, 2)}\n\n`
      
      if (mediaInfo.length > 0) {
        details += `关联媒体:\n`
        mediaInfo.forEach(m => {
          details += `- ${getMediaRoleName(m.usage_role)}: ${m.file_type} (${m.mime_type})\n`
        })
      }
      
      alert(details)
    }
    
    const editExercise = (exercise) => {
      console.log('编辑题目:', exercise)
      alert('编辑功能开发中...')
    }
    
    const deleteExercise = (exercise) => {
      if (confirm(`确定要删除题目 "${exercise.prompt.slice(0, 20)}..." 吗？`)) {
        console.log('删除题目:', exercise)
        alert('删除功能开发中...')
      }
    }
    
    return {
      authStore,
      searchQuery,
      showCreateModal,
      filters,
      skillCategories,
      exerciseTypes,
      filteredExerciseTypes,
      filteredExercises,
      exercisesBySkill,
      words,
      mediaAssets,
      getSkillName,
      getSkillClass,
      getExerciseTypeName,
      getDifficultyText,
      getDifficultyClass,
      getQualityText,
      getQualityClass,
      getCreatorText,
      getCreatorClass,
      canModify,
      getWordInfo,
      getExerciseMedia,
      getMediaRoleName,
      formatDate,
      viewExercise,
      editExercise,
      deleteExercise
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

.btn-add {
  padding: 12px 24px;
  background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
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

.exercises-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
}

.exercise-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
}

.exercise-card:hover {
  border-color: #66bb6a;
  box-shadow: 0 4px 16px rgba(102, 187, 106, 0.2);
  transform: translateY(-2px);
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

.card-body {
  padding: 20px;
}

.exercise-id {
  margin-bottom: 12px;
}

.exercise-id code {
  background: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #d32f2f;
  font-weight: 600;
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

.info-label {
  font-weight: 600;
  color: #2e7d32;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.word-details {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.word-char {
  font-size: 1.3rem;
  font-weight: bold;
  color: #1b5e20;
}

.word-pinyin {
  color: #666;
  font-style: italic;
}

.word-translation {
  color: #555;
}

.hsk-badge {
  background: #2e7d32;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
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

.table-container {
  display: none; /* 隐藏旧的表格样式 */
}

.table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table thead {
  background: linear-gradient(135deg, #81c784 0%, #66bb6a 100%);
  color: white;
}

.table th {
  padding: 15px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 0.95rem;
}

.table td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.95rem;
}

.table tbody tr:hover {
  background-color: #f9f9f9;
}

.text-ellipsis {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

code {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #d32f2f;
}

.skill-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.skill-listening {
  background-color: #e3f2fd;
  color: #1565c0;
}

.skill-speaking {
  background-color: #fce4ec;
  color: #c2185b;
}

.skill-reading {
  background-color: #fff3e0;
  color: #e65100;
}

.skill-writing {
  background-color: #f3e5f5;
  color: #6a1b9a;
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

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.approved {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.rejected {
  background-color: #f8d7da;
  color: #721c24;
}

.creator-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.creator-me {
  background-color: #cce5ff;
  color: #004085;
}

.creator-admin {
  background-color: #e2e3e5;
  color: #383d41;
}

.creator-other {
  background-color: #d6d8db;
  color: #1b1e21;
}

.action-btns {
  display: flex;
  gap: 5px;
}

.btn-small {
  padding: 6px 12px;
  font-size: 0.85rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.btn-view {
  background-color: #2196f3;
  color: white;
}

.btn-view:hover {
  background-color: #1976d2;
}

.btn-edit {
  background-color: #6c757d;
  color: white;
}

.btn-edit:hover {
  background-color: #5a6268;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #666;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.empty-state p {
  margin: 0;
  color: #999;
}
</style>
