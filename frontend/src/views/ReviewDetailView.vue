<template>
  <div class="container py-5">
    <button @click="router.back()" class="btn btn-outline-secondary mb-4">
      ← 뒤로가기
    </button>

    <div v-if="review" class="review-detail-card bg-dark text-white p-4 rounded-3 border border-secondary">
      <div class="d-flex justify-content-between align-items-start mb-4">
        <div>
          <h2 class="text-warning mb-1">{{ review.movie_title }}</h2>
          <p class="text-secondary small">작성자: {{ review.username }} | {{ formatDate(review.created_at) }}</p>
        </div>
        <div class="star-rating">
          <span v-for="i in 5" :key="i" class="star fs-4" :class="{ filled: i <= review.rating / 2 }">★</span>
        </div>
      </div>

      <div class="review-body mb-5">
        <p class="lead" style="white-space: pre-wrap;">{{ review.content }}</p>
      </div>

      <div class="actions mb-5">
        <button @click="handleLike" class="btn btn-outline-danger" :class="{ active: review.is_liked }">
          {{ review.is_liked ? '❤️ 좋아요 취소' : '🤍 좋아요' }} {{ review.like_count }}
        </button>
      </div>

      <hr class="border-secondary">

      <div class="comment-section mt-5">
        <h4 class="mb-4">댓글 ({{ review.comments?.length || 0 }})</h4>
        
        <div class="comment-form mb-4">
          <div class="input-group">
            <input 
              v-model.trim="commentContent" 
              type="text" 
              class="form-control bg-secondary text-white border-0" 
              placeholder="댓글을 남겨보세요..."
              @keyup.enter="submitComment"
            >
            <button @click="submitComment" class="btn btn-primary">등록</button>
          </div>
        </div>

        <div class="comment-list">
          <div v-for="comment in review.comments" :key="comment.id" class="comment-item border-bottom border-secondary py-3">
            <div class="d-flex justify-content-between">
              <strong>{{ comment.username }}</strong>
              <span class="text-secondary small">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="mt-2 mb-0">{{ comment.content }}</p>
          </div>
          <p v-if="!review.comments?.length" class="text-secondary">첫 댓글을 남겨보세요!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter()
const reviewStore = useReviewStore()
const accountStore = useAccountStore()

const review = ref(null)
const commentContent = ref('')
const API_URL = import.meta.env.VITE_API_URL

const fetchReviewDetail = async () => {
  try {
    const res = await axios.get(`${API_URL}/reviews/${route.params.reviewId}/`)
    review.value = res.data
  } catch (err) {
    console.error(err)
    alert('리뷰를 불러올 수 없습니다.')
  }
}

const submitComment = async () => {
  if (!commentContent.value) return
  
  try {
    await axios({
      method: 'post',
      url: `${API_URL}/reviews/${route.params.reviewId}/comments/`,
      data: { content: commentContent.value },
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    commentContent.value = ''
    fetchReviewDetail()
  } catch (err) {
    alert('댓글 등록 실패')
  }
}


const handleLike = async () => {
  await reviewStore.likeReview(review.value.id)
  fetchReviewDetail() 
}

const formatDate = (date) => new Date(date).toLocaleString()

onMounted(fetchReviewDetail)
</script>

<style scoped>
.star { color: #444; }
.star.filled { color: #ffc107; }
.review-detail-card { min-height: 400px; }
.comment-item:last-child { border-bottom: none !important; }
</style>