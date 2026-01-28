<template>
  <div class="search-bar" :class="variantClass">
    <div class="search-input-wrapper">
      <span class="search-icon">🔍</span>
      <input 
        v-model="localQuery"
        type="text" 
        class="search-input"
        :placeholder="placeholder"
        @keyup.enter="handleSearch"
      >
    </div>
    <button class="btn-search" @click="handleSearch" :disabled="loading">
      {{ loading ? '搜索中...' : '搜索' }}
    </button>
    <button v-if="showClear && localQuery" class="btn-clear" @click="handleClear">
      清空
    </button>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: '输入关键词搜索...'
    },
    variant: {
      type: String,
      default: 'default' // default, green, purple, blue, orange
    },
    loading: {
      type: Boolean,
      default: false
    },
    showClear: {
      type: Boolean,
      default: true
    }
  },
  emits: ['update:modelValue', 'search', 'clear'],
  data() {
    return {
      localQuery: this.modelValue
    }
  },
  watch: {
    modelValue(val) {
      this.localQuery = val
    }
  },
  methods: {
    handleSearch() {
      this.$emit('update:modelValue', this.localQuery)
      this.$emit('search', this.localQuery)
    },
    handleClear() {
      this.localQuery = ''
      this.$emit('update:modelValue', '')
      this.$emit('clear')
      this.$emit('search', '')
    }
  }
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.search-bar.search-default {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid #dee2e6;
}

.search-bar.search-green {
  background: linear-gradient(135deg, #f5fff5 0%, #e8f5e9 100%);
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.search-bar.search-purple {
  background: linear-gradient(135deg, #faf5ff 0%, #f3e5f5 100%);
  border: 1px solid rgba(171, 71, 188, 0.2);
}

.search-bar.search-blue {
  background: linear-gradient(135deg, #f5f9ff 0%, #e3f2fd 100%);
  border: 1px solid rgba(33, 150, 243, 0.2);
}

.search-bar.search-orange {
  background: linear-gradient(135deg, #fffaf5 0%, #fff3e0 100%);
  border: 1px solid rgba(255, 152, 0, 0.2);
}

.search-input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  padding: 0 12px;
  border: 2px solid #e0e0e0;
  transition: all 0.2s;
}

.search-default .search-input-wrapper:focus-within {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.search-green .search-input-wrapper:focus-within {
  border-color: #4caf50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.15);
}

.search-purple .search-input-wrapper:focus-within {
  border-color: #ab47bc;
  box-shadow: 0 0 0 3px rgba(171, 71, 188, 0.15);
}

.search-blue .search-input-wrapper:focus-within {
  border-color: #2196f3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.15);
}

.search-orange .search-input-wrapper:focus-within {
  border-color: #ff9800;
  box-shadow: 0 0 0 3px rgba(255, 152, 0, 0.15);
}

.search-icon {
  font-size: 1.1rem;
  margin-right: 8px;
}

.search-input {
  flex: 1;
  padding: 12px 0;
  border: none;
  font-size: 1rem;
  background: transparent;
  color: #333;
}

.search-input:focus {
  outline: none;
}

.search-input::placeholder {
  color: #999;
}

.btn-search {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.search-default .btn-search {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.search-green .btn-search {
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
}

.search-purple .btn-search {
  background: linear-gradient(135deg, #ab47bc 0%, #6a1b9a 100%);
  color: white;
}

.search-blue .btn-search {
  background: linear-gradient(135deg, #42a5f5 0%, #1565c0 100%);
  color: white;
}

.search-orange .btn-search {
  background: linear-gradient(135deg, #ff9800 0%, #e65100 100%);
  color: white;
}

.btn-search:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-search:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-clear {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-clear:hover {
  border-color: #bbb;
  color: #333;
}
</style>
