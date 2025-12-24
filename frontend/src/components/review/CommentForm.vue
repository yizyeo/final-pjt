<template>
  <div class="comment-form-container">
    <div class="input-wrapper" :class="{ 'focused': isFocused }">
      <input 
        v-model.trim="content" 
        type="text" 
        class="comment-input" 
        placeholder="댓글을 입력하세요."
        @focus="isFocused = true"
        @blur="isFocused = false"
        @keyup.enter="handleSubmit"
      >
      <button 
        @click="handleSubmit" 
        class="submit-btn"
        :class="{ active: content.length > 0 }"
        :disabled="content.length === 0"
      >
        등록
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['submit-comment'])
const content = ref('')
const isFocused = ref(false)

const handleSubmit = () => {
  if (!content.value) return
  emit('submit-comment', content.value)
  content.value = ''
}
</script>

<style scoped>
.comment-form-container {
  width: 100%;
}

/* 입력창 래퍼: 둥근 알약 모양 */
.input-wrapper {
  display: flex;
  align-items: center;
  background-color: #F5F5F5; /* 평소엔 연한 회색 */
  border: 1px solid #EEEEEE;
  border-radius: 30px; /* 완전 둥글게 */
  padding: 6px 6px 6px 24px; /* 버튼 공간 확보 */
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* 입력 중일 때(포커스): 흰색 배경 + 보라색 테두리 + 그림자 */
.input-wrapper.focused {
  background-color: #FFFFFF;
  border-color: #7A6CFA;
  box-shadow: 0 4px 12px rgba(122, 108, 250, 0.15);
}

/* 실제 input 태그 */
.comment-input {
  flex: 1;
  border: none;
  background: none;
  font-size: 0.95rem;
  color: #333333;
  padding: 8px 0;
  outline: none;
}

.comment-input::placeholder {
  color: #AAAAAA;
}

/* 등록 버튼 */
.submit-btn {
  border: none;
  border-radius: 20px;
  padding: 8px 20px;
  font-weight: 600;
  font-size: 0.9rem;
  margin-left: 8px;
  transition: all 0.2s;
  
  /* 기본(비활성) 상태 */
  background-color: #E0E0E0;
  color: #FFFFFF;
  cursor: default;
}

/* 내용이 있을 때(활성) 상태 */
.submit-btn.active {
  background-color: #7A6CFA; /* 브랜드 컬러 */
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(122, 108, 250, 0.2);
}

.submit-btn.active:hover {
  background-color: #6656E0; /* 호버 시 조금 더 진하게 */
  transform: translateY(-1px);
}
</style>