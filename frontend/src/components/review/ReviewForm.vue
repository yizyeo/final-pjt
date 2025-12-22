<template>
  <div class="review-form-container bg-dark p-4 rounded-3 border border-secondary mt-5">
    <h4 class="text-white mb-3">이 영화는 어땠나요?</h4>
    
    <div class="star-input-container mb-3">
      <div class="stars">
        <span 
          v-for="score in 5" 
          :key="score"
          class="star-btn"
          :class="{ filled: (hoverScore || rating) >= score }"
          @mouseenter="hoverScore = score"
          @mouseleave="hoverScore = 0"
          @click="setRating(score)"
        >
          ★
        </span>
      </div>
      <span class="score-text ms-2 text-secondary">{{ (hoverScore || rating) * 2 }}점</span>
    </div>

    <div class="input-group">
      <textarea 
        v-model.trim="content"
        class="form-control bg-secondary text-white border-0" 
        placeholder="스포일러 방지를 위해 매너를 지켜주세요!"
        rows="3"
      ></textarea>
      <button @click="submitReview" class="btn btn-primary px-4">등록</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useReviewStore } from '@/stores/review'

const props = defineProps(['moviePk'])
const reviewStore = useReviewStore()

const content = ref('')
const rating = ref(0)      // 클릭한 별점
const hoverScore = ref(0)  // 마우스 올린 별점

const setRating = (score) => {
  rating.value = score
}

const submitReview = async () => {
  if (rating.value === 0) return alert('별점을 선택해주세요!')
  if (!content.value) return alert('내용을 입력해주세요!')

  const payload = {
    content: content.value,
    rating: rating.value * 2  // 백엔드 10점 만점 기준에 맞춤
  }

  try {
    await reviewStore.createReview(props.moviePk, payload)
    content.value = ''
    rating.value = 0
    alert('리뷰가 등록되었습니다!')
  } catch (err) {
    alert('리뷰 등록에 실패했습니다.')
  }
}
</script>

<style scoped>
.star-btn {
  font-size: 2rem;
  color: #444;
  cursor: pointer;
  transition: color 0.1s;
}
.star-btn.filled {
  color: #ffc107;
}
.score-text {
  font-size: 1.2rem;
  font-weight: bold;
}
textarea::placeholder {
  color: #ccc;
}
</style>