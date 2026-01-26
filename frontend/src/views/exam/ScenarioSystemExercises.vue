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

      <div class="exercises-section">
        <h3>🎯 AI生成的题目</h3>
        <div v-if="filteredExercises.length > 0" class="cards-grid">
          <div v-for="exercise in filteredExercises" :key="exercise.id" class="exercise-card">
            <div class="card-header">
              <div class="header-left">
                <span class="type-badge">{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
              </div>
              <div class="header-right">
                <span class="difficulty-badge" :class="getDifficultyClass(exercise.difficulty_level)">
                  {{ getDifficultyText(exercise.difficulty_level) }}
                </span>
              </div>
            </div>

            <div class="card-body">
              <div class="exercise-prompt">
                {{ getExercisePrompt(exercise) }}
              </div>

              <div class="word-info">
                <div class="info-label">📘 来源课程：{{ getLessonName(exercise) }}</div>
                <div class="info-label">🔤 关联单词：{{ getVocabDisplay(exercise) }}</div>
              </div>

              <div class="exercise-meta">
                <div class="meta-item">
                  <span class="meta-label">题型：</span>
                  <span class="meta-value">{{ getExerciseTypeName(exercise.exercise_type_id) }}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">技能分类：</span>
                  <span class="meta-value">{{ getSkillCategoryName(exercise) }}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">难度：</span>
                  <span class="meta-value">{{ getDifficultyText(exercise.difficulty_level) }}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">创建时间：</span>
                  <span class="meta-value">{{ formatDate(exercise.created_at) }}</span>
                </div>
              </div>

              <div class="metadata-section" v-if="exercise.metadata">
                <div class="info-label">题目详情</div>
                <div class="metadata-content">
                  <template v-if="isType(exercise, 'LISTEN_SENTENCE_QA')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">听力原文</div>
                      <div class="meta-text">{{ getTextValue(getField(exercise, 'listeningText'), '无听力原文信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">问题</div>
                      <div class="meta-text">
                        {{ getTextValue(getField(exercise, 'question'), '无问题信息') }}
                      </div>
                    </div>
                    <div class="meta-block" v-if="getOptions(exercise).length">
                      <div class="meta-title">选项</div>
                      <div class="options-list">
                        <div v-for="(option, idx) in getOptions(exercise)" :key="idx" class="option-item">
                          <span class="option-key">{{ getOptionLabel(option, idx) }}.</span>
                          <span class="option-text">{{ getOptionText(option) }}</span>
                          <span v-if="option.pinyin" class="option-pinyin">{{ option.pinyin }}</span>
                          <span v-if="isCorrectOptionByAnswer(getCorrectAnswer(exercise.metadata), option, idx)" class="correct-mark">✓</span>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确答案：{{ formatCorrectAnswer(exercise.metadata) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'LISTEN_SENTENCE_TF')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">听力原文</div>
                      <div class="meta-text">{{ getTextValue(getField(exercise, 'listeningText'), '无听力原文信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">判断句</div>
                      <div class="meta-text">
                        {{ getTextValue(getField(exercise, 'statement'), '无判断句信息') }}
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">答案：{{ formatBoolean(exercise.metadata.correctAnswer) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'READ_SENTENCE_COMPREHENSION_CHOICE')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block" v-if="getField(exercise, 'passage')">
                      <div class="meta-title">阅读材料</div>
                      <div class="meta-text">{{ getField(exercise, 'passage') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">问题</div>
                      <div class="meta-text">
                        {{ getTextValue(getField(exercise, 'question'), '无问题信息') }}
                      </div>
                    </div>
                    <div class="meta-block" v-if="getOptions(exercise).length">
                      <div class="meta-title">选项</div>
                      <div class="options-list">
                        <div v-for="(option, idx) in getOptions(exercise)" :key="idx" class="option-item">
                          <span class="option-key">{{ getOptionLabel(option, idx) }}.</span>
                          <span class="option-text">{{ getOptionText(option) }}</span>
                          <span v-if="option.pinyin" class="option-pinyin">{{ option.pinyin }}</span>
                          <span v-if="isCorrectOptionByAnswer(getCorrectAnswer(exercise.metadata), option, idx)" class="correct-mark">✓</span>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确答案：{{ formatCorrectAnswer(exercise.metadata) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'READ_WORD_GAP_FILL')">
                    <div class="meta-block">
                      <div class="meta-title">题干</div>
                      <div class="meta-text">{{ getTextValue(getField(exercise, 'text'), '无题干信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block" v-if="getField(exercise, 'blanks') && getField(exercise, 'blanks').length">
                      <div class="meta-title">填空选项</div>
                      <div class="meta-list">
                        <div v-for="(blank, idx) in getField(exercise, 'blanks')" :key="idx" class="meta-item-card">
                          <div class="meta-subtitle">空{{ getTextValue(blank.blankIndex, idx) }}</div>
                          <div class="options-list">
                            <div v-for="opt in getBlankOptions(blank)" :key="opt.key" class="option-item">
                              <span class="option-key">{{ opt.key }}.</span>
                              <span class="option-text">{{ getTextValue(opt.text, '无选项信息') }}</span>
                              <span v-if="opt.pinyin" class="option-pinyin">{{ opt.pinyin }}</span>
                              <span v-if="getBlankCorrectAnswer(blank, exercise.metadata?.content || exercise.metadata, idx) === opt.key" class="correct-mark">✓</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'READ_SENTENCE_ORDER')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block" v-if="getField(exercise, 'sentences') && getField(exercise, 'sentences').length">
                      <div class="meta-title">句子片段</div>
                      <div class="meta-list">
                        <div v-for="(sentence, idx) in getField(exercise, 'sentences')" :key="idx" class="meta-item-card">
                          {{ sentence.label }}. {{ sentence.text || sentence.sentence || sentence.content }}
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确顺序：{{ formatCorrectAnswer(exercise.metadata) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'READ_WORD_ORDER')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block" v-if="getField(exercise, 'words') && getField(exercise, 'words').length">
                      <div class="meta-title">词语</div>
                      <div class="meta-list">
                        <div v-for="(word, idx) in getField(exercise, 'words')" :key="idx" class="meta-item-card">
                          {{ word.label }}. {{ word.text || word.word || word.value }}
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确顺序：{{ formatCorrectAnswer(exercise.metadata) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'READ_SENTENCE_TF')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">阅读材料</div>
                      <div class="meta-text">{{ getTextValue(getField(exercise, 'passage'), '无阅读材料信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">判断句</div>
                      <div class="meta-text">{{ getTextValue(getField(exercise, 'statement'), '无判断句信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">答案：{{ formatBoolean(exercise.metadata.correctAnswer) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'READ_SENTENCE_TRANSLATION')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">中文</div>
                      <div class="meta-text">{{ getTextValue(getField(exercise, 'sentenceCn'), '无中文信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">英文</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.correctAnswer, '无英文信息') }}</div>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'SPEAK_FOLLOW')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">句子</div>
                      <div class="meta-text">
                        {{ getTextValue(getField(exercise, 'sentence'), '无句子信息') }}
                        <span v-if="getField(exercise, 'pinyin')" class="pinyin-text">{{ getField(exercise, 'pinyin') }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">示例音频：{{ getTextValue(getField(exercise, 'sampleAudioUrl'), '无音频信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isType(exercise, 'TRANSLATE_WORD_ORDER')">
                    <div class="meta-block" v-if="getField(exercise, 'prompt')">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ getField(exercise, 'prompt') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">原句</div>
                      <div class="meta-text">{{ getTextValue(getField(exercise, 'originalSentence'), '无原句信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="getField(exercise, 'words') && getField(exercise, 'words').length">
                      <div class="meta-title">词语</div>
                      <div class="meta-list">
                        <div v-for="(word, idx) in getField(exercise, 'words')" :key="idx" class="meta-item-card">
                          {{ word.label }}. {{ word.text || word.word || word.value }}
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确顺序：{{ formatCorrectAnswer(exercise.metadata) }}</span>
                    </div>
                  </template>

                  <pre class="json-view" v-else>{{ JSON.stringify(exercise.metadata, null, 2) }}</pre>
                </div>
              </div>

              <div v-if="getExerciseMedia(exercise.id).length > 0" class="media-section">
                <div class="info-label">关联媒体</div>
                <div class="media-list">
                  <div v-for="media in getExerciseMedia(exercise.id)" :key="media.id" class="media-item">
                    <span class="media-icon">{{ media.file_type === 'audio' ? '🔊' : '🖼️' }}</span>
                    <span class="media-name">{{ getMediaName(media) }}</span>
                    <span class="media-role">{{ getMediaRoleName(media.usage_role) }}</span>
                    <span class="media-type">{{ media.mime_type }}</span>
                    <img v-if="media.file_type === 'image' && media.file_url" :src="media.file_url" class="media-preview" />
                    <audio v-else-if="media.file_type === 'audio' && media.file_url" :src="media.file_url" controls class="media-audio"></audio>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <div class="empty-icon">🤖</div>
          <h3>暂无AI生成的题目</h3>
          <p>{{ searchQuery ? '没有找到匹配的题目' : '暂无题目' }}</p>
        </div>
      </div>

      <div class="pagination" v-if="totalPages > 1">
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
import request from '../../utils/request'

export default {
  name: 'ScenarioSystemExercises',
  components: {
    Header
  },
  setup() {
    const searchQuery = ref('')
    
    // 筛选条件
    const filters = ref({
      lessonId: '',
      exerciseType: '',
      difficulty: ''
    })
    
    // 数据
    const slExercises = ref([])
    const currentPage = ref(1)
    const pageSize = ref(6)
    const total = ref(0)
    
    // 获取题目数据
    const fetchExercises = async () => {
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
        if (searchQuery.value) {
          params.search = searchQuery.value
        }
        const res = await request.get('/v1/questions', { params })
        if (res.data) {
          slExercises.value = res.data.items || []
          total.value = res.data.total || 0
        }
      } catch (error) {
        console.error('获取题目失败:', error)
      }
    }

    onMounted(() => {
      fetchExercises()
    })

    watch(
      [() => filters.value.exerciseType, () => filters.value.difficulty, () => searchQuery.value],
      () => {
        currentPage.value = 1
        fetchExercises()
      }
    )

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
      const m = exercise?.metadata || {}
      const c = m?.content || {}
      const prompt = c.prompt ?? m.prompt ?? c.question ?? m.question
      if (prompt) return prompt
      return exercise.prompt || '无题干信息'
    }

    const getField = (exercise, key) => {
      const m = exercise?.metadata || {}
      const c = m?.content || {}
      const snake = key.replace(/([A-Z])/g, '_$1').toLowerCase()
      return c[key] ?? c[snake] ?? m[key] ?? m[snake]
    }

    const getOptions = (exercise) => {
      const m = exercise?.metadata || {}
      const c = m?.content || {}
      return c.options ?? m.options ?? []
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
    
    const getExerciseTypeKey = (exercise) => {
      return exercise?.exercise_type?.name || ''
    }

    const isType = (exercise, typeKey) => {
      return getExerciseTypeKey(exercise) === typeKey
    }

    const getContent = (exercise) => {
      const metadata = exercise?.metadata || {}
      return metadata.content || metadata || {}
    }

    const getTextValue = (value, fallback) => {
      if (value === undefined || value === null || value === '') return fallback
      return value
    }

    const formatBoolean = (value) => {
      if (value === true) return '正确'
      if (value === false) return '错误'
      return '无判断信息'
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }

    const getOptionLabel = (option, index) => {
      return option?.label || option?.key || String.fromCharCode(65 + index)
    }

    const getOptionText = (option) => {
      if (option && typeof option === 'object') {
        return option.text || option.keyword || option.word || option.value || '无选项信息'
      }
      return option || '无选项信息'
    }

    const getCorrectAnswer = (metadata) => {
      return metadata?.correctAnswer ?? metadata?.content?.correctAnswer ?? metadata?.correct_answer
    }

    const isCorrectOptionByAnswer = (answer, option, idx) => {
      const label = getOptionLabel(option, idx)
      if (answer === undefined || answer === null) return false
      if (label === answer) return true
      return getOptionText(option) === answer
    }

    const getBlankOptions = (blank) => {
      const options = blank?.options || {}
      return Object.keys(options).map(key => ({
        key,
        text: options[key]?.text,
        pinyin: options[key]?.pinyin
      }))
    }

    const getBlankCorrectAnswer = (blank, metadata, index) => {
      if (blank?.correctAnswer) return blank.correctAnswer
      const key = blank?.blankIndex ?? index
      if (metadata?.correctAnswer && metadata.correctAnswer[key] !== undefined) {
        return metadata.correctAnswer[key]
      }
      if (metadata?.correctAnswer && metadata.correctAnswer[String(key)] !== undefined) {
        return metadata.correctAnswer[String(key)]
      }
      return ''
    }

    const getShuffledPieces = (map) => {
      if (!map) return []
      return Object.keys(map).map(label => ({
        label,
        text: map[label]?.text,
        pinyin: map[label]?.pinyin
      }))
    }

    const formatOrder = (order) => {
      if (Array.isArray(order)) return order.join(' ')
      return getTextValue(order, '无答案信息')
    }

    const formatCorrectAnswer = (metadata) => {
      const answer = metadata?.correctAnswer ?? metadata?.correct_answer ?? metadata?.correct_label
      if (Array.isArray(answer)) return answer.join(' ')
      if (answer && typeof answer === 'object') {
        return Object.keys(answer).map(key => `${key}:${answer[key]}`).join(' ')
      }
      if (typeof answer === 'boolean') return formatBoolean(answer)
      return getTextValue(answer, '无答案信息')
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
      generatedLessons,
      slExerciseTypes,
      filteredExercises,
      currentPage,
      totalPages,
      total,
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
      getExerciseTypeKey,
      isType,
      getContent,
      getField,
      getOptions,
      getTextValue,
      formatBoolean,
      getOptionLabel,
      getOptionText,
      getCorrectAnswer,
      isCorrectOptionByAnswer,
      getBlankOptions,
      getBlankCorrectAnswer,
      getShuffledPieces,
      formatOrder,
      formatCorrectAnswer,
      getDifficultyText,
      formatDate
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
  background: linear-gradient(135deg, #f3e5f5 0%, #ede7f6 100%);
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

.difficulty-badge {
  font-size: 0.85rem;
  font-weight: 600;
}

.card-body {
  padding: 20px;
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

.metadata-section {
  background: #f9f9f9;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.info-label {
  font-weight: 600;
  color: #6a1b9a;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

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
