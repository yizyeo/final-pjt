<template>
  <div class="review-card">
    <div class="movie-info" @click="$emit('go-movie', review.movie)">
      <img :src="getImageUrl(review.movie_poster)" alt="poster">
      <h5>{{ review.movie_title }}</h5>
    </div>

    <div class="star-rating">
      <span v-for="n in 5" :key="n" class="star">
        {{ getStarChar(n) }}
      </span>
      <span class="score-text">{{ review.rating }}점</span>
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
      <span>by {{ review.username }}</span>
      <button @click="$emit('like', review.id)">
        {{ review.is_liked ? '❤️' : '🤍' }} {{ review.like_count }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps(['review'])
defineEmits(['go-movie', 'go-detail', 'like'])

// 스포일러 상태 관리
const showSpoiler = ref(false)

// 0.5단위 별 모양 결정 로직 (10점 만점 기준)
const getStarChar = (n) => {
  const score = props.review.rating / 2 // 10점 만점을 5점 만점으로 환산
  if (score >= n) return '★'       // 꽉 찬 별
  if (score >= n - 0.5) return '⯪'  // 반 별
  return '☆'                         // 빈 별
}

const getImageUrl = (path) => path ? `https://image.tmdb.org/t/p/w200${path}` : '/no-image.png'
</script>

<style scoped>
.clickable { cursor: pointer; }
.star-rating { color: #ffc107; font-size: 0.9rem; }
/* 빈 별은 어두운 색으로 */
.star:contains('☆') { color: #444; }
.review-content {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.comment-link { color: #0d6efd; font-size: 0.8rem; }
</style>