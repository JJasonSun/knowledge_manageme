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
                <span class="status-badge" :class="getQualityClass(exercise.quality_status)">
                  {{ getQualityText(exercise.quality_status) }}
                </span>
              </div>
            </div>

            <div class="card-body">
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
                  <span class="meta-label">创建时间：</span>
                  <span class="meta-value">{{ formatDate(exercise.created_at) }}</span>
                </div>
              </div>

              <div class="metadata-section" v-if="exercise.metadata">
                <div class="info-label">📋 题目详情：</div>
                <div class="metadata-content">
                  <template v-if="isListenQa(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">听力原文</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.listening_text, '无听力原文信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">问题</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.question, '无问题信息') }}
                        <span v-if="exercise.metadata.question_pinyin" class="pinyin-text">{{ exercise.metadata.question_pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.options && exercise.metadata.options.length">
                      <div class="meta-title">选项</div>
                      <div class="options-list">
                        <div v-for="(option, idx) in exercise.metadata.options" :key="idx" class="option-item">
                          <span class="option-key">{{ getOptionLabel(option, idx) }}.</span>
                          <span class="option-text">{{ getOptionText(option) }}</span>
                          <span v-if="option.pinyin" class="option-pinyin">{{ option.pinyin }}</span>
                          <span v-if="exercise.metadata.correct_label && getOptionLabel(option, idx) === exercise.metadata.correct_label" class="correct-mark">✓</span>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确答案：{{ getTextValue(exercise.metadata.correct_label, '无答案信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isListenSentenceTf(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">听力原文</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.listening_text, '无听力原文信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">判断句</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.statement, '无判断句信息') }}
                        <span v-if="exercise.metadata.statement_pinyin" class="pinyin-text">{{ exercise.metadata.statement_pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">答案：{{ formatBoolean(exercise.metadata.correct_answer) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isListenImageTrueFalse(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">听力原文</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.listening_text, '无听力原文信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">答案：{{ formatBoolean(exercise.metadata.correct_answer) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isListenImageMc(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">听力原文</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.listening_text, '无听力原文信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.options && exercise.metadata.options.length">
                      <div class="meta-title">选项</div>
                      <div class="options-list">
                        <div v-for="(option, idx) in exercise.metadata.options" :key="idx" class="option-item">
                          <span class="option-key">{{ getOptionLabel(option, idx) }}.</span>
                          <span class="option-text">{{ getTextValue(option.keyword, '无关键词信息') }}</span>
                          <span class="option-pinyin">{{ getTextValue(option.image_asset_id, '无图片资源信息') }}</span>
                          <span v-if="exercise.metadata.correct_answer && getOptionLabel(option, idx) === exercise.metadata.correct_answer" class="correct-mark">✓</span>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确答案：{{ getTextValue(exercise.metadata.correct_answer, '无答案信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isListenImageMatch(exercise)">
                    <div class="meta-block" v-if="exercise.metadata.listening_text">
                      <div class="meta-title">听力原文</div>
                      <div class="meta-text">{{ exercise.metadata.listening_text }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.keywords && exercise.metadata.keywords.length">
                      <div class="meta-title">关键词</div>
                      <div class="meta-list">
                        <div v-for="(keyword, idx) in exercise.metadata.keywords" :key="idx" class="meta-item-card">{{ keyword }}</div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确图片序号：{{ getTextValue(getCorrectImageIndex(exercise.metadata), '无答案信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadImageMatch(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">词语</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.word, '无词语信息') }}
                        <span v-if="exercise.metadata.pinyin" class="pinyin-text">{{ exercise.metadata.pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确图片序号：{{ getTextValue(getCorrectImageIndex(exercise.metadata), '无答案信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadImageTrueFalse(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">词语</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.word, '无词语信息') }}
                        <span v-if="exercise.metadata.pinyin" class="pinyin-text">{{ exercise.metadata.pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">答案：{{ formatBoolean(exercise.metadata.correct_answer) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadDialogueMatch(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">对话</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.utterance, '无问题信息') }}
                        <span v-if="exercise.metadata.utter_pinyin" class="pinyin-text">{{ exercise.metadata.utter_pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">回答</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.reply, '无回答信息') }}
                        <span v-if="exercise.metadata.reply_pinyin" class="pinyin-text">{{ exercise.metadata.reply_pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">配对序号：{{ getTextValue(exercise.metadata.pair_index, '无配对信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadParagraphComprehension(exercise)">
                    <div class="meta-block" v-if="exercise.metadata.passage">
                      <div class="meta-title">阅读材料</div>
                      <div class="meta-text">{{ exercise.metadata.passage }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">问题</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.question, '无问题信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.options && exercise.metadata.options.length">
                      <div class="meta-title">选项</div>
                      <div class="options-list">
                        <div v-for="(option, idx) in exercise.metadata.options" :key="idx" class="option-item">
                          <span class="option-key">{{ getOptionLabel(option, idx) }}.</span>
                          <span class="option-text">{{ getOptionText(option) }}</span>
                          <span v-if="exercise.metadata.correct_label && getOptionLabel(option, idx) === exercise.metadata.correct_label" class="correct-mark">✓</span>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确答案：{{ getTextValue(exercise.metadata.correct_label, '无答案信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadSentenceComprehensionChoice(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">阅读材料</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.passage, '无阅读材料信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">问题</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.question, '无问题信息') }}
                        <span v-if="exercise.metadata.question_pinyin" class="pinyin-text">{{ exercise.metadata.question_pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.options && exercise.metadata.options.length">
                      <div class="meta-title">选项</div>
                      <div class="options-list">
                        <div v-for="(option, idx) in exercise.metadata.options" :key="idx" class="option-item">
                          <span class="option-key">{{ getOptionLabel(option, idx) }}.</span>
                          <span class="option-text">{{ getOptionText(option) }}</span>
                          <span v-if="option.pinyin" class="option-pinyin">{{ option.pinyin }}</span>
                          <span v-if="exercise.metadata.correct_label && getOptionLabel(option, idx) === exercise.metadata.correct_label" class="correct-mark">✓</span>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确答案：{{ getTextValue(exercise.metadata.correct_label, '无答案信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadSentenceTf(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">阅读材料</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.passage, '无阅读材料信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">判断句</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.statement, '无判断句信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">答案：{{ formatBoolean(exercise.metadata.correct_answer) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadSentenceTranslation(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">中文</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.sentence_cn, '无中文信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">英文</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.sentence_en, '无英文信息') }}</div>
                    </div>
                  </template>

                  <template v-else-if="isReadWordGapFill(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">题干</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.content?.text, '无题干信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.content?.prompt">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ exercise.metadata.content.prompt }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.content?.blanks && exercise.metadata.content.blanks.length">
                      <div class="meta-title">填空选项</div>
                      <div class="meta-list">
                        <div v-for="(blank, idx) in exercise.metadata.content.blanks" :key="idx" class="meta-item-card">
                          <div class="meta-subtitle">空{{ getTextValue(blank.blankIndex, idx) }}</div>
                          <div class="options-list">
                            <div v-for="opt in getBlankOptions(blank)" :key="opt.key" class="option-item">
                              <span class="option-key">{{ opt.key }}.</span>
                              <span class="option-text">{{ getTextValue(opt.text, '无选项信息') }}</span>
                              <span v-if="opt.pinyin" class="option-pinyin">{{ opt.pinyin }}</span>
                              <span v-if="getBlankCorrectAnswer(blank, exercise.metadata.content, idx) === opt.key" class="correct-mark">✓</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>

                  <template v-else-if="isReadSentenceOrder(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">段落</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.paragraph, '无段落信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.pieces_original && exercise.metadata.pieces_original.length">
                      <div class="meta-title">原始句子</div>
                      <div class="meta-list">
                        <div v-for="piece in exercise.metadata.pieces_original" :key="piece.id" class="meta-item-card">
                          <div>{{ piece.text }}</div>
                          <div v-if="piece.pinyin" class="pinyin-text">{{ piece.pinyin }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.pieces_shuffled_label_map">
                      <div class="meta-title">打乱句子</div>
                      <div class="meta-list">
                        <div v-for="piece in getShuffledPieces(exercise.metadata.pieces_shuffled_label_map)" :key="piece.label" class="meta-item-card">
                          <div>{{ piece.label }}. {{ piece.text }}</div>
                          <div v-if="piece.pinyin" class="pinyin-text">{{ piece.pinyin }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确顺序：{{ formatOrder(exercise.metadata.answer_order) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isReadWordOrder(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">目标句子</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.sentence, '无句子信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.pieces_original && exercise.metadata.pieces_original.length">
                      <div class="meta-title">原始词语</div>
                      <div class="meta-list">
                        <div v-for="piece in exercise.metadata.pieces_original" :key="piece.id" class="meta-item-card">
                          <div>{{ piece.text }}</div>
                          <div v-if="piece.pinyin" class="pinyin-text">{{ piece.pinyin }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.pieces_shuffled_label_map">
                      <div class="meta-title">打乱词语</div>
                      <div class="meta-list">
                        <div v-for="piece in getShuffledPieces(exercise.metadata.pieces_shuffled_label_map)" :key="piece.label" class="meta-item-card">
                          <div>{{ piece.label }}. {{ piece.text }}</div>
                          <div v-if="piece.pinyin" class="pinyin-text">{{ piece.pinyin }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确顺序：{{ formatOrder(exercise.metadata.answer_order) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isTranslateWordOrder(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">原句</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.content?.originalSentence, '无原句信息') }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.content?.prompt">
                      <div class="meta-title">提示</div>
                      <div class="meta-text">{{ exercise.metadata.content.prompt }}</div>
                    </div>
                    <div class="meta-block" v-if="exercise.metadata.content?.words && exercise.metadata.content.words.length">
                      <div class="meta-title">词语</div>
                      <div class="meta-list">
                        <div v-for="(word, idx) in exercise.metadata.content.words" :key="idx" class="meta-item-card">
                          {{ word.label }}. {{ word.word }}
                        </div>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">正确顺序：{{ formatOrder(exercise.metadata.correctAnswer) }}</span>
                    </div>
                  </template>

                  <template v-else-if="isSpeakFollow(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">句子</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.sentence, '无句子信息') }}
                        <span v-if="exercise.metadata.pinyin" class="pinyin-text">{{ exercise.metadata.pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">音频资源：{{ getTextValue(exercise.metadata.audio_asset_id, '无音频资源信息') }}</span>
                    </div>
                  </template>

                  <template v-else-if="isStrokeOrderWriting(exercise)">
                    <div class="meta-block">
                      <div class="meta-title">汉字</div>
                      <div class="meta-text">
                        {{ getTextValue(exercise.metadata.character, '无汉字信息') }}
                        <span v-if="exercise.metadata.pinyin" class="pinyin-text">{{ exercise.metadata.pinyin }}</span>
                      </div>
                    </div>
                    <div class="meta-block">
                      <div class="meta-title">释义</div>
                      <div class="meta-text">{{ getTextValue(exercise.metadata.definition, '无释义信息') }}</div>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">笔顺动图：{{ getTextValue(exercise.metadata.animation, '无动图信息') }}</span>
                    </div>
                    <div class="meta-block">
                      <span class="answer-badge">笔顺图片：{{ getTextValue(exercise.metadata.stroke_image_url, '无图片信息') }}</span>
                    </div>
                  </template>

                  <pre class="json-view" v-else>{{ JSON.stringify(exercise.metadata, null, 2) }}</pre>
                </div>
              </div>

              <div v-if="getExerciseMedia(exercise.id).length > 0" class="media-section">
                <div class="info-label">🎬 关联媒体：</div>
                <div class="media-list">
                  <div v-for="media in getExerciseMedia(exercise.id)" :key="media.id" class="media-item">
                    <span class="media-icon">{{ media.file_type === 'audio' ? '🔊' : '🖼️' }}</span>
                    <span class="media-name">{{ getMediaName(media) }}</span>
                    <span class="media-role">{{ getMediaRoleName(media.usage_role) }}</span>
                    <span class="media-type">{{ media.mime_type }}</span>
                  </div>
                </div>
              </div>
            </div>


          </div>
        </div>
        
        <div v-else class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>暂无题目数据</h3>
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
  name: 'ContentSystemExercises',
  components: {
    Header
  },
  setup() {
    const searchQuery = ref('')
    
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

    // 获取题目数据
    const fetchExercises = async () => {
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
      if (exercise.metadata && exercise.metadata.question) return exercise.metadata.question
      if (exercise.metadata && exercise.metadata.prompt) return exercise.metadata.prompt
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
    
    const getExerciseTypeKey = (exercise) => {
      return exercise?.exercise_type?.name || ''
    }

    const isListenQa = (exercise) => {
      return ['LISTEN_DIALOGUE_QA', 'LISTEN_PARAGRAPH_QA', 'LISTEN_SENTENCE_QA'].includes(getExerciseTypeKey(exercise))
    }

    const isListenSentenceTf = (exercise) => getExerciseTypeKey(exercise) === 'LISTEN_SENTENCE_TF'
    const isListenImageTrueFalse = (exercise) => getExerciseTypeKey(exercise) === 'LISTEN_IMAGE_TRUE_FALSE'
    const isListenImageMc = (exercise) => getExerciseTypeKey(exercise) === 'LISTEN_IMAGE_MC'
    const isListenImageMatch = (exercise) => getExerciseTypeKey(exercise) === 'LISTEN_IMAGE_MATCH'
    const isReadImageMatch = (exercise) => getExerciseTypeKey(exercise) === 'READ_IMAGE_MATCH'
    const isReadImageTrueFalse = (exercise) => getExerciseTypeKey(exercise) === 'READ_IMAGE_TRUE_FALSE'
    const isReadDialogueMatch = (exercise) => getExerciseTypeKey(exercise) === 'READ_DIALOGUE_MATCH'
    const isReadParagraphComprehension = (exercise) => getExerciseTypeKey(exercise) === 'READ_PARAGRAPH_COMPREHENSION'
    const isReadSentenceComprehensionChoice = (exercise) => getExerciseTypeKey(exercise) === 'READ_SENTENCE_COMPREHENSION_CHOICE'
    const isReadSentenceTf = (exercise) => getExerciseTypeKey(exercise) === 'READ_SENTENCE_TF'
    const isReadSentenceTranslation = (exercise) => getExerciseTypeKey(exercise) === 'READ_SENTENCE_TRANSLATION'
    const isReadWordGapFill = (exercise) => getExerciseTypeKey(exercise) === 'READ_WORD_GAP_FILL'
    const isReadSentenceOrder = (exercise) => getExerciseTypeKey(exercise) === 'READ_SENTENCE_ORDER'
    const isReadWordOrder = (exercise) => getExerciseTypeKey(exercise) === 'READ_WORD_ORDER'
    const isTranslateWordOrder = (exercise) => getExerciseTypeKey(exercise) === 'TRANSLATE_WORD_ORDER'
    const isSpeakFollow = (exercise) => getExerciseTypeKey(exercise) === 'SPEAK_FOLLOW'
    const isStrokeOrderWriting = (exercise) => getExerciseTypeKey(exercise) === 'STROKE_ORDER_WRITING'

    const getTextValue = (value, fallback) => {
      if (value === undefined || value === null || value === '') return fallback
      return value
    }

    const formatBoolean = (value) => {
      if (value === true) return '正确'
      if (value === false) return '错误'
      return '无判断信息'
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

    const getCorrectImageIndex = (metadata) => {
      if (!metadata) return ''
      return metadata.correct_image_index ?? metadata.correctImageIndex ?? metadata.correct_answer ?? metadata.correctAnswer ?? ''
    }

    const getBlankOptions = (blank) => {
      const options = blank?.options || {}
      return Object.keys(options).map(key => ({
        key,
        text: options[key]?.text,
        pinyin: options[key]?.pinyin
      }))
    }

    const getBlankCorrectAnswer = (blank, content, index) => {
      if (blank?.correctAnswer) return blank.correctAnswer
      const key = blank?.blankIndex ?? index
      if (content?.correctAnswer && content.correctAnswer[key] !== undefined) {
        return content.correctAnswer[key]
      }
      if (content?.correctAnswer && content.correctAnswer[String(key)] !== undefined) {
        return content.correctAnswer[String(key)]
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

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }

    return {
      searchQuery,
      filters,
      skillCategories,
      exerciseTypes,
      filteredExerciseTypes,
      filteredExercises,
      currentPage,
      totalPages,
      total,
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
      getExerciseTypeKey,
      isListenQa,
      isListenSentenceTf,
      isListenImageTrueFalse,
      isListenImageMc,
      isListenImageMatch,
      isReadImageMatch,
      isReadImageTrueFalse,
      isReadDialogueMatch,
      isReadParagraphComprehension,
      isReadSentenceComprehensionChoice,
      isReadSentenceTf,
      isReadSentenceTranslation,
      isReadWordGapFill,
      isReadSentenceOrder,
      isReadWordOrder,
      isTranslateWordOrder,
      isSpeakFollow,
      isStrokeOrderWriting,
      getTextValue,
      formatBoolean,
      getOptionLabel,
      getOptionText,
      getCorrectImageIndex,
      getBlankOptions,
      getBlankCorrectAnswer,
      getShuffledPieces,
      formatOrder,
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

.word-sub {
  color: #2e7d32;
  font-size: 0.9rem;
  margin-top: 6px;
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
