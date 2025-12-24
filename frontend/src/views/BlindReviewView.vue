<template>
  <div class="blind-container">
    
    <header class="page-header">
      <h2>Blind Pick 🎬</h2>
      <p>마음에 드는 리뷰를 선택하면 영화가 공개됩니다.</p>
    </header>

    <div v-if="loading" class="status-msg">
      <div class="spinner"></div>
      <p>AI가 취향 저격 영화를 선별 중입니다...</p>
    </div>

    <div v-else-if="reviews.length === 0" class="status-msg">
      <p>추천할 리뷰가 없습니다. 😭</p>
      <button @click="router.push({ name: 'HomeView' })">홈으로</button>
    </div>

    <div v-else class="review-grid">
      <div 
        v-for="(review, index) in reviews" 
        :key="review.id" 
        class="review-card"
        @click="selectReview(review)"
      >
        <div class="card-content">
          <span class="quote-mark">❝</span>
          <p class="review-text">{{ truncateText(review.content, 80) }}</p>
          <span class="card-footer">클릭해서 확인하기</span>
        </div>
      </div>
    </div>

    <div v-if="selectedReview" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">✕</button>
        
        <div class="modal-poster">
          <img 
            :src="getPosterUrl(selectedReview.movie_poster)" 
            alt="Movie Poster" 
          />
        </div>

        <div class="modal-info">
          <h3>{{ selectedReview.movie_title }}</h3>
          <p class="full-review">"{{ selectedReview.content }}"</p>
          
          <div class="modal-actions">
            <button class="btn-detail" @click="goToDetail(selectedReview.movie)">
              상세 정보 보기
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()

const reviews = ref([])
const loading = ref(true)
const selectedReview = ref(null) // 현재 선택된(열린) 리뷰

const API_URL = import.meta.env.VITE_API_URL

// 1. 데이터 가져오기
const fetchRecommendations = async () => {
  loading.value = true
  try {
    const res = await axios.get(
      `${API_URL}/reviews/blind/recommend/`,
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    reviews.value = res.data
  } catch (err) {
    console.error(err)
    alert('추천 목록을 불러오지 못했습니다.')
  } finally {
    loading.value = false
  }
}

// 2. 리뷰 선택 (모달 열기)
const selectReview = (review) => {
  selectedReview.value = review
}

// 3. 모달 닫기
const closeModal = () => {
  selectedReview.value = null
}

// 4. 상세 페이지 이동
const goToDetail = (movieId) => {
  router.push({ name: 'MovieDetailView', params: { movieId } })
}

// 유틸: 포스터 URL
const getPosterUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : 'https://via.placeholder.com/500x750'
}

// 유틸: 텍스트 말줄임
const truncateText = (text, length) => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
/* 전체 레이아웃 */
.blind-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

.page-header h2 {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #00C6FF, #0072FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-header p {
  color: #888;
  margin-bottom: 40px;
}

/* 그리드 레이아웃 (반응형) */
.review-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

/* 리뷰 카드 스타일 */
.review-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #eee;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  position: relative;
  overflow: hidden;
}

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  border-color: #0072FF;
}

.card-content {
  position: relative;
  z-index: 1;
}

.quote-mark {
  font-size: 2rem;
  color: #0072FF;
  opacity: 0.2;
  display: block;
  margin-bottom: 10px;
}

.review-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  line-height: 1.5;
  margin-bottom: 20px;
  word-break: keep-all;
}

.card-footer {
  font-size: 0.85rem;
  color: #999;
  font-weight: 500;
}

/* 모달 (팝업) 스타일 */
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  z-index: 10000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 800px;
  border-radius: 20px;
  display: flex;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
  position: relative;
  animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.close-btn {
  position: absolute;
  top: 15px; right: 20px;
  background: none; border: none;
  font-size: 1.5rem; cursor: pointer;
  color: #333;
  z-index: 10;
}

.modal-poster {
  width: 40%;
  background: #000;
}

.modal-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-info {
  width: 60%;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}

.modal-info h3 {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 20px;
}

.full-review {
  font-size: 1.2rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 30px;
  font-style: italic;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}

.btn-detail {
  background: #0072FF;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 30px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-detail:hover {
  background: #0056b3;
}

/* 로딩 애니메이션 */
.spinner {
  width: 50px; height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #0072FF;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes popIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

/* 모바일 대응 */
@media (max-width: 768px) {
  .modal-content { flex-direction: column; max-height: 90vh; overflow-y: auto; }
  .modal-poster { width: 100%; height: 300px; }
  .modal-info { width: 100%; padding: 20px; }
}
</style>