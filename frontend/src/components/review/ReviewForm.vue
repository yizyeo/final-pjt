<template>
  <div class="review-form-card">
    <div class="form-header">
      <h4>이 영화, 어떠셨나요?</h4>
      <p class="sub-text">솔직한 리뷰를 남겨주세요.</p>
    </div>

    <div class="star-rating-area">
      <div class="stars" @mouseleave="hoverScore = 0">
        <span 
          v-for="n in 5" 
          :key="n"
          class="star-wrapper"
          @mousemove="handleMouseMove($event, n)"
          @click="setRating"
        >
          <svg v-if="(hoverScore || rating) >= n" 
            xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="star-icon full">
            <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z" clip-rule="evenodd" />
          </svg>
          
          <svg v-else-if="(hoverScore || rating) >= n - 0.5" 
            xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="star-icon half">
            <defs>
              <linearGradient :id="'half-grad-' + n">
                <stop offset="50%" stop-color="#FFC107" />
                <stop offset="50%" stop-color="#E0E0E0" />
              </linearGradient>
            </defs>
            <path fill-rule="evenodd" :fill="`url(#half-grad-${n})`" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z" clip-rule="evenodd" />
          </svg>

          <svg v-else 
            xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="star-icon empty">
            <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z" clip-rule="evenodd" />
          </svg>
        </span>
      </div>
      
      <div class="score-display">
        <span v-if="(hoverScore || rating) > 0" class="score-num">{{ (hoverScore || rating) * 2 }}</span>
        <span v-else class="score-placeholder">평가하기</span>
      </div>
    </div>

    <div class="input-area">
      <textarea 
        v-model.trim="content" 
        placeholder="이 영화의 어떤 점이 좋았나요? 감상평을 남겨주세요."
        rows="3"
      ></textarea>
      
      <div class="form-footer">
        <div class="checkbox-group">
          <input type="checkbox" id="spoiler-check" v-model="isSpoiler">
          <label for="spoiler-check">스포일러가 포함된 리뷰인가요?</label>
        </div>
        
        <button @click="submitReview" class="submit-btn">
          등록
        </button>
      </div>
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
  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX - rect.left // 별 내부에서의 마우스 X 좌표
  
  // 별의 너비의 절반보다 왼쪽이면 0.5점, 아니면 1점
  if (x < rect.width / 2) {
    hoverScore.value = n - 0.5 
  } else {
    hoverScore.value = n 
  }
}

const setRating = () => {
  rating.value = hoverScore.value
}

const submitReview = async () => {
  if (rating.value === 0) return alert('별점을 선택해주세요!')
  if (!content.value) return alert('내용을 입력해주세요!')

  const payload = {
    content: content.value,
    rating: Math.round(rating.value * 2), // 0.5 * 2 = 1점 단위로 변환해서 백엔드 전송
    is_spoiler: isSpoiler.value
  }

  try {
    await reviewStore.createReview(props.moviePk, payload)
    content.value = ''
    rating.value = 0
    isSpoiler.value = false
    alert('소중한 리뷰가 등록되었습니다! 📝')
  } catch (err) {
    alert('리뷰 등록에 실패했습니다.')
  }
}
</script>

<style scoped>
/* 카드 컨테이너 */
.review-form-card {
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  margin-top: 1rem;
}

.form-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-header h4 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.3rem;
}

.sub-text {
  font-size: 0.9rem;
  color: #888;
}

/* 별점 영역 */
.star-rating-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.stars {
  display: flex;
  gap: 8px;
  cursor: pointer;
}

.star-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s;
}

.star-wrapper:hover {
  transform: scale(1.1);
}

.star-icon {
  width: 100%;
  height: 100%;
}

.star-icon.full { color: #FFC107; }
.star-icon.empty { color: #E0E0E0; }

/* 점수 텍스트 */
.score-display {
  margin-top: 0.5rem;
  height: 1.5rem;
}

.score-num {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
}

.score-placeholder {
  font-size: 0.9rem;
  color: #BBB;
}

/* 입력 영역 */
.input-area {
  background-color: #F8F9FA;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #F0F0F0;
}

textarea {
  width: 100%;
  border: none;
  background: transparent;
  resize: none;
  font-size: 0.95rem;
  color: #333;
  outline: none;
  margin-bottom: 1rem;
  font-family: inherit;
}

textarea::placeholder {
  color: #AAA;
}

/* 푸터 (체크박스 & 버튼) */
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #EEE;
  padding-top: 1rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.checkbox-group input {
  cursor: pointer;
  accent-color: #7A6CFA;
}

.checkbox-group label {
  font-size: 0.9rem;
  color: #666;
  cursor: pointer;
  user-select: none;
}

.submit-btn {
  background-color: #7A6CFA;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background-color: #6859D4;
}
</style>