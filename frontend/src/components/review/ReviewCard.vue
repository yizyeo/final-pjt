<template>
  <div class="review-card-inner">
    
    <div class="card-header">
      <div class="user-info">
        <div class="tier-badge" :title="userTier.label">
          <img :src="userTier.icon" :alt="userTier.label" class="tier-img">
        </div>
        <span class="username">{{ review.username }}</span>
      </div>
      
      <div class="rating-display">
        <span class="star-icon">★</span>
        <span class="score">{{ review.rating }}</span>
      </div>
    </div>

    <div class="card-body" @click="$emit('go-detail', review.id)">
      
      <div class="poster-area" @click.stop="$emit('go-movie', review.movie)">
        <img :src="getImageUrl(review.movie_poster)" alt="movie poster" class="poster-img">
      </div>

      <div class="text-area">
        <h4 class="movie-title">{{ review.movie_title }}</h4>
        
        <div v-if="review.is_spoiler && !showSpoiler" class="spoiler-mask">
          <p>⚠️ 스포일러가 포함된 리뷰입니다.</p>
          <button @click.stop="showSpoiler = true" class="spoiler-btn">내용 보기</button>
        </div>
        <p v-else class="review-content">{{ review.content }}</p>
      </div>
    </div>

    <div class="card-footer">
      <div class="action-group">
        <button class="action-btn" @click.stop="$emit('like', review.id)" :class="{ 'liked': review.is_liked }">
          <span class="icon">{{ review.is_liked ? '❤️' : '🤍' }}</span>
          <span class="count">{{ review.like_count }}</span>
        </button>
        <div class="action-item">
          <span class="icon">💬</span>
          <span class="count">{{ review.comments_count || 0 }}</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getTier } from '@/utils/tierUtils'

const props = defineProps(['review'])
defineEmits(['go-movie', 'go-detail', 'like'])

const showSpoiler = ref(false)

// 티어 정보 가져오기
const userTier = computed(() => getTier(props.review.user_review_count || 0))

// 포스터 URL 처리
const getImageUrl = (path) => path ? `https://image.tmdb.org/t/p/w200${path}` : '/no-image.png'
</script>

<style scoped>
/* 카드 내부 전체 레이아웃 */
.review-card-inner {
  display: flex;
  flex-direction: column;
  height: 100%; /* 부모 그리드 높이에 꽉 차게 */
  justify-content: space-between;
}

/* 1. Header Styles */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid #F5F5F5;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tier-badge {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #F0F0F0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.tier-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.username {
  font-size: 0.9rem;
  font-weight: 700;
  color: #333333;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #FFD700; /* 별점 색상 */
}

.star-icon {
  font-size: 1rem;
}

.score {
  font-weight: 700;
  color: #333333;
  font-size: 0.9rem;
}

/* 2. Body Styles (가로 배치 핵심) */
.card-body {
  display: flex;
  gap: 1rem;
  flex: 1; /* 남은 공간 차지 */
  margin-bottom: 0.8rem;
  cursor: pointer;
}

.poster-area {
  flex-shrink: 0;
  width: 60px; /* 포스터 너비 */
  height: 90px; /* 포스터 높이 (3:2 비율 유지) */
  border-radius: 6px;
  overflow: hidden;
  background-color: #eee;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.poster-area:hover {
  transform: scale(1.05); /* 포스터 호버 효과 */
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.text-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  justify-content: flex-start; 
}

.movie-title {
  font-size: 1rem;
  font-weight: 700;
  color: #111111;
  margin-bottom: 0.5rem; 
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0; 
}

.review-content {
  font-size: 0.9rem;
  color: #666666;
  line-height: 1.5;
  
  /* 멀티라인 말줄임표 (3줄까지만 표시) */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 스포일러 마스크 */
.spoiler-mask {
  background-color: #F9F9F9;
  border-radius: 8px;
  padding: 0.5rem; /* 패딩을 조금 줄임 */
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex: 1; 
  width: 100%; /* 가로 너비는 꽉 차게 */
}

.spoiler-mask p {
  font-size: 0.8rem;
  color: #888888;
}

.spoiler-btn {
  font-size: 0.8rem;
  color: #7A6CFA;
  background: none;
  border: 1px solid #7A6CFA;
  padding: 2px 8px;
  border-radius: 12px;
  cursor: pointer;
}

/* 3. Footer Styles */
.card-footer {
  display: flex;
  align-items: center;
  padding-top: 0.5rem;
  /* border-top: 1px solid #F5F5F5; (선택사항: 너무 선이 많으면 지저분해 보일 수 있음) */
}

.action-group {
  display: flex;
  gap: 12px;
}

.action-btn, .action-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  color: #888888;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: color 0.2s;
}

.action-btn:hover {
  color: #FF4444; /* 좋아요 호버 색상 */
}

.action-btn.liked {
  color: #FF4444;
}

.icon {
  font-size: 1rem;
}
</style>