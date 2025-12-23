<template>
  <div class="review-card">
    <div class="movie-info" @click="$emit('go-movie', review.movie)">
      <img :src="getImageUrl(review.movie_poster)" alt="poster">
      <h5>{{ review.movie_title }}</h5>
    </div>

    <div class="star-rating">
      <span v-for="n in 5" :key="n">
        {{ getStarChar(n) }}
      </span>
      <span>{{ review.rating }}점</span>
    </div>

    <div class="content-wrapper">
      <div v-if="review.is_spoiler && !showSpoiler">
        <p>⚠️ 스포일러가 포함된 리뷰입니다.</p>
        <button @click.stop="showSpoiler = true">내용 보기</button>
      </div>
      <div v-else class="clickable" @click="$emit('go-detail', review.id)">
        <p class="review-content">{{ review.content }}</p>
        <span class="comment-link">댓글 {{ review.comments_count || 0 }}개 더보기...</span>
      </div>
    </div>

    <div class="footer">
      <div class="user-profile">
        <img :src="userTier.icon" :alt="userTier.label" class="tier-icon-sm">
        <span>{{ review.username }}</span>
      </div>
      
      <button @click="$emit('like', review.id)">
        {{ review.is_liked ? '❤️' : '🤍' }} {{ review.like_count }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getTier } from '@/utils/tierUtils' // 유틸 함수 import

const props = defineProps(['review'])
defineEmits(['go-movie', 'go-detail', 'like'])

const showSpoiler = ref(false)

// [추가] 리뷰 개수에 따른 티어 계산
const userTier = computed(() => getTier(props.review.user_review_count || 0))

const getStarChar = (n) => {
  const score = props.review.rating / 2
  if (score >= n) return '★'
  if (score >= n - 0.5) return '⯪'
  return '☆'
}
const getImageUrl = (path) => path ? `https://image.tmdb.org/t/p/w200${path}` : '/no-image.png'
</script>

<style scoped>
.user-profile { display: flex; align-items: center; gap: 5px; }
.tier-icon-sm { width: 24px; height: 24px; object-fit: contain; }
/* 나머지 스타일 유지 */
.clickable { cursor: pointer; }
.star-rating { color: #ffc107; }
</style>