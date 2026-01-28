<template>
  <div class="page-header" :class="variantClass">
    <div class="header-left">
      <h2>
        <span class="header-icon">{{ icon }}</span>
        {{ title }}
      </h2>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
    <div class="header-actions" v-if="$slots.actions || showAddButton">
      <slot name="actions">
        <div class="permission-info" v-if="showPermissionTip">
          <small>💡 操作说明：只能编辑/删除自己创建的资源</small>
        </div>
        <button v-if="showAddButton" class="btn btn-add" @click="$emit('add')">
          + {{ addButtonText }}
        </button>
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageHeader',
  props: {
    icon: {
      type: String,
      default: '📄'
    },
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    },
    variant: {
      type: String,
      default: 'default' // default, green, purple, blue, orange
    },
    showAddButton: {
      type: Boolean,
      default: false
    },
    addButtonText: {
      type: String,
      default: '添加'
    },
    showPermissionTip: {
      type: Boolean,
      default: false
    }
  },
  emits: ['add'],
  computed: {
    variantClass() {
      return `header-${this.variant}`
    }
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.header-left h2 {
  margin: 0 0 5px 0;
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  font-size: 1.6rem;
}

.subtitle {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

/* 主题变体 */
.header-default h2 { color: #333; }
.header-green h2 { color: #1b5e20; }
.header-purple h2 { color: #6a1b9a; }
.header-blue h2 { color: #1565c0; }
.header-orange h2 { color: #e65100; }

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.permission-info {
  color: #666;
  font-size: 0.85rem;
}

.btn-add {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.header-default .btn-add {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-green .btn-add {
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
}

.header-purple .btn-add {
  background: linear-gradient(135deg, #ab47bc 0%, #6a1b9a 100%);
  color: white;
}

.header-blue .btn-add {
  background: linear-gradient(135deg, #42a5f5 0%, #1565c0 100%);
  color: white;
}

.header-orange .btn-add {
  background: linear-gradient(135deg, #ff9800 0%, #e65100 100%);
  color: white;
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>
