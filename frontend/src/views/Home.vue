<template>
  <div>
    <Header />
    <div class="home-container">
      <!-- 大搜索框区域 -->
      <div class="search-hero">
        <h1 class="search-title">中文教育资源查询</h1>
        <p class="search-subtitle">搜索成语、词语，探索中文之美</p>
        
        <div class="search-wrapper">
          <select v-model="searchType" class="search-type-select">
            <option value="chengyu">成语</option>
            <option value="ciyu">词语</option>
          </select>
          <input 
            v-model="searchQuery" 
            type="text" 
            class="search-input-large"
            :placeholder="searchType === 'chengyu' ? '输入成语进行搜索...' : '输入词语进行搜索...'"
            @keyup.enter="handleSearch"
          >
          <button class="search-btn" @click="handleSearch" :disabled="!searchQuery.trim()">
            搜索
          </button>
        </div>
      </div>

      <!-- 样例常用词语 -->
      <div class="sample-section">
        <h3 class="section-title">常用成语</h3>
        <div class="sample-tags">
          <span 
            v-for="item in sampleChengyu" 
            :key="item" 
            class="sample-tag"
            @click="quickSearch(item)"
          >
            {{ item }}
          </span>
        </div>
      </div>

      <div class="sample-section">
        <h3 class="section-title">常用词语</h3>
        <div class="sample-tags">
          <span 
            v-for="item in sampleCiyu" 
            :key="item" 
            class="sample-tag sample-tag--ciyu"
            @click="quickSearch(item)"
          >
            {{ item }}
          </span>
        </div>
      </div>

      <!-- 搜索结果区域 -->
      <div v-if="hasSearched" class="results-section">
        <h3 class="section-title">
          搜索结果 
          <span class="result-count">
            （{{ getSearchTypeText() }}，共 {{ totalResults }} 条）
          </span>
        </h3>

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
            
            <!-- 定义/解释 -->
            <div class="result-definition">
              <span class="label">{{ item.type === 'chengyu' ? '解释：' : '定义：' }}</span>
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
              <button class="btn-small" @click="editItem(item)">编辑</button>
              <button class="btn-small btn-danger" @click="deleteItem(item)">删除</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="quick-actions">
        <router-link to="/chengyu" class="action-card">
          <div class="action-icon">📚</div>
          <div class="action-title">成语管理</div>
          <div class="action-desc">浏览和管理成语资源</div>
        </router-link>
        <router-link to="/ciyu" class="action-card">
          <div class="action-icon">📖</div>
          <div class="action-title">词语管理</div>
          <div class="action-desc">浏览和管理词语资源</div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Header from '../components/Header.vue'
import request from '../utils/request'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Home',
  components: { Header },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const searchQuery = ref('')
    const searchType = ref('chengyu')
    const searchResults = ref([])
    const loading = ref(false)
    const hasSearched = ref(false)
    const totalResults = ref(0)

    // 样例成语
    const sampleChengyu = ref([
      '一心一意', '画龙点睛', '守株待兔', '亡羊补牢', 
      '掩耳盗铃', '刻舟求剑', '叶公好龙', '杯弓蛇影'
    ])

    // 样例词语
    const sampleCiyu = ref([
      '学习', '知识', '教育', '文化', 
      '语言', '阅读', '写作', '思考'
    ])

    const handleSearch = async () => {
      if (!searchQuery.value.trim()) return
      
      loading.value = true
      hasSearched.value = true
      searchResults.value = []
      
      try {
        const results = []
        
        // 根据搜索类型查询对应的API
        if (searchType.value === 'chengyu') {
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
        } else if (searchType.value === 'ciyu') {
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

    const quickSearch = (keyword) => {
      searchQuery.value = keyword
      handleSearch()
    }

    const getSearchTypeText = () => {
      const typeMap = {
        'chengyu': '成语',
        'ciyu': '词语'
      }
      return typeMap[searchType.value] || '成语'
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

    return {
      authStore,
      searchQuery,
      searchType,
      searchResults,
      loading,
      hasSearched,
      totalResults,
      sampleChengyu,
      sampleCiyu,
      handleSearch,
      quickSearch,
      getSearchTypeText,
      canModifyItem,
      editItem,
      deleteItem
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.search-hero {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  margin-bottom: 30px;
  color: white;
}

.search-title {
  font-size: 32px;
  margin-bottom: 10px;
}

.search-subtitle {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 30px;
}

.search-wrapper {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  gap: 10px;
}

.search-type-select {
  padding: 16px 20px;
  font-size: 16px;
  border: none;
  border-radius: 50px;
  outline: none;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  background: white;
  color: #667eea;
  font-weight: bold;
  min-width: 100px;
}

.search-input-large {
  flex: 1;
  padding: 16px 24px;
  font-size: 18px;
  border: none;
  border-radius: 50px;
  outline: none;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.search-btn {
  padding: 16px 32px;
  font-size: 16px;
  background: #fff;
  color: #667eea;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s;
}

.search-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sample-section {
  margin-bottom: 25px;
}

.section-title {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-count {
  font-size: 14px;
  color: #666;
  font-weight: normal;
}

.sample-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.sample-tag {
  padding: 8px 16px;
  background: #e8f4fd;
  color: #1976d2;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.sample-tag:hover {
  background: #1976d2;
  color: white;
}

.sample-tag--ciyu {
  background: #e8f5e9;
  color: #388e3c;
}

.sample-tag--ciyu:hover {
  background: #388e3c;
  color: white;
}

.results-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
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
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: box-shadow 0.2s;
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
  background: #e3f2fd;
  color: #1565c0;
}

.type-ciyu {
  background: #e8f5e9;
  color: #2e7d32;
}

.result-mine {
  padding: 2px 8px;
  background: #fff3e0;
  color: #e65100;
  border-radius: 4px;
  font-size: 12px;
}

.result-admin {
  padding: 2px 8px;
  background: #fff3e0;
  color: #e65100;
  border-radius: 4px;
  font-size: 12px;
}

.result-system {
  padding: 2px 8px;
  background: #f3e5f5;
  color: #7b1fa2;
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
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.btn-small:hover {
  background: #f5f5f5;
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
