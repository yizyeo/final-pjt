<template>
  <div class="comment-item">
    
    <div class="avatar-column">
      <div class="tier-badge" :title="tier.label">
        <img :src="tier.icon" :alt="tier.label" class="tier-img">
      </div>
    </div>

    <div class="content-column">
      <div class="comment-header">
        <div class="info-group">
          <strong class="username">{{ comment.username }}</strong>
          <span class="date">{{ formatDate(comment.created_at) }}</span>
        </div>

        <button 
          v-if="currentUsername === comment.username" 
          @click="$emit('delete-comment', comment.id)"
          class="delete-btn"
          title="댓글 삭제"
        >
          삭제
        </button>
      </div>

      <p class="comment-text">{{ comment.content }}</p>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { getTier } from '@/utils/tierUtils'

const props = defineProps(['comment', 'currentUsername'])
defineEmits(['delete-comment'])

const tier = computed(() => getTier(props.comment.user_review_count || 0))

const formatDate = (date) => {
  const d = new Date(date)
  // 깔끔하게 날짜만 표시하거나, 시간까지 표시 (원하는 대로 선택)
  return d.toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.comment-item {
  display: flex;
  gap: 12px; /* 좌우 간격 */
  padding: 1.2rem 0;
  border-bottom: 1px solid #F5F5F5; /* 아주 연한 구분선 */
  transition: background-color 0.2s;
}

/* 1. 좌측 아바타 영역 */
.avatar-column {
  flex-shrink: 0;
}

.tier-badge {
  width: 36px;
  height: 36px;
  background-color: #F9F9F9;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  border: 1px solid #EEEEEE;
}

.tier-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* 2. 우측 컨텐츠 영역 */
.content-column {
  flex: 1; /* 남은 공간 다 차지 */
  display: flex;
  flex-direction: column;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4px;
}

.info-group {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.username {
  font-size: 0.9rem;
  font-weight: 700;
  color: #333333;
}

.date {
  font-size: 0.75rem;
  color: #999999;
}

/* 삭제 버튼 (작고 심플하게) */
.delete-btn {
  background: none;
  border: none;
  color: #AAAAAA;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.delete-btn:hover {
  color: #FF4444; /* 호버 시 빨간색 */
  text-decoration: underline;
}

/* 댓글 본문 */
.comment-text {
  font-size: 0.95rem;
  color: #444444;
  line-height: 1.5;
  white-space: pre-wrap; /* 줄바꿈 문자(\n) 반영 */
  word-break: break-all; /* 긴 단어 줄바꿈 */
}
</style>