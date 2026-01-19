<template>
  <div>
    <Header />
    <div class="container">
      <div class="page-header">
        <div class="header-left">
          <h2>🤖 Scenario Learning System - AI生成题目</h2>
          <p class="subtitle">基于AI动态生成的情境学习题目库</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-generate" @click="showGenerateModal = true">✨ AI生成题目</button>
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

      <!-- 统计信息 -->
      <div class="stats-section">
        <div class="stat-card ai-card">
          <div class="stat-icon">🤖</div>
          <div class="stat-number">{{ filteredExercises.length }}</div>
          <div class="stat-label">AI生成题目总数</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-number">{{ generatedLessons.length }}</div>
          <div class="stat-label">生成课程数</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📝</div>
          <div class="stat-number">{{ topics.length }}</div>
          <div class="stat-label">生成主题数</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📖</div>
          <div class="stat-number">{{ vocabulary.length }}</div>
          <div class="stat-label">词汇库数量</div>
        </div>
      </div>

      <!-- 生成课程列表 -->
      <div class="lessons-section">
        <h3>📚 生成的课程</h3>
        <div class="lessons-grid">
          <div v-for="lesson in generatedLessons" :key="lesson.lesson_db_id" class="lesson-card">
            <div class="lesson-header">
              <span class="lesson-type-badge" :class="lesson.type">
                {{ lesson.type === 'dialogue' ? '对话' : '文章' }}
              </span>
              <h4>{{ lesson.lesson_name }}</h4>
            </div>
            <div class="lesson-meta">
              <span>📅 {{ formatDate(lesson.generated_at) }}</span>
              <span>🔖 {{ getTopicName(lesson.topic_id) }}</span>
            </div>
            <div class="lesson-stats">
              <span>题目数: {{ getExerciseCountByLesson(lesson.lesson_db_id) }}</span>
              <span>词汇数: {{ getVocabCountByLesson(lesson.lesson_db_id) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 题目卡片列表 -->
      <div class="exercises-section">
        <h3>🎯 AI生成的题目</h3>
        <div v-if="filteredExercises.length > 0" class="exercises-grid">
          <div v-for="exercise in filteredExercises" :key="exercise.id" class="exercise-card">
            <!-- 卡片头部 -->
            <div class="card-header">
              <div class="header-left">
                <span class="ai-badge">🤖 AI生成</span>
                <span class="type-badge">{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
              </div>
              <div class="header-right">
                <span class="difficulty-badge" :class="getDifficultyClass(exercise.difficulty_level)">
                  {{ getDifficultyText(exercise.difficulty_level) }}
                </span>
              </div>
            </div>

            <!-- 题目内容 -->
            <div class="card-body">
              <div class="exercise-id">
                <code>{{ exercise.id }}</code>
              </div>

              <!-- 来源课程信息 -->
              <div class="lesson-info">
                <div class="info-label">📚 来源课程：</div>
                <div class="lesson-details">
                  <span class="lesson-name">{{ getLessonInfo(exercise.source_lesson_db_id).lesson_name }}</span>
                  <span class="lesson-type-badge" :class="getLessonInfo(exercise.source_lesson_db_id).type">
                    {{ getLessonInfo(exercise.source_lesson_db_id).type === 'dialogue' ? '对话' : '文章' }}
                  </span>
                  <span class="topic-badge">{{ getTopicName(getLessonInfo(exercise.source_lesson_db_id).topic_id) }}</span>
                </div>
              </div>

              <!-- 关联词汇信息 -->
              <div v-if="exercise.vocab_package_db_id" class="vocab-info">
                <div class="info-label">🔤 考察词汇：</div>
                <div class="vocab-details">
                  <span class="vocab-word">{{ getVocabInfo(exercise.vocab_package_db_id).word }}</span>
                  <span class="vocab-pinyin">{{ getVocabInfo(exercise.vocab_package_db_id).pinyin }}</span>
                  <span class="vocab-translation">{{ getVocabInfo(exercise.vocab_package_db_id).translation }}</span>
                  <span class="hsk-badge">HSK{{ getVocabInfo(exercise.vocab_package_db_id).hsk_level }}</span>
                </div>
              </div>

              <!-- 题目元数据 -->
              <div class="metadata-section">
                <div class="info-label">📋 题目详情：</div>
                <div class="metadata-content">
                  <!-- 选择题 -->
                  <div v-if="exercise.metadata.question" class="question-section">
                    <div class="question-text">{{ exercise.metadata.question }}</div>
                    <div v-if="exercise.metadata.options" class="options-list">
                      <div v-for="(option, idx) in exercise.metadata.options" :key="idx" class="option-item">
                        <span class="option-key">{{ String.fromCharCode(65 + idx) }}.</span>
                        <span class="option-text">{{ option }}</span>
                        <span v-if="option === exercise.metadata.correct_answer" class="correct-mark">✓</span>
                      </div>
                    </div>
                    <div v-if="exercise.metadata.explanation" class="explanation-box">
                      <strong>💡 AI解析：</strong>{{ exercise.metadata.explanation }}
                    </div>
                  </div>

                  <!-- 造句题 -->
                  <div v-if="exercise.metadata.prompt" class="prompt-section">
                    <div class="prompt-text">{{ exercise.metadata.prompt }}</div>
                    <div v-if="exercise.metadata.sample_answer" class="sample-answer">
                      <strong>参考答案：</strong>{{ exercise.metadata.sample_answer }}
                    </div>
                    <div v-if="exercise.metadata.evaluation_criteria" class="criteria-list">
                      <strong>评分标准：</strong>
                      <ul>
                        <li v-for="(criterion, idx) in exercise.metadata.evaluation_criteria" :key="idx">
                          {{ criterion }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 课程内容预览 -->
              <div class="lesson-preview">
                <div class="info-label">📖 课程内容预览：</div>
                <div class="preview-content">
                  <!-- 对话内容 -->
                  <div v-if="getLessonInfo(exercise.source_lesson_db_id).type === 'dialogue'" class="dialogue-preview">
                    <div v-for="(line, idx) in getDialogueContent(exercise.source_lesson_db_id)" :key="idx" class="dialogue-line">
                      <span class="role-name">{{ line.role_name }}：</span>
                      <span class="dialogue-text">{{ line.text }}</span>
                    </div>
                  </div>
                  <!-- 文章内容 -->
                  <div v-else class="passage-preview">
                    <div v-for="(para, idx) in getLessonInfo(exercise.source_lesson_db_id).passage?.paragraphs || []" :key="idx" class="paragraph">
                      {{ para }}
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
                <span class="ai-creator-badge">🤖 AI系统</span>
                <span class="create-time">{{ formatDate(exercise.created_at) }}</span>
              </div>
              <div class="action-btns">
                <button class="btn-small btn-view" @click="viewExercise(exercise)">详情</button>
                <button class="btn-small btn-regenerate" @click="regenerateExercise(exercise)">重新生成</button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <div class="empty-icon">🤖</div>
          <h3>暂无AI生成的题目</h3>
          <p>{{ searchQuery ? '没有找到匹配的题目' : '点击"AI生成题目"开始创建' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import Header from '../../components/Header.vue'
import { useAuthStore } from '../../stores/auth'
import { scenarioSystemMock } from '../../mock/exerciseData'

export default {
  name: 'ScenarioSystemExercises',
  components: {
    Header
  },
  setup() {
    const authStore = useAuthStore()
    const searchQuery = ref('')
    const showGenerateModal = ref(false)
    
    // 筛选条件
    const filters = ref({
      lessonId: '',
      exerciseType: '',
      difficulty: ''
    })
    
    // Mock 数据
    const topics = ref(scenarioSystemMock.topics)
    const generatedLessons = ref(scenarioSystemMock.generatedLessons)
    const dialogues = ref(scenarioSystemMock.dialogues)
    const slExerciseTypes = ref(scenarioSystemMock.slExerciseTypes)
    const slExercises = ref(scenarioSystemMock.slExercises)
    const vocabulary = ref(scenarioSystemMock.vocabulary)
    const generatedVocabPackages = ref(scenarioSystemMock.generatedVocabPackages)
    const slMediaAssets = ref(scenarioSystemMock.slMediaAssets)
    const slExerciseMediaAssets = ref(scenarioSystemMock.slExerciseMediaAssets)
    
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
    
    const getTopicName = (topicId) => {
      const topic = topics.value.find(t => t.topic_id === topicId)
      return topic ? topic.topic_name : '-'
    }
    
    const getLessonName = (lessonId) => {
      const lesson = generatedLessons.value.find(l => l.lesson_db_id === lessonId)
      return lesson ? lesson.lesson_name : '-'
    }
    
    const getExerciseTypeName = (typeId) => {
      const type = slExerciseTypes.value.find(t => t.id === typeId)
      return type ? type.name : '-'
    }
    
    const getExercisePrompt = (exercise) => {
      if (exercise.metadata.question) return exercise.metadata.question
      if (exercise.metadata.prompt) return exercise.metadata.prompt
      return '查看详情'
    }
    
    const getLessonInfo = (lessonId) => {
      const lesson = generatedLessons.value.find(l => l.lesson_db_id === lessonId)
      return lesson || { lesson_name: '-', type: 'passage', topic_id: null, passage: null }
    }
    
    const getVocabInfo = (vocabPackageId) => {
      const vocabPackage = generatedVocabPackages.value.find(vp => vp.vocab_package_db_id === vocabPackageId)
      if (vocabPackage) {
        const vocab = vocabulary.value.find(v => v.vocab_uuid === vocabPackage.vocab_uuid)
        return vocab || { word: '-', pinyin: '-', translation: '-', hsk_level: '-' }
      }
      return { word: '-', pinyin: '-', translation: '-', hsk_level: '-' }
    }
    
    const getDialogueContent = (lessonId) => {
      const dialogue = dialogues.value.find(d => d.lesson_db_id === lessonId)
      if (dialogue) {
        return dialogue.dialogues.map(line => ({
          role_name: dialogue.roles[line.role],
          text: line.text
        }))
      }
      return []
    }
    
    const getExerciseMedia = (exerciseId) => {
      const relations = slExerciseMediaAssets.value.filter(em => em.exercise_id === exerciseId)
      return relations.map(rel => {
        const media = slMediaAssets.value.find(m => m.id === rel.media_asset_id)
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
    
    const getExerciseCountByLesson = (lessonId) => {
      return slExercises.value.filter(ex => ex.source_lesson_db_id === lessonId).length
    }
    
    const getVocabCountByLesson = (lessonId) => {
      return generatedVocabPackages.value.filter(vp => vp.lesson_db_id === lessonId).length
    }
    
    const getDifficultyText = (level) => {
      const map = { 1: '简单', 2: '中等', 3: '困难' }
      return map[level] || level
    }
    
    const getDifficultyClass = (level) => {
      const map = { 1: 'easy', 2: 'medium', 3: 'hard' }
      return map[level] || ''
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }
    
    const viewExercise = (exercise) => {
      console.log('查看AI生成题目:', exercise)
      const lessonInfo = getLessonInfo(exercise.source_lesson_db_id)
      const vocabInfo = getVocabInfo(exercise.vocab_package_db_id)
      const mediaInfo = getExerciseMedia(exercise.id)
      
      let details = `AI生成题目详情\n\n`
      details += `ID: ${exercise.id}\n`
      details += `来源课程: ${lessonInfo.lesson_name} (${lessonInfo.type === 'dialogue' ? '对话' : '文章'})\n`
      details += `考察词汇: ${vocabInfo.word} (${vocabInfo.pinyin}) - ${vocabInfo.translation}\n\n`
      details += `元数据:\n${JSON.stringify(exercise.metadata, null, 2)}\n\n`
      
      if (mediaInfo.length > 0) {
        details += `关联媒体:\n`
        mediaInfo.forEach(m => {
          details += `- ${getMediaRoleName(m.usage_role)}: ${m.file_type} (${m.mime_type})\n`
        })
      }
      
      alert(details)
    }
    
    const regenerateExercise = (exercise) => {
      if (confirm('确定要重新生成这道题目吗？')) {
        console.log('重新生成题目:', exercise)
        alert('重新生成功能开发中...')
      }
    }
    
    return {
      authStore,
      searchQuery,
      showGenerateModal,
      filters,
      topics,
      generatedLessons,
      slExerciseTypes,
      filteredExercises,
      vocabulary,
      getTopicName,
      getLessonName,
      getLessonInfo,
      getVocabInfo,
      getDialogueContent,
      getExerciseTypeName,
      getExercisePrompt,
      getExerciseMedia,
      getMediaRoleName,
      getExerciseCountByLesson,
      getVocabCountByLesson,
      getDifficultyText,
      getDifficultyClass,
      formatDate,
      viewExercise,
      regenerateExercise
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

.btn-generate {
  padding: 12px 24px;
  background: linear-gradient(135deg, #ab47bc 0%, #8e24aa 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(142, 36, 170, 0.3);
}

.btn-generate:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(142, 36, 170, 0.4);
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

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.stat-card {
  background: linear-gradient(135deg, #f5f5f5 0%, #fce4ec 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-card.ai-card {
  background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #6a1b9a;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.lessons-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.lessons-section h3 {
  margin: 0 0 20px 0;
  color: #6a1b9a;
}

.lessons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.lesson-card {
  background: linear-gradient(135deg, #f9f9f9 0%, #f3e5f5 100%);
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #ab47bc;
  transition: all 0.3s;
}

.lesson-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.lesson-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.lesson-type-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.lesson-type-badge.dialogue {
  background-color: #e1bee7;
  color: #6a1b9a;
}

.lesson-type-badge.passage {
  background-color: #c5cae9;
  color: #3f51b5;
}

.lesson-header h4 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.lesson-meta {
  display: flex;
  gap: 15px;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 10px;
}

.lesson-stats {
  display: flex;
  gap: 15px;
  font-size: 0.85rem;
  color: #6a1b9a;
  font-weight: 500;
}

.exercises-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-top: 20px;
}

.exercises-section h3 {
  margin: 0 0 20px 0;
  color: #6a1b9a;
}

.exercises-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(550px, 1fr));
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
  border-color: #ab47bc;
  box-shadow: 0 4px 16px rgba(171, 71, 188, 0.2);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: linear-gradient(135deg, #f5f5f5 0%, #f3e5f5 100%);
  border-bottom: 2px solid #e0e0e0;
}

.header-left,
.header-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.ai-badge {
  background: linear-gradient(135deg, #ab47bc 0%, #8e24aa 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.card-body {
  padding: 20px;
}

.exercise-id {
  margin-bottom: 12px;
}

.exercise-id code {
  background: #f3e5f5;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #6a1b9a;
  font-weight: 600;
}

.lesson-info {
  background: #f3e5f5;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.info-label {
  font-weight: 600;
  color: #6a1b9a;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.lesson-details {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.lesson-name {
  font-size: 1.1rem;
  font-weight: bold;
  color: #4a148c;
}

.topic-badge {
  background: #6a1b9a;
  color: white;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.vocab-info {
  background: #e1bee7;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.vocab-details {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.vocab-word {
  font-size: 1.3rem;
  font-weight: bold;
  color: #4a148c;
}

.vocab-pinyin {
  color: #666;
  font-style: italic;
}

.vocab-translation {
  color: #555;
}

.hsk-badge {
  background: #6a1b9a;
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

.question-section {
  padding: 10px;
  background: white;
  border-radius: 6px;
}

.question-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.6;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
}

.option-key {
  font-weight: bold;
  color: #6a1b9a;
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

.explanation-box {
  padding: 10px;
  background: #fff3e0;
  border-radius: 6px;
  border-left: 4px solid #ff9800;
  color: #e65100;
  font-size: 0.95rem;
}

.prompt-section {
  padding: 10px;
  background: white;
  border-radius: 6px;
}

.prompt-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  padding: 12px;
  background: #f3e5f5;
  border-radius: 6px;
}

.sample-answer {
  padding: 10px;
  background: #e8f5e9;
  border-radius: 6px;
  margin-bottom: 10px;
  border-left: 4px solid #4caf50;
}

.criteria-list {
  padding: 10px;
  background: #e3f2fd;
  border-radius: 6px;
}

.criteria-list ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.criteria-list li {
  margin: 4px 0;
  color: #1565c0;
}

.lesson-preview {
  background: #fff9e6;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.preview-content {
  margin-top: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.dialogue-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dialogue-line {
  padding: 8px 12px;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #ab47bc;
}

.role-name {
  font-weight: bold;
  color: #6a1b9a;
  margin-right: 8px;
}

.dialogue-text {
  color: #333;
}

.passage-preview {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.paragraph {
  padding: 10px;
  background: white;
  border-radius: 6px;
  line-height: 1.8;
  color: #333;
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

.ai-creator-badge {
  background: linear-gradient(135deg, #ab47bc 0%, #8e24aa 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
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
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.table-container h3 {
  margin: 0 0 20px 0;
  color: #6a1b9a;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table thead {
  background: linear-gradient(135deg, #ba68c8 0%, #ab47bc 100%);
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
  color: #6a1b9a;
}

.lesson-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
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

.btn-regenerate {
  background-color: #ab47bc;
  color: white;
}

.btn-regenerate:hover {
  background-color: #8e24aa;
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
