<template>
  <div>
    <Header />
    <div class="container">
      <h2>词语列表</h2>
      
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input"
          placeholder="搜索词语..."
          @input="handleSearch"
        >
      </div>
      
      <table class="table" v-if="!loading && ciyuList.length > 0">
        <thead>
          <tr>
            <th>词语</th>
            <th>拼音</th>
            <th>词性</th>
            <th>定义</th>
            <th>创建者</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in ciyuList" :key="item.id">
            <td>{{ item.word }}</td>
            <td>{{ item.pinyin }}</td>
            <td>{{ item.part_of_speech || 'N/A' }}</td>
            <td>{{ item.definition }}</td>
            <td>
              <span
                class="owner-pill"
                :class="{ 'owner-pill--me': item.created_by === authStore.user?.username }"
              >
                {{ item.created_by || '系统' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="loading" style="text-align: center; padding: 20px;">
        加载中...
      </div>
      
      <div v-if="!loading && ciyuList.length === 0" style="text-align: center; padding: 20px;">
        暂无数据
      </div>
      
      <div class="pagination" v-if="totalPages > 1">
        <button 
          class="btn" 
          @click="currentPage > 1 && goToPage(currentPage - 1)"
          :disabled="currentPage <= 1"
        >
          上一页
        </button>
        
        <span style="padding: 0 15px;">
          第 {{ currentPage }} 页，共 {{ totalPages }} 页
        </span>
        
        <button 
          class="btn" 
          @click="currentPage < totalPages && goToPage(currentPage + 1)"
          :disabled="currentPage >= totalPages"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import Header from '../components/Header.vue'
import request from '../utils/request'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'CiyuList',
  components: {
    Header
  },
  setup() {
    const authStore = useAuthStore()
    const ciyuList = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(20)
    const total = ref(0)
    
    const totalPages = computed(() => Math.ceil(total.value / pageSize.value))
    
    const fetchCiyu = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          size: pageSize.value
        }
        
        if (searchQuery.value) {
          params.search = searchQuery.value
        }
        
        const response = await request.get('/v2/ciyu', { params })
        ciyuList.value = response.data.items
        total.value = response.data.total
      } catch (error) {
        console.error('获取词语列表失败:', error)
        alert('获取数据失败')
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = async () => {
      currentPage.value = 1
      await fetchCiyu()
    }
    
    const goToPage = async (page) => {
      currentPage.value = page
      await fetchCiyu()
    }
    
    onMounted(() => {
      fetchCiyu()
    })
    
    return {
      authStore,
      ciyuList,
      loading,
      searchQuery,
      currentPage,
      totalPages,
      handleSearch,
      goToPage
    }
  }
}
</script>