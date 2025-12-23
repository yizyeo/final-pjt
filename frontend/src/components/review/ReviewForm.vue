<template>
  <div class="review-form-container">
    <h4>이 영화는 어땠나요?</h4>
    
    <div class="star-input-container">
      <div class="stars" @mouseleave="hoverScore = 0">
        <span 
          v-for="n in 5" 
          :key="n"
          class="star-btn"
          @mousemove="handleMouseMove($event, n)"
          @click="setRating"
        >
          {{ getStarChar(n) }}
        </span>
      </div>
      <span class="score-text">{{ (hoverScore || rating) * 2 }}점</span>
    </div>

    <div>
      <input type="checkbox" id="spoiler-check" v-model="isSpoiler">
      <label for="spoiler-check">스포일러가 포함된 댓글입니다.</label>
    </div>

    <div>
      <textarea v-model.trim="content" placeholder="리뷰 내용을 입력해주세요."></textarea>
      <button @click="submitReview">등록</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useReviewStore } from '@/stores/review'

const props = defineProps(['moviePk'])
const reviewStore = useReviewStore()

const content = ref('')
const rating = ref(0)      // 저장된 별 개수 (0.5 단위)
const hoverScore = ref(0)  // 호버 중인 별 개수 (0.5 단위)
const isSpoiler = ref(false)

// 마우스 위치에 따라 0.5점 단위 계산
const handleMouseMove = (event, n) => {
  const rect = event.target.getBoundingClientRect()
  const x = event.clientX - rect.left // 별 내부에서의 마우스 X 좌표
  
  if (x < rect.width / 2) {
    hoverScore.value = n - 0.5 // 왼쪽 절반
  } else {
    hoverScore.value = n // 오른쪽 절반
  }
}

const setRating = () => {
  rating.value = hoverScore.value
}

// 별 모양 결정 로직
const getStarChar = (n) => {
  const current = hoverScore.value || rating.value
  if (current >= n) return '★'       // 꽉 찬 별
  if (current >= n - 0.5) return '⯪'  // 반 별 (유니코드 하프 스타)
  return '☆'                         // 빈 별
}

const submitReview = async () => {
  if (rating.value === 0) return alert('별점을 선택해주세요!')
  if (!content.value) return alert('내용을 입력해주세요!')

  const payload = {
    content: content.value,
    rating: Math.round(rating.value * 2), // 0.5 * 2 = 1점 단위로 변환
    is_spoiler: isSpoiler.value
  }

  try {
    await reviewStore.createReview(props.moviePk, payload)
    content.value = ''
    rating.value = 0
    isSpoiler.value = false
    alert('리뷰가 등록되었습니다!')
  } catch (err) {
    alert('리뷰 등록에 실패했습니다.')
  }
}
</script>

<style scoped>
.star-btn {
  font-size: 2rem;
  cursor: pointer;
  display: inline-block;
  width: 1.1em; /* 별 간격 조절 */
  color: #ffc107; /* 기본적으로 노란색, 로직으로 빈별 구분 */
}
/* 점수가 없는 별은 회색으로 */
.star-btn:has(text:contains('☆')) {
  color: #444;
}
.score-text {
  font-size: 1.2rem;
  font-weight: bold;
}
</style>