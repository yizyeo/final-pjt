<template>
  <div class="review-item bg-dark p-3 rounded mb-3 border border-secondary shadow-sm">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <div class="user-info text-white">
        <strong>{{ review.username }}</strong>
        <div class="star-rating d-inline-block ms-2">
          <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating / 2 }">★</span>
        </div>
      </div>
      <span class="text-secondary small">{{ formatDate(review.created_at) }}</span>
    </div>

    <div class="content-wrapper clickable" @click="goDetail">
      <p class="text-white mb-2 review-text">{{ review.content }}</p>
      <span class="text-primary small">댓글 {{ review.comments_count || 0 }}개 더보기...</span>
    </div>
    
    <div class="mt-3">
      <button @click="$emit('like', review.id)" class="btn btn-sm border-0 p-0 text-white">
        {{ review.is_liked ? '❤️' : '🤍' }} {{ review.like_count }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const props = defineProps(['review'])
const emit = defineEmits(['like'])
const router = useRouter()

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