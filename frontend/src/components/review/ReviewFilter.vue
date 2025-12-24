<template>
  <div class="filter-container">
    <button 
      v-for="mode in modes" 
      :key="mode.value"
      @click="$emit('change-sort', mode.value)" 
      class="filter-btn"
      :class="{ active: currentSort === mode.value }"
    >
      <span class="btn-label">{{ mode.label }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps(['currentSort'])
defineEmits(['change-sort'])

const modes = [
  { value: 'popular', label: '인기순' },
  { value: 'latest', label: '최신순' }
]
</script>

<style scoped>
/* 전체 컨테이너: 회색 트랙 */
.filter-container {
  display: inline-flex;
  background-color: #F5F5F5; /* 연한 회색 배경 */
  padding: 4px;
  border-radius: 12px;
  gap: 4px;
}

/* 버튼 기본 스타일 */
.filter-btn {
  border: none;
  background: none;
  padding: 8px 16px; /* 텍스트만 있으므로 패딩을 살짝 조정 */
  border-radius: 8px;
  
  font-size: 0.9rem;
  font-weight: 500;
  color: #888888; /* 비활성 텍스트 색상 */
  
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 호버 효과 */
.filter-btn:hover {
  color: #555555;
  background-color: rgba(0, 0, 0, 0.03);
}

/* 활성화 상태 (Active) */
.filter-btn.active {
  background-color: #FFFFFF; /* 흰색 배경 */
  color: #7A6CFA; /* 브랜드 컬러 텍스트 */
  font-weight: 700;
  
  /* 살짝 떠있는 듯한 그림자 효과 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); 
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .filter-btn {
    padding: 6px 12px;
    font-size: 0.85rem;
  }
}
</style>