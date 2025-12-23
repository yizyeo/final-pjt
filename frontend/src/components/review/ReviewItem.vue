<template>
  <div class="review-item">
    <div class="user-info">
      <strong>{{ review.username }}</strong>
      <div class="star-rating">
        <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating / 2 }">★</span>
      </div>
      <span>{{ formatDate(review.created_at) }}</span>
    </div>

    <div class="content-wrapper">
      <div v-if="review.is_spoiler && !showSpoiler">
        <p>스포일러가 포함된 리뷰입니다.</p>
        <button @click="showSpoiler = true">내용 보기</button>
      </div>

      <div v-else @click="goDetail" class="clickable">
        <p class="review-text">{{ review.content }}</p>
        <span>댓글 {{ review.comments_count || 0 }}개 더보기...</span>
      </div>
    </div>
    
    <div>
      <button @click="$emit('like', review.id)">
        {{ review.is_liked ? '❤️' : '🤍' }} {{ review.like_count }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps(['review'])
const emit = defineEmits(['like'])
const router = useRouter()

const showSpoiler = ref(false)

const formatDate = (date) => new Date(date).toLocaleDateString()

const goDetail = () => {
  router.push({ 
    name: 'ReviewDetailView', 
    params: { reviewId: props.review.id } 
  })
}
</script>

<style scoped>
.clickable { cursor: pointer; }
.review-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.star { color: #444; }
.star.filled { color: #ffc107; }
</style>