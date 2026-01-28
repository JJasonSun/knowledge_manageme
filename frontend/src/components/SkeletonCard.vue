<template>
  <div class="skeleton-card" :class="variantClass">
    <div class="skeleton-header">
      <div class="skeleton-badges">
        <div class="skeleton-badge"></div>
        <div class="skeleton-badge-sm"></div>
      </div>
    </div>
    <div class="skeleton-body">
      <div class="skeleton-line long"></div>
      <div class="skeleton-line medium"></div>
      <div class="skeleton-block"></div>
      <div class="skeleton-line short"></div>
      <div class="skeleton-line short"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonCard',
  props: {
    variant: {
      type: String,
      default: 'green' // green, purple
    }
  },
  computed: {
    variantClass() {
      return `skeleton-${this.variant}`
    }
  }
}
</script>

<style scoped>
.skeleton-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 2px solid #e0e0e0;
}

.skeleton-green .skeleton-header {
  background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
}

.skeleton-purple .skeleton-header {
  background: linear-gradient(135deg, #f3e5f5 0%, #ede7f6 100%);
}

.skeleton-badges {
  display: flex;
  gap: 8px;
}

.skeleton-badge {
  width: 80px;
  height: 24px;
  border-radius: 12px;
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-green .skeleton-badge {
  background: linear-gradient(90deg, #c8e6c9 25%, #e8f5e9 50%, #c8e6c9 75%);
  background-size: 200% 100%;
}

.skeleton-purple .skeleton-badge {
  background: linear-gradient(90deg, #e1bee7 25%, #f3e5f5 50%, #e1bee7 75%);
  background-size: 200% 100%;
}

.skeleton-badge-sm {
  width: 50px;
  height: 20px;
  background: linear-gradient(90deg, #e8e8e8 25%, #f5f5f5 50%, #e8e8e8 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 10px;
}

.skeleton-body {
  padding: 15px;
}

.skeleton-line {
  height: 14px;
  background: linear-gradient(90deg, #e8e8e8 25%, #f5f5f5 50%, #e8e8e8 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 12px;
}

.skeleton-line.long {
  width: 90%;
}

.skeleton-line.medium {
  width: 70%;
}

.skeleton-line.short {
  width: 50%;
}

.skeleton-block {
  height: 80px;
  background: linear-gradient(90deg, #e8e8e8 25%, #f5f5f5 50%, #e8e8e8 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
  margin: 15px 0;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
