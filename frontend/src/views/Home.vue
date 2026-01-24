<template>
  <div>
    <Header />
    <div class="home-container">
      <!-- 大搜索框区域 -->
      <div class="search-hero">
        <h1 class="search-title">中文教育资源查询</h1>
        <p class="search-subtitle">搜索汉字、词语、成语、题目、音视频资源</p>
        
        <div class="search-wrapper">
          <!-- 第一级：选择模块 -->
          <select v-model="selectedModule" class="search-type-select" @change="handleModuleChange">
            <option value="">请先选择模块</option>
            <option value="hanzi">基础知识</option>
            <option value="exam">题目模块</option>
            <option value="media">音视频模块</option>
          </select>
          
          <!-- 第二级：选择具体类型 -->
          <select v-model="selectedType" class="search-subtype-select" :disabled="!selectedModule" @change="handleTypeChange">
            <option value="">请先选择类型</option>
            <!-- 基础知识选项 -->
            <option v-if="selectedModule === 'hanzi'" value="zi">汉字</option>
            <option v-if="selectedModule === 'hanzi'" value="ciyu">词语</option>
            <option v-if="selectedModule === 'hanzi'" value="chengyu">成语</option>
            <!-- 题目模块选项 -->
            <option v-if="selectedModule === 'exam'" value="content-system">📚 Content System</option>
            <option v-if="selectedModule === 'exam'" value="scenario-system">🤖 Scenario System</option>
            <!-- 音视频模块选项 -->
            <option v-if="selectedModule === 'media'" value="audio">音频</option>
            <option v-if="selectedModule === 'media'" value="video">视频</option>
          </select>
          
          <input 
            v-model="searchQuery" 
            type="text" 
            class="search-input-large"
            :placeholder="getSearchPlaceholder()"
            :disabled="!selectedModule || !selectedType"
            @keyup.enter="handleSearch"
          >
          <button class="search-btn" @click="handleSearch" :disabled="!canSearch">
            搜索
          </button>
        </div>
      </div>

      <!-- 三大模块展示 -->
      <div class="modules-section">
        <!-- 基础知识 -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon">📝</div>
            <h3 class="module-title">基础知识</h3>
          </div>
          <div class="module-items">
            <div class="module-group-items">
              <router-link to="/hanzi/zi" class="module-item small">汉字管理</router-link>
              <router-link to="/hanzi/ciyu" class="module-item small">词语管理</router-link>
              <router-link to="/hanzi/chengyu" class="module-item small">成语管理</router-link>
            </div>
          </div>
        </div>

        <!-- 题目模块 -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon">📋</div>
            <h3 class="module-title">题目模块</h3>
          </div>
          <div class="module-items">
            <div class="module-group-items">
              <router-link to="/exam/content-system" class="module-item small">📚 Content System</router-link>
              <router-link to="/exam/scenario-system" class="module-item small">🤖 Scenario System</router-link>
            </div>
          </div>
        </div>

        <!-- 音视频模块 -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon">🎬</div>
            <h3 class="module-title">音视频模块</h3>
          </div>
          <div class="module-items">
            <div class="module-group-items">
              <router-link to="/media/audio" class="module-item small">音频资源</router-link>
              <router-link to="/media/video" class="module-item small">视频资源</router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- 搜索结果弹窗 -->
      <div v-if="showResultsModal" class="results-modal" @click.self="closeResultsModal">
        <div class="results-modal-content">
          <div class="results-modal-header">
            <h3>
              搜索结果
              <span class="result-count">
                （{{ getSearchTypeText() }}，共 {{ totalResults }} 条）
              </span>
            </h3>
            <button class="close-btn" @click="closeResultsModal">×</button>
          </div>

          <div class="results-modal-body">
            <div v-if="loading" class="loading">搜索中...</div>

            <div v-else-if="searchResults.length === 0" class="no-results">
              未找到相关结果，试试其他关键词？
            </div>

            <div v-else class="results-list">
              <div 
                v-for="item in searchResults" 
                :key="item.type + '-' + item.id" 
                class="result-card"
              >
                <div class="result-header">
                  <span class="result-word">{{ item.word }}</span>
                  <span class="result-type" :class="'type-' + item.type">
                    {{ item.type === 'chengyu' ? '成语' : '词语' }}
                  </span>
                  <span v-if="canModifyItem(item)" class="result-mine">我的</span>
                  <span v-else-if="item.created_by === 'admin'" class="result-admin">管理员</span>
                  <span v-else-if="!item.created_by || item.created_by === 'system'" class="result-system">系统</span>
                </div>
                
                <!-- 拼音和注音 -->
                <div class="result-phonetic">
                  <span v-if="item.pinyin" class="pinyin">拼音：{{ item.pinyin }}</span>
                  <span v-if="item.zhuyin" class="zhuyin">注音：{{ item.zhuyin }}</span>
                </div>
                
                <!-- 成语特有字段 -->
                <div v-if="item.type === 'chengyu'" class="result-details">
                  <div v-if="item.emotion" class="detail-item">
                    <span class="label">情感色彩：</span>{{ item.emotion }}
                  </div>
                  <div v-if="item.source" class="detail-item">
                    <span class="label">来源：</span>{{ item.source }}
                  </div>
                  <div v-if="item.usage" class="detail-item">
                    <span class="label">用法：</span>{{ item.usage }}
                  </div>
                  <div v-if="item.translation" class="detail-item">
                    <span class="label">翻译：</span>{{ item.translation }}
                  </div>
                </div>
                
                <!-- 词语特有字段 -->
                <div v-if="item.type === 'ciyu'" class="result-details">
                  <div v-if="item.part_of_speech" class="detail-item">
                    <span class="label">词性：</span>{{ item.part_of_speech }}
                  </div>
                  <div v-if="item.is_common !== null" class="detail-item">
                    <span class="label">常用程度：</span>{{ item.is_common ? '常用词' : '非常用词' }}
                  </div>
                </div>

                <!-- 题目特有字段 -->
                <div v-if="item.type === 'content-system' || item.type === 'scenario-system'" class="result-details">
                  <div class="detail-item">
                    <span class="label">难度：</span>
                    <span v-for="n in item.difficulty" :key="n" style="color: #ff9800;">★</span>
                  </div>
                  <div v-if="item.status !== undefined" class="detail-item">
                    <span class="label">状态：</span>{{ item.status === 1 ? '已发布' : '草稿' }}
                  </div>
                  <!-- 选项展示 -->
                  <div v-if="item.options" class="detail-item" style="margin-top: 8px;">
                    <span class="label">选项：</span>
                    <div style="margin-left: 10px; font-size: 0.9em; color: #666;">
                      <div v-for="opt in item.options" :key="opt.key || opt">
                        {{ typeof opt === 'string' ? opt : `${opt.key}. ${opt.text}` }}
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 定义/解释 -->
                <div class="result-definition">
                  <span class="label">{{ item.type === 'chengyu' ? '解释：' : (item.type === 'zi' ? '释义：' : '详情：') }}</span>
                  {{ item.definition }}
                </div>
                
                <!-- 例句 -->
                <div v-if="item.example" class="result-example">
                  <span class="label">例句：</span>{{ item.example }}
                </div>
                
                <!-- 同义词和反义词 -->
                <div v-if="item.synonyms && item.synonyms.length > 0" class="result-relations">
                  <span class="label">同义词：</span>
                  <span class="relation-tags">
                    <span 
                      v-for="synonym in item.synonyms" 
                      :key="synonym" 
                      class="relation-tag synonym"
                      @click="quickSearch(synonym)"
                    >
                      {{ synonym }}
                    </span>
                  </span>
                </div>
                <div v-if="item.antonyms && item.antonyms.length > 0" class="result-relations">
                  <span class="label">反义词：</span>
                  <span class="relation-tags">
                    <span 
                      v-for="antonym in item.antonyms" 
                      :key="antonym" 
                      class="relation-tag antonym"
                      @click="quickSearch(antonym)"
                    >
                      {{ antonym }}
                    </span>
                  </span>
                </div>
                
                <!-- 操作按钮 -->
                <div class="result-actions" v-if="canModifyItem(item)">
                  <button class="btn-small btn-header" @click="editItem(item)">编辑</button>
                  <button class="btn-small btn-header btn-danger-header" @click="deleteItem(item)">删除</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import Header from '../components/Header.vue'
import request from '../utils/request'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { contentSystemMock, scenarioSystemMock } from '../mock/exerciseData'

export default {
  name: 'Home',
  components: { Header },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const searchQuery = ref('')
    const selectedModule = ref('')
    const selectedType = ref('')
    const searchResults = ref([])
    const loading = ref(false)
    const hasSearched = ref(false)
    const totalResults = ref(0)
    const showResultsModal = ref(false)

    // 模块变更处理
    const handleModuleChange = () => {
      selectedType.value = ''
    }

    // 类型变更处理
    const handleTypeChange = () => {
      // 可在此处添加类型变更后的额外处理
    }

    // 获取搜索提示文本
    const getSearchPlaceholder = () => {
      if (!selectedModule.value) return '请先选择模块和类型'
      if (!selectedType.value) return '请选择具体类型'
      
      const placeholders = {
        'zi': '输入汉字进行搜索...',
        'ciyu': '输入词语进行搜索...',
        'chengyu': '输入成语进行搜索...',
        'content-system': '输入关键词搜索Content System题目...',
        'scenario-system': '输入关键词搜索Scenario System题目...',
        'audio': '输入关键词搜索音频资源...',
        'video': '输入关键词搜索视频资源...'
      }
      return placeholders[selectedType.value] || '输入关键词搜索...'
    }

    // 判断是否可以搜索
    const canSearch = computed(() => {
      return selectedModule.value && selectedType.value && searchQuery.value.trim()
    })

    const handleSearch = async () => {
      if (!selectedType.value || !searchQuery.value.trim()) return
      
      loading.value = true
      hasSearched.value = true
      searchResults.value = []
      showResultsModal.value = true
      
      try {
        const results = []
        
        // 根据选中的类型查询对应的API
        if (selectedType.value === 'chengyu') {
          try {
            const chengyuRes = await request.get('/v1/chengyu', { 
              params: { search: searchQuery.value, size: 50 } 
            })
            if (chengyuRes.data.items) {
              chengyuRes.data.items.forEach(item => {
                results.push({
                  id: item.id,
                  type: 'chengyu',
                  word: item.chengyu,
                  pinyin: item.pinyin,
                  zhuyin: item.zhuyin,
                  emotion: item.emotion,
                  definition: item.explanation,
                  source: item.source,
                  usage: item.usage,
                  example: item.example,
                  synonyms: item.synonyms,
                  antonyms: item.antonyms,
                  translation: item.translation,
                  created_by: item.created_by
                })
              })
            }
          } catch (error) {
            console.error('搜索成语失败:', error)
          }
        } else if (selectedType.value === 'ciyu') {
          try {
            const ciyuRes = await request.get('/v1/ciyu', { 
              params: { search: searchQuery.value, size: 50 } 
            })
            if (ciyuRes.data.items) {
              ciyuRes.data.items.forEach(item => {
                results.push({
                  id: item.id,
                  type: 'ciyu',
                  word: item.word,
                  pinyin: item.pinyin,
                  zhuyin: item.zhuyin,
                  part_of_speech: item.part_of_speech,
                  is_common: item.is_common,
                  definition: item.definition,
                  synonyms: item.synonyms,
                  antonyms: item.antonyms,
                  created_by: item.created_by
                })
              })
            }
          } catch (error) {
            console.error('搜索词语失败:', error)
          }
        } else if (selectedType.value === 'zi') {
          try {
            const hanziRes = await request.get('/v1/hanzi', { 
              params: { search: searchQuery.value, size: 50 } 
            })
            if (hanziRes.data.items) {
              hanziRes.data.items.forEach(item => {
                results.push({
                  id: item.id,
                  type: 'zi',
                  word: item.character,
                  pinyin: item.basic_info?.pinyin || '',
                  unicode: item.unicode_decimal,
                  definition: item.yisi_info?.meanings?.join('; ') || '暂无释义',
                  url: item.url,
                  created_by: item.created_by
                })
              })
            }
          } catch (error) {
            console.error('搜索汉字失败:', error)
          }
        } else if (selectedType.value === 'content-system') {
          // 搜索 Content System 题目 (Mock)
          const keyword = searchQuery.value.toLowerCase()
          const matchedExercises = contentSystemMock.exercises.filter(ex => 
            ex.prompt.toLowerCase().includes(keyword) || 
            (ex.metadata.options && ex.metadata.options.some(opt => opt.text && opt.text.toLowerCase().includes(keyword)))
          )
          
          matchedExercises.forEach(ex => {
            const typeInfo = contentSystemMock.exerciseTypes.find(t => t.id === ex.exercise_type_id)
            results.push({
              id: ex.id,
              type: 'content-system',
              word: ex.prompt, // 使用 prompt 作为主要显示文本
              definition: `题型: ${typeInfo?.display_name || '未知'}`,
              difficulty: ex.difficulty_level,
              status: ex.quality_status,
              created_by: ex.created_by,
              // 额外字段
              exerciseType: typeInfo?.display_name,
              options: ex.metadata.options
            })
          })
        } else if (selectedType.value === 'scenario-system') {
          // 搜索 Scenario System 题目 (Mock)
          const keyword = searchQuery.value.toLowerCase()
          const matchedExercises = scenarioSystemMock.slExercises.filter(ex => 
            (ex.metadata.question && ex.metadata.question.toLowerCase().includes(keyword)) ||
            (ex.metadata.prompt && ex.metadata.prompt.toLowerCase().includes(keyword))
          )
          
          matchedExercises.forEach(ex => {
            const typeInfo = scenarioSystemMock.slExerciseTypes.find(t => t.id === ex.exercise_type_id)
            const lesson = scenarioSystemMock.generatedLessons.find(l => l.lesson_db_id === ex.source_lesson_db_id)
            
            results.push({
              id: ex.id,
              type: 'scenario-system',
              word: ex.metadata.question || ex.metadata.prompt, // 使用问题或提示作为主要显示文本
              definition: `题型: ${typeInfo?.name || '未知'} | 来源: ${lesson?.lesson_name || '未知'}`,
              difficulty: ex.difficulty_level,
              created_by: ex.created_by,
              // 额外字段
              exerciseType: typeInfo?.name,
              sourceLesson: lesson?.lesson_name
            })
          })
        } else if (selectedType.value === 'audio' || selectedType.value === 'video') {
          // 音视频搜索 - 待实现
          console.log('音视频搜索功能待实现')
        }

        searchResults.value = results
        totalResults.value = results.length
      } catch (error) {
        console.error('搜索失败:', error)
        alert('搜索失败，请重试')
      } finally {
        loading.value = false
      }
    }

    const quickSearch = (keyword, type = 'chengyu') => {
      searchQuery.value = keyword
      selectedModule.value = 'hanzi'
      selectedType.value = type
      handleSearch()
    }

    const getSearchTypeText = () => {
      const typeMap = {
        'zi': '字',
        'ciyu': '词',
        'chengyu': '成语',
        'content-system': 'Content System',
        'scenario-system': 'Scenario System',
        'audio': '音频',
        'video': '视频'
      }
      return typeMap[selectedType.value] || '资源'
    }

    const canModifyItem = (item) => {
      // 管理员可以修改所有资源
      if (authStore.user?.role === 'admin') {
        return true
      }
      // 老师只能修改自己创建的资源
      if (authStore.user?.role === 'teacher') {
        return item.created_by === authStore.user.username
      }
      return false
    }

    const editItem = (item) => {
      if (item.type === 'chengyu') {
        router.push(`/chengyu?edit=${item.id}`)
      } else {
        router.push(`/ciyu?edit=${item.id}`)
      }
    }

    const deleteItem = async (item) => {
      if (!confirm(`确定要删除"${item.word}"吗？`)) return
      
      try {
        const url = item.type === 'chengyu' 
          ? `/v1/chengyu/${item.id}` 
          : `/v1/ciyu/${item.id}`
        await request.delete(url)
        alert('删除成功')
        handleSearch() // 刷新结果
      } catch (error) {
        console.error('删除失败:', error)
        alert(error.response?.data?.detail || '删除失败')
      }
    }

    const closeResultsModal = () => {
      showResultsModal.value = false
    }

    return {
      authStore,
      searchQuery,
      selectedModule,
      selectedType,
      searchResults,
      loading,
      hasSearched,
      totalResults,
      showResultsModal,
      canSearch,
      handleModuleChange,
      handleTypeChange,
      getSearchPlaceholder,
      handleSearch,
      quickSearch,
      getSearchTypeText,
      canModifyItem,
      editItem,
      deleteItem,
      closeResultsModal
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px;
}

.search-hero {
  position: relative;
  text-align: center;
  padding: 48px 32px 40px;
  margin-bottom: 32px;
  color: #1f2a33;
  background: radial-gradient(circle at 20% 20%, rgba(102, 187, 106, 0.08), transparent 45%),
              radial-gradient(circle at 80% 0%, rgba(102, 187, 106, 0.06), transparent 40%),
              #ffffff;
  border-radius: 20px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(102, 187, 106, 0.12);
}

.search-title {
  font-size: 34px;
  margin-bottom: 12px;
  color: #1b5e20;
  letter-spacing: 0.02em;
  font-weight: 800;
}

.search-subtitle {
  font-size: 15px;
  margin-bottom: 28px;
  color: #4f5b62;
}

.search-wrapper {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  max-width: 760px;
  margin: 0 auto;
  padding: 0;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  backdrop-filter: none;
  border: none;
}

.search-type-select,
.search-subtype-select {
  padding: 12px 18px;
  font-size: 15px;
  border: 1px solid #d7e8dc;
  border-radius: 999px;
  outline: none;
  background: #f7fbf8;
  cursor: pointer;
  color: #1f2a33;
  transition: all 0.25s;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8' fill='none'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='%236b8a7a' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  background-size: 12px 8px;
  padding-right: 48px;
  white-space: nowrap;
  flex-shrink: 0;
}

.search-type-select {
  min-width: 180px;
}

.search-subtype-select {
  min-width: 200px;
}

.search-subtype-select:focus,
.search-type-select:focus {
  box-shadow: 0 0 0 3px rgba(102, 187, 106, 0.15), 0 6px 18px rgba(0, 0, 0, 0.12);
  border-color: #66bb6a;
}

.search-subtype-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f0f0f0;
  border-color: #f0f0f0;
}

.search-input-large {
  flex: 1;
  min-width: 220px;
  padding: 14px 22px;
  font-size: 16px;
  border: 1px solid #d7e8dc;
  border-radius: 999px;
  outline: none;
  background: #ffffff;
  color: #1f2a33;
  transition: all 0.25s;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.search-input-large:hover:not(:disabled) {
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.08);
  border-color: #66bb6a;
}

.search-input-large:focus:not(:disabled) {
  box-shadow: 0 0 0 3px rgba(102, 187, 106, 0.18), 0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: #66bb6a;
}

.search-input-large:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f0f0f0;
  border-color: #e0e0e0;
  color: #999;
}

.search-input-large::placeholder {
  color: #999;
}

.search-input-large:disabled::placeholder {
  color: #ccc;
}

.search-btn {
  padding: 14px 32px;
  font-size: 16px;
  background: linear-gradient(135deg, #66bb6a 0%, #5ca660 100%);
  color: white;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.25s;
  box-shadow: 0 10px 20px rgba(102, 187, 106, 0.25);
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 12px 26px rgba(102, 187, 106, 0.32);
}

.search-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 8px 18px rgba(102, 187, 106, 0.24);
}

.search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #dfe7e1;
  color: #8da298;
  box-shadow: none;
}

/* 三大模块展示区 */
.modules-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 30px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.module-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
  border: 1px solid #e7f0ea;
}

.module-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.module-icon {
  font-size: 32px;
}

.module-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.module-items {
  display: block;
}

.module-group {
  margin-bottom: 16px;
}

.module-group:last-child {
  margin-bottom: 0;
}

.module-group-title {
  font-size: 14px;
  font-weight: bold;
  color: #66bb6a;
  border-radius: 6px;
  padding-bottom: 6px;
}

.module-group-items {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.module-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #f9fcfa 0%, #eef5f0 100%);
  border-radius: 12px;
  text-decoration: none;
  color: #263238;
  border: 1px solid #e1ebe4;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.module-item:hover {
  background: linear-gradient(135deg, #81c784 0%, #66bb6a 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(102, 187, 106, 0.25);
}

.module-item-icon {
  font-size: 22px;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(102, 187, 106, 0.12);
  color: #2e7d32;
  font-weight: 700;
  transition: background 0.2s ease, color 0.2s ease;
}

.module-item:hover .module-item-icon {
  color: white;
  background: rgba(255, 255, 255, 0.2);
}

.module-item-name {
  font-size: 15px;
  font-weight: 500;
}

.module-item.small {
  justify-content: center;
  font-size: 14px;
  padding: 12px 14px;
}

/* 搜索结果弹窗 */
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
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
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

.result-count {
  font-size: 14px;
  color: #666;
  font-weight: normal;
  margin-left: 8px;
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

.loading, .no-results {
  text-align: center;
  padding: 40px;
  color: #666;
}

.results-list {
  display: grid;
  gap: 15px;
}

.result-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: box-shadow 0.2s;
}

.result-card:hover {
  box-shadow: 0 4px 15px rgba(0,0,0,0.12);
}

.result-card:hover {
  box-shadow: 0 4px 15px rgba(0,0,0,0.12);
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

.type-chengyu {
  background: #e8f5e9;
  color: #66bb6a;
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

.result-example {
  color: #666;
  font-style: italic;
  line-height: 1.6;
  margin-bottom: 12px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
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
  cursor: pointer;
  transition: all 0.2s;
}

.relation-tag.synonym {
  background: #e8f5e9;
  color: #2e7d32;
}

.relation-tag.synonym:hover {
  background: #2e7d32;
  color: white;
}

.relation-tag.antonym {
  background: #ffebee;
  color: #c62828;
}

.relation-tag.antonym:hover {
  background: #c62828;
  color: white;
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

.btn-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background: #dc3545;
  color: white;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 40px;
}

.action-card {
  display: block;
  padding: 30px;
  background: white;
  border-radius: 12px;
  text-decoration: none;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: all 0.2s;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.action-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.action-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.action-desc {
  font-size: 14px;
  color: #666;
}
</style>
