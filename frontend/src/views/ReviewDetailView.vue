<template>
  <div class="container py-5">
    <button @click="router.back()" class="btn btn-outline-secondary mb-4">← 뒤로가기</button>

    <div v-if="review" class="review-detail-card bg-dark text-white p-4 rounded-3 border border-secondary">
      
      <div v-if="!isEditing">
        <div class="d-flex justify-content-between align-items-start mb-4">
          <div>
            <h2 class="text-warning mb-1">{{ review.movie_title }}</h2>
            <p class="text-secondary small">작성자: {{ review.username }} | {{ formatDate(review.created_at) }}</p>
          </div>
          <div class="d-flex flex-column align-items-end">
            <div class="star-rating fs-4 mb-2">
              <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating / 2 }">★</span>
            </div>
            
            <div v-if="accountStore.username === review.username" class="btn-group btn-group-sm">
              <button @click="toggleEdit" class="btn btn-outline-light">수정</button>
              <button @click="deleteReview" class="btn btn-outline-danger">삭제</button>
            </div>
          </div>
        </div>

        <div class="review-body mb-5">
          <p class="lead" style="white-space: pre-wrap;">{{ review.content }}</p>
        </div>
      </div>

      <div v-else class="edit-mode mb-5">
        <h3 class="text-warning mb-4">리뷰 수정하기</h3>
        <div class="mb-3">
          <label class="form-label text-secondary">평점</label>
          <select v-model="editData.rating" class="form-select bg-secondary text-white border-0 w-25">
            <option v-for="n in [2,4,6,8,10]" :key="n" :value="n">{{ n }}점 (별 {{ n/2 }}개)</option>
          </select>
        </div>
        <div class="mb-3">
          <label class="form-label text-secondary">내용</label>
          <textarea v-model="editData.content" class="form-control bg-secondary text-white border-0" rows="5"></textarea>
        </div>
        <div class="d-flex gap-2">
          <button @click="updateReview" class="btn btn-primary px-4">저장</button>
          <button @click="toggleEdit" class="btn btn-secondary px-4">취소</button>
        </div>
      </div>

      <div class="actions mb-5">
        <button @click="handleLike" class="btn btn-outline-danger" :class="{ active: review.is_liked }">
          {{ review.is_liked ? '❤️ 좋아요 취소' : '🤍 좋아요' }} {{ review.like_count }}
        </button>
      </div>

      <hr class="border-secondary">

      <div class="comment-section mt-5">
        <h4 class="mb-4">댓글 ({{ review.comments?.length || 0 }})</h4>
        <CommentForm @submit-comment="submitComment" />
        <div class="comment-list">
          <CommentItem 
            v-for="comment in review.comments" 
            :key="comment.id" 
            :comment="comment"
            :currentUsername="accountStore.username"
            @delete-comment="deleteComment"
          />
          <p v-if="!review.comments?.length" class="text-secondary text-center">첫 댓글을 남겨보세요!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

import CommentForm from '@/components/review/CommentForm.vue'
import CommentItem from '@/components/review/CommentItem.vue'

const route = useRoute()
const router = useRouter()
const reviewStore = useReviewStore()
const accountStore = useAccountStore()

const review = ref(null)
const isEditing = ref(false)
const editData = ref({ content: '', rating: 0 })
const API_URL = import.meta.env.VITE_API_URL

const fetchReviewDetail = async () => {
  try {
    const res = await axios.get(`${API_URL}/reviews/${route.params.reviewId}/`)
    review.value = res.data
    editData.value.content = res.data.content
    editData.value.rating = res.data.rating
  } catch (err) {
    alert('리뷰를 불러올 수 없습니다.')
  }
}

const toggleEdit = () => {
  isEditing.value = !isEditing.value
}

const updateReview = async () => {
  try {
    await axios({
      method: 'put',
      url: `${API_URL}/reviews/${route.params.reviewId}/`,
      data: editData.value,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    isEditing.value = false
    fetchReviewDetail()
  } catch (err) {
    alert('수정 실패')
  }
}

const deleteReview = async () => {
  if (!confirm('정말 이 리뷰를 삭제하시겠습니까?')) return
  try {
    await axios({
      method: 'delete',
      url: `${API_URL}/reviews/${route.params.reviewId}/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    alert('삭제되었습니다.')
    router.push({ name: 'ReviewListView' })
  } catch (err) {
    alert('삭제 실패')
  }
}

const submitComment = async (content) => {
  try {
    await axios({
      method: 'post',
      url: `${API_URL}/reviews/${route.params.reviewId}/comments/`,
      data: { content },
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    fetchReviewDetail()
  } catch (err) {
    alert('댓글 등록 실패')
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  try {
    await axios({
      method: 'delete',
      url: `${API_URL}/reviews/${route.params.reviewId}/comments/${commentId}/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    fetchReviewDetail()
  } catch (err) {
    alert('댓글 삭제 실패')
  }
}

const handleLike = async () => {
  await reviewStore.likeReview(review.value.id)
  fetchReviewDetail() 
}

const formatDate = (date) => new Date(date).toLocaleString()
onMounted(fetchReviewDetail)
</script>