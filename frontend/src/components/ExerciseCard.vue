<template>
  <div class="exercise-card" :class="variantClass">
    <div class="card-header" :class="headerClass">
      <div class="header-left">
        <slot name="left"></slot>
      </div>
      <div class="header-right">
        <slot name="right"></slot>
      </div>
    </div>
    <div class="card-body">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExerciseCard',
  props: {
    variant: {
      type: String,
      default: 'green'
    }
  },
  computed: {
    headerClass() {
      return this.variant === 'purple' ? 'variant-purple' : 'variant-green'
    },
    variantClass() {
      return `card-${this.variant}`
    }
  }
}
</script>

<style scoped>
.exercise-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 580px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 2px solid #e0e0e0;
  flex-shrink: 0;
}

.card-header.variant-green {
  background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
}

.card-header.variant-purple {
  background: linear-gradient(135deg, #f3e5f5 0%, #ede7f6 100%);
}

.header-left,
.header-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.card-body {
  padding: 15px;
  overflow-y: scroll;
  flex: 1;
}

/* ========== 通用子组件样式 ========== */

/* 题干 */
:deep(.exercise-prompt) {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.6;
}

/* 信息区域 */
:deep(.exercise-info) {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 24px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.card-green :deep(.exercise-info) {
  background: linear-gradient(135deg, #f5fff5 0%, #e4f7e4 100%);
}

.card-purple :deep(.exercise-info) {
  background: linear-gradient(135deg, #faf5ff 0%, #ede4f7 100%);
}

:deep(.info-row) {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: #444;
}

:deep(.info-icon) {
  font-size: 1rem;
}

:deep(.info-text) {
  color: #333;
}

:deep(.info-label) {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.card-green :deep(.info-label) {
  color: #2e7d32;
}

.card-purple :deep(.info-label) {
  color: #6a1b9a;
}

/* 单词/词汇信息 */
:deep(.word-info) {
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.card-green :deep(.word-info) {
  background: #f1f8e9;
  border-left: 4px solid #4caf50;
}

.card-purple :deep(.word-info) {
  background: #f3e5f5;
  border-left: 4px solid #ab47bc;
}

:deep(.word-sub) {
  font-size: 0.85rem;
  color: #666;
  margin-top: 4px;
  padding-left: 24px;
}

/* ========== 开发者信息折叠 ========== */
:deep(.id-details) {
  background: #fafafa;
  border: 1px dashed #ddd;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 0.85rem;
}

:deep(.id-summary) {
  padding: 8px 12px;
  cursor: pointer;
  color: #888;
  font-size: 0.85rem;
  user-select: none;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

:deep(.id-summary)::before {
  content: '▶';
  font-size: 0.7rem;
  transition: transform 0.2s;
}

:deep(.id-details[open]) > :deep(.id-summary)::before {
  transform: rotate(90deg);
}

:deep(.id-summary::-webkit-details-marker) {
  display: none;
}

:deep(.id-summary:hover) {
  color: #666;
  background: #f5f5f5;
  border-radius: 6px;
}

:deep(.id-content) {
  padding: 10px 12px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
  border-top: 1px dashed #ddd;
}

:deep(.id-item) {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #666;
}

:deep(.id-item span) {
  color: #999;
  min-width: 50px;
}

:deep(.id-item code) {
  font-family: 'Consolas', 'Monaco', monospace;
  background: #e8e8e8;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #555;
  word-break: break-all;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ========== Metadata 折叠 ========== */
:deep(.meta-details) {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 15px;
  overflow: hidden;
}

:deep(.meta-summary) {
  padding: 10px 12px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  user-select: none;
  list-style: none;
}

.card-green :deep(.meta-summary) {
  color: #2e7d32;
}

.card-purple :deep(.meta-summary) {
  color: #6a1b9a;
}

:deep(.meta-summary)::before {
  content: '▶';
  font-size: 0.7rem;
  transition: transform 0.2s;
  flex-shrink: 0;
}

:deep(.meta-details[open]) > :deep(.meta-summary)::before {
  transform: rotate(90deg);
}

:deep(.meta-summary::-webkit-details-marker) {
  display: none;
}

.card-green :deep(.meta-summary:hover) {
  background: #f1f8e9;
}

.card-purple :deep(.meta-summary:hover) {
  background: #f3e5f5;
}

:deep(.meta-actions) {
  display: inline-flex;
  gap: 6px;
  margin-left: auto;
}

:deep(.json-preview) {
  width: 100%;
  padding: 12px;
  border-top: 1px solid #e0e0e0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
  background: #fff;
  color: #555;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}

:deep(.json-editor) {
  width: 100%;
  min-height: 180px;
  padding: 12px;
  border: none;
  border-top: 1px solid #e0e0e0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.5;
  background: #fff;
  color: #333;
  resize: vertical;
}

.card-green :deep(.json-editor:focus) {
  outline: 2px solid #4caf50;
  outline-offset: -2px;
}

.card-purple :deep(.json-editor:focus) {
  outline: 2px solid #ab47bc;
  outline-offset: -2px;
}

:deep(.error-text) {
  padding: 8px 12px;
  color: #d32f2f;
  font-size: 0.85rem;
  background: #ffebee;
  border-top: 1px solid #ffcdd2;
}

/* ========== 通用按钮 ========== */
:deep(.btn-small) {
  padding: 4px 10px;
  font-size: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s;
}

:deep(.btn-small:hover) {
  background: #f5f5f5;
}

.card-green :deep(.btn-small.primary) {
  background: #4caf50;
  color: white;
  border-color: #4caf50;
}

.card-green :deep(.btn-small.primary:hover) {
  background: #43a047;
}

.card-purple :deep(.btn-small.primary) {
  background: #ab47bc;
  color: white;
  border-color: #ab47bc;
}

.card-purple :deep(.btn-small.primary:hover) {
  background: #9c27b0;
}

/* ========== 媒体区域 ========== */
:deep(.media-section) {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #e0e0e0;
}

:deep(.media-list) {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

:deep(.media-item-wrapper) {
  background: #fafafa;
  border-radius: 8px;
  overflow: hidden;
}

:deep(.media-item) {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  flex-wrap: wrap;
}

:deep(.media-icon) {
  font-size: 1.2rem;
}

:deep(.media-name) {
  font-weight: 500;
  color: #333;
  flex: 1;
  min-width: 100px;
}

:deep(.media-role) {
  font-size: 0.8rem;
  padding: 2px 8px;
  border-radius: 10px;
}

.card-green :deep(.media-role) {
  background: #e8f5e9;
  color: #2e7d32;
}

.card-purple :deep(.media-role) {
  background: #f3e5f5;
  color: #7b1fa2;
}

:deep(.media-type) {
  font-size: 0.75rem;
  color: #999;
}

:deep(.media-preview-container) {
  padding: 10px;
  background: #f5f5f5;
  border-top: 1px solid #eee;
}

:deep(.media-preview-img) {
  max-width: 100%;
  max-height: 150px;
  border-radius: 6px;
  object-fit: contain;
}

:deep(.media-preview-audio) {
  width: 100%;
  max-width: 300px;
}

:deep(.media-preview-video) {
  width: 100%;
  max-height: 200px;
  border-radius: 6px;
}

:deep(.media-no-url) {
  padding: 8px 10px;
  font-size: 0.85rem;
  color: #f57c00;
  background: #fff3e0;
  border-top: 1px solid #ffe0b2;
}

/* ========== 徽章 ========== */
:deep(.type-badge) {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.card-green :deep(.type-badge) {
  background-color: #c8e6c9;
  color: #1b5e20;
}

.card-purple :deep(.type-badge) {
  background-color: #e1bee7;
  color: #4a148c;
}

:deep(.difficulty-badge) {
  font-size: 0.85rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 12px;
}

:deep(.difficulty-badge.easy) {
  background: #e8f5e9;
  color: #2e7d32;
}

:deep(.difficulty-badge.medium) {
  background: #fff3e0;
  color: #ef6c00;
}

:deep(.difficulty-badge.hard) {
  background: #ffebee;
  color: #c62828;
}

:deep(.status-badge) {
  font-size: 0.8rem;
  padding: 3px 8px;
  border-radius: 10px;
}

:deep(.status-badge.passed) {
  background: #e8f5e9;
  color: #2e7d32;
}

:deep(.status-badge.pending) {
  background: #fff3e0;
  color: #ef6c00;
}

:deep(.status-badge.rejected) {
  background: #ffebee;
  color: #c62828;
}
</style>
