<template>
  <div class="filter-section" :class="variantClass">
    <div class="filter-row">
      <!-- 技能分类 (Content System) -->
      <div v-if="showSkillCategory" class="filter-item">
        <label><span class="filter-icon">📂</span>技能分类</label>
        <select :value="filters.skillCategory" @change="updateFilter('skillCategory', $event.target.value)" class="filter-select">
          <option value="">全部分类</option>
          <option v-for="cat in skillCategories" :key="cat.id" :value="cat.id">
            {{ cat.description || cat.name }}
          </option>
        </select>
      </div>

      <!-- 来源课程 (Scenario System) -->
      <div v-if="showLesson" class="filter-item">
        <label><span class="filter-icon">📘</span>来源课程</label>
        <select :value="filters.lessonId" @change="updateFilter('lessonId', $event.target.value)" class="filter-select">
          <option value="">全部课程</option>
          <option v-for="lesson in lessons" :key="lesson.lesson_db_id" :value="lesson.lesson_db_id">
            {{ lesson.lesson_name }}
          </option>
        </select>
      </div>
      
      <!-- 题型 -->
      <div class="filter-item">
        <label><span class="filter-icon">🏷️</span>题型</label>
        <select :value="filters.exerciseType" @change="updateFilter('exerciseType', $event.target.value)" class="filter-select">
          <option value="">全部题型</option>
          <option v-for="type in exerciseTypes" :key="type.id" :value="type.id">
            {{ type.display_name || type.name }}
          </option>
        </select>
      </div>
      
      <!-- 难度 -->
      <div class="filter-item">
        <label><span class="filter-icon">📊</span>难度</label>
        <select :value="filters.difficulty" @change="updateFilter('difficulty', $event.target.value)" class="filter-select">
          <option value="">全部难度</option>
          <option v-for="level in difficultyLevels" :key="level.id" :value="level.id">
            {{ level.name }}
          </option>
        </select>
      </div>
      
      <!-- 质检状态 (Content System) -->
      <div v-if="showQualityStatus" class="filter-item">
        <label><span class="filter-icon">✅</span>质检状态</label>
        <select :value="filters.qualityStatus" @change="updateFilter('qualityStatus', $event.target.value)" class="filter-select">
          <option value="">全部状态</option>
          <option value="1">✓ 已通过</option>
          <option value="0">⏳ 待审核</option>
          <option value="-1">✗ 已驳回</option>
        </select>
      </div>
      
      <!-- 搜索 -->
      <div class="filter-item search-item">
        <label><span class="filter-icon">🔍</span>搜索</label>
        <div class="search-wrapper">
          <input 
            v-model="localSearchQuery"
            type="text" 
            class="filter-input"
            placeholder="输入关键词搜索题目..."
            @keyup.enter="handleSearch"
          >
          <button class="btn-search" @click="handleSearch">搜索</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExerciseFilterBar',
  props: {
    // 主题色: green / purple
    variant: {
      type: String,
      default: 'green'
    },
    // 筛选条件对象
    filters: {
      type: Object,
      required: true
    },
    // 搜索关键词
    searchQuery: {
      type: String,
      default: ''
    },
    // 数据源
    skillCategories: {
      type: Array,
      default: () => []
    },
    exerciseTypes: {
      type: Array,
      default: () => []
    },
    lessons: {
      type: Array,
      default: () => []
    },
    difficultyLevels: {
      type: Array,
      default: () => [
        { id: '1', name: '⭐ 简单' },
        { id: '2', name: '⭐⭐ 中等' },
        { id: '3', name: '⭐⭐⭐ 困难' }
      ]
    },
    // 显示控制
    showSkillCategory: {
      type: Boolean,
      default: false
    },
    showLesson: {
      type: Boolean,
      default: false
    },
    showQualityStatus: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:filters', 'update:searchQuery', 'search'],
  data() {
    return {
      localSearchQuery: this.searchQuery
    }
  },
  watch: {
    searchQuery(val) {
      this.localSearchQuery = val
    }
  },
  computed: {
    variantClass() {
      return `filter-${this.variant}`
    }
  },
  methods: {
    updateFilter(key, value) {
      this.$emit('update:filters', {
        ...this.filters,
        [key]: value
      })
    },
    handleSearch() {
      this.$emit('update:searchQuery', this.localSearchQuery)
      this.$emit('search', this.localSearchQuery)
    }
  }
}
</script>

<style scoped>
.filter-section {
  padding: 20px 24px;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.filter-section.filter-green {
  background: linear-gradient(135deg, #f5fff5 0%, #e8f5e9 100%);
  border: 1px solid rgba(76, 175, 80, 0.1);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.08);
}

.filter-section.filter-purple {
  background: linear-gradient(135deg, #faf5ff 0%, #f3e5f5 100%);
  border: 1px solid rgba(171, 71, 188, 0.1);
  box-shadow: 0 4px 12px rgba(106, 27, 154, 0.08);
}

.filter-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 160px;
}

.filter-item.search-item {
  flex: 1;
  min-width: 200px;
}

.filter-item label {
  font-weight: 600;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.filter-green .filter-item label {
  color: #2e7d32;
}

.filter-purple .filter-item label {
  color: #6a1b9a;
}

.filter-icon {
  font-size: 0.9rem;
}

.filter-select,
.filter-input {
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 0.95rem;
  background: white;
  color: #333;
  transition: all 0.2s ease;
  cursor: pointer;
}

.filter-green .filter-select,
.filter-green .filter-input {
  border: 2px solid #c8e6c9;
}

.filter-purple .filter-select,
.filter-purple .filter-input {
  border: 2px solid #e1bee7;
}

.filter-select option {
  color: #333;
  background: white;
  padding: 8px;
}

.filter-green .filter-select:hover,
.filter-green .filter-input:hover {
  border-color: #a5d6a7;
}

.filter-purple .filter-select:hover,
.filter-purple .filter-input:hover {
  border-color: #ce93d8;
}

.filter-green .filter-select:focus,
.filter-green .filter-input:focus {
  outline: none;
  border-color: #66bb6a;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.15);
}

.filter-purple .filter-select:focus,
.filter-purple .filter-input:focus {
  outline: none;
  border-color: #ab47bc;
  box-shadow: 0 0 0 3px rgba(171, 71, 188, 0.15);
}

.filter-input::placeholder {
  color: #aaa;
}

/* 搜索框包装器 */
.search-wrapper {
  display: flex;
  gap: 8px;
}

.search-wrapper .filter-input {
  flex: 1;
}

.btn-search {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.filter-green .btn-search {
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
}

.filter-purple .btn-search {
  background: linear-gradient(135deg, #ab47bc 0%, #6a1b9a 100%);
  color: white;
}

.btn-search:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>
