<template>
  <div class="review-item">
    
    <div class="review-header">
      <div 
        class="user-profile" 
        @click.stop="$emit('go-profile', review.username)"
      >
        <div class="tier-badge" :title="userTier.label">
          <img :src="userTier.icon" :alt="userTier.label" class="tier-img">
        </div>
        
        <div class="user-meta">
          <span class="username">{{ review.username }}</span>
          <div class="star-rating">
            <span class="star-icon">⭐</span>
            <span class="rating-score">{{ review.rating }}</span>
          </div>
        </div>
      </div>
      <span class="created-at">{{ formatDate(review.created_at) }}</span>
    </div>

    <div class="review-body">
      <div v-if="review.is_spoiler && !showSpoiler" class="spoiler-overlay">
        <p class="spoiler-warning">⚠️ 스포일러가 포함된 리뷰입니다.</p>
        <button @click.stop="showSpoiler = true" class="spoiler-btn">
          내용 보기
        </button>
      </div>

      <div v-else @click="goDetail" class="content-text clickable">
        <p>{{ review.content }}</p>
      </div>
    </div>

    <div class="review-footer">
      <button 
        @click.stop="$emit('like', review.id)" 
        class="footer-btn like-btn"
        :class="{ active: review.is_liked }"
      >
        <span class="icon">{{ review.is_liked ? '❤️' : '🤍' }}</span>
        <span class="count">{{ review.like_count }}</span>
      </button>

      <button @click.stop="goDetail" class="footer-btn comment-btn">
        <span class="icon">💬</span>
        <span class="count">{{ review.comments_count || 0 }}</span>
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getTier } from '@/utils/tierUtils'

const props = defineProps(['review'])
const emit = defineEmits(['like', 'go-profile'])
const router = useRouter()

const showSpoiler = ref(false)

const userTier = computed(() => getTier(props.review.user_review_count || 0))

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const goDetail = () => {
  router.push({ 
    name: 'ReviewDetailView', 
    params: { reviewId: props.review.id } 
  })
}
</script>

<style scoped>
.review-item {
  padding: 1.5rem 0;
  border-bottom: 1px solid #F0F0F0;
  background-color: #FFF;
  /* [수정] 호버 효과 제거를 위해 transition 및 hover 스타일 삭제 */
}

/* 1. 헤더 */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.user-profile:hover {
  opacity: 0.7;
}

.tier-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #F0F0F0;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
}

.tier-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 0.95rem;
  font-weight: 700;
  color: #333;
}

.star-rating {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 0.85rem;
}
.star-icon { color: #FFC107; font-size: 0.9rem; }
.rating-score { font-weight: 600; color: #555; }

.created-at {
  font-size: 0.85rem;
  color: #AAA;
}

/* 2. 본문 */
.review-body {
  margin-bottom: 1rem;
  padding-left: 40px; 
}

.content-text {
  cursor: pointer;
  line-height: 1.6;
  color: #444;
  font-size: 0.95rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: pre-line;
}

/* 스포일러 오버레이 */
.spoiler-overlay {
  background-color: #F9F9F9;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 1px dashed #DDD;
}
.spoiler-warning {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
.spoiler-btn {
  background: none;
  border: 1px solid #CCC;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #666;
  cursor: pointer;
}
.spoiler-btn:hover { background-color: #FFF; }

/* 3. 푸터 */
.review-footer {
  display: flex;
  gap: 12px;
  padding-left: 40px;
}

.footer-btn {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.9rem;
  color: #888;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.footer-btn:hover {
  background-color: #F0F0F0;
}

.footer-btn .count {
  font-size: 0.85rem;
  margin-top: 2px;
}

/* 좋아요 활성화 */
.like-btn.active .count {
  color: #E11D48;
  font-weight: 600;
}
</style>