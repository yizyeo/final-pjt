<template>
  <div>
    <button @click="router.back()">뒤로가기</button>

    <div v-if="reviewStore.currentReview">
      
      <div v-if="!isEditing">
        <div>
          <h2>{{ reviewStore.currentReview.movie_title }}</h2>
          <p>
            작성자: {{ reviewStore.currentReview.username }} | 
            {{ formatDate(reviewStore.currentReview.created_at) }}
          </p>
          
          <div>
            <span v-for="n in 5" :key="n">
              {{ getStarChar(n) }}
            </span>
            <span>({{ reviewStore.currentReview.rating }}점)</span>
          </div>

          <div v-if="accountStore.username === reviewStore.currentReview.username">
            <button @click="toggleEdit">수정</button>
            <button @click="handleDelete">삭제</button>
          </div>
        </div>

        <hr>

        <div>
          <div v-if="reviewStore.currentReview.is_spoiler && !showSpoilerDetail">
            <p>스포일러가 포함된 리뷰입니다.</p>
            <button @click="showSpoilerDetail = true">내용 보기</button>
          </div>

          <p v-else style="white-space: pre-wrap;">
            {{ reviewStore.currentReview.content }}
          </p>
        </div>
      </div>

      <div v-else>
        <h3>리뷰 수정하기</h3>
        <div>
          <label>평점 (1~10점): </label>
          <select v-model="editData.rating">
            <option v-for="n in 10" :key="n" :value="n">{{ n }}점</option>
          </select>
        </div>
        <div>
          <label>내용: </label>
          <textarea v-model="editData.content" rows="5"></textarea>
        </div>
        <div>
          <button @click="handleUpdate">저장</button>
          <button @click="toggleEdit">취소</button>
        </div>
      </div>

      <hr>

      <div>
        <button @click="reviewStore.likeReview(reviewStore.currentReview.id)">
          {{ reviewStore.currentReview.is_liked ? '좋아요 취소' : '좋아요' }} 
          {{ reviewStore.currentReview.like_count }}
        </button>
      </div>

      <hr>

      <div>
        <h4>댓글 ({{ reviewStore.currentReview.comments?.length || 0 }})</h4>
        <CommentForm @submit-comment="submitComment" />
        <div>
          <CommentItem 
            v-for="comment in reviewStore.currentReview.comments" 
            :key="comment.id" 
            :comment="comment"
            :currentUsername="accountStore.username"
            @delete-comment="deleteComment"
          />
          <p v-if="!reviewStore.currentReview.comments?.length">
            첫 댓글을 남겨보세요!
          </p>
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
import CommentForm from '@/components/review/CommentForm.vue'
import CommentItem from '@/components/review/CommentItem.vue'

const route = useRoute()
const router = useRouter()
const reviewStore = useReviewStore()
const accountStore = useAccountStore()

const isEditing = ref(false)
const showSpoilerDetail = ref(false)
const editData = ref({ content: '', rating: 0 })

onMounted(async () => {
  await reviewStore.getReviewDetail(route.params.reviewId)
  
  if (reviewStore.currentReview) {
    editData.value.content = reviewStore.currentReview.content
    editData.value.rating = reviewStore.currentReview.rating
  }
})

const getStarChar = (n) => {
  const score = reviewStore.currentReview.rating / 2
  if (score >= n) return '★'
  if (score >= n - 0.5) return '⯪'
  return '☆'
}

const toggleEdit = () => {
  isEditing.value = !isEditing.value
  if (isEditing.value && reviewStore.currentReview) {
    editData.value.content = reviewStore.currentReview.content
    editData.value.rating = reviewStore.currentReview.rating
  }
}

const handleUpdate = async () => {
  try {
    await reviewStore.updateReview(route.params.reviewId, editData.value)
    isEditing.value = false
    alert('수정되었습니다.')
  } catch (err) {
    alert('수정 실패')
  }
}

const handleDelete = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await reviewStore.deleteReview(route.params.reviewId)
    alert('삭제되었습니다.')
    router.push({ name: 'ReviewListView' })
  } catch (err) {
    alert('삭제 실패')
  }
}

const submitComment = async (content) => {
  try {
    await reviewStore.createComment(route.params.reviewId, content)
  } catch (err) {
    alert('댓글 등록 실패')
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  try {
    await reviewStore.deleteComment(route.params.reviewId, commentId)
  } catch (err) {
    alert('댓글 삭제 실패')
  }
}

const formatDate = (date) => new Date(date).toLocaleString()
</script>