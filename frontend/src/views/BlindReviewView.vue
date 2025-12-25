<template>
  <div class="blind-container" :class="{ 'is-revealed': isRevealed }">
    
    <div class="section-intro">
      <div class="icon-wrapper">🔮</div>
      <h2 class="intro-title">Blind Pick</h2>
      <p class="intro-desc">
        오직 텍스트가 주는 울림을 믿으세요.<br class="mobile-break" />
        단 한 번의 선택이 당신의 인생 영화를 찾아줍니다.
      </p>
    </div>

    <div v-if="loading" class="status-container">
      <div class="spinner"></div>
      <p>운명의 리뷰들을 수집하고 있습니다...</p>
    </div>

    <div v-else-if="reviews.length === 0" class="status-container">
      <div class="empty-icon">📭</div>
      <p>지금은 도착한 리뷰가 없습니다.</p>
      <button class="action-btn outline" @click="goHome">
        홈으로 돌아가기
      </button>
    </div>

    <div v-else class="review-grid">
      <div 
        v-for="(review, index) in reviews" 
        :key="review.id" 
        class="review-card"
        :style="{ animationDelay: `${Math.random() * 2}s` }" 
        @click="selectReview(review)"
      >
        <div class="card-content">
          <span class="quote-mark">❝</span>
          <p class="review-text">{{ truncateText(review.content, 80) }}</p>
          <div class="card-footer">
            <span class="click-guide">Click to Pick</span>
          </div>
        </div>
      </div>
    </div>

    <Transition name="reveal">
      <div v-if="selectedReview" class="reveal-backdrop">
        <div class="reveal-card">
          <div class="card-header">
            <span class="match-badge">✨ DESTINY MATCH ✨</span>
          </div>
          
          <div class="content-wrapper">
            <div class="poster-section">
              <img 
                :src="getPosterUrl(selectedReview.movie_poster)" 
                alt="Movie Poster" 
                class="poster-img"
              />
            </div>

            <div class="info-section">
              <h3 class="movie-title">{{ selectedReview.movie_title }}</h3>
              
              <div class="meta-info">
                <span class="date">
                  {{ movieStore.movieDetail ? getYear(movieStore.movieDetail.release_date) : 'Loading...' }}
                </span>
                <span class="divider"></span>
                <span class="genres">
                  {{ movieStore.movieDetail ? getGenreNames(movieStore.movieDetail.genres) : '...' }}
                </span>
              </div>

              <div class="review-highlight">
                <span class="icon">✍️</span>
                <p>"{{ selectedReview.content }}"</p>
              </div>

              <div class="action-area">
                <button 
                  class="action-btn outline" 
                  :class="{ active: isWished }"
                  @click="handleToggleWish"
                >
                  {{ isWished ? '✅ 등록 완료' : '➕ 볼 영화 등록' }}
                </button>

                <button class="action-btn primary full-width" @click="goToDetail(selectedReview.movie)">
                  상세 정보 확인하기
                </button>
                
                <button class="action-btn text-only" @click="goHome">
                  홈으로 돌아가기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useMovieStore } from '@/stores/movie'

const router = useRouter()
const accountStore = useAccountStore()
const movieStore = useMovieStore()

const reviews = ref([])
const loading = ref(true)
const selectedReview = ref(null)
const isRevealed = ref(false)
const isWished = ref(false)

const API_URL = import.meta.env.VITE_API_URL

// 데이터 가져오기
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
    alert('리뷰 목록을 불러오지 못했습니다.')
  } finally {
    loading.value = false
  }
}

// [핵심 수정] 리뷰 선택 시 상세 정보 Fetch 추가
const selectReview = async (review) => {
  if (isRevealed.value) return 

  isRevealed.value = true 
  selectedReview.value = review
  document.body.style.overflow = 'hidden'

  // 선택된 영화의 상세 정보(장르, 연도 등)를 스토어로 불러옵니다.
  try {
    // review.movie는 영화 ID입니다.
    await movieStore.fetchMovieDetail(review.movie)
    
    // 상세 정보를 불러온 후, 찜 상태도 동기화
    if (movieStore.movieDetail) {
        isWished.value = movieStore.movieDetail.is_wished
    }
  } catch (err) {
    console.error('상세 정보 로딩 실패', err)
  }
}

// 찜하기 핸들러
const handleToggleWish = async () => {
    if (!selectedReview.value) return
    await movieStore.toggleWish(selectedReview.value.movie)
    isWished.value = !isWished.value
}

// 상세 페이지 이동
const goToDetail = (movieId) => {
  document.body.style.overflow = ''
  router.push({ name: 'MovieDetailView', params: { movieId } })
}

// 홈으로 이동
const goHome = () => {
  document.body.style.overflow = ''
  router.push({ name: 'HomeView' })
}

onUnmounted(() => {
  document.body.style.overflow = ''
})

const getPosterUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : 'https://via.placeholder.com/500x750'
}

const truncateText = (text, length) => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

const getYear = (date) => {
    if (!date) return ''
    return date.split('-')[0]
}

const getGenreNames = (genres) => {
    if (!genres || genres.length === 0) return '장르 정보 없음'
    
    // 상세 조회 API의 장르 데이터는 보통 객체 배열입니다.
    if (typeof genres[0] === 'object') {
        return genres.map(g => g.name_kr || g.name).join(' · ')
    }
    return genres.join(' · ')
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
/* 전체 컨테이너 */
.blind-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 80vh;
  transition: filter 0.5s ease;
}

/* 선택 완료 시 배경 흐림 처리 */
.blind-container.is-revealed .section-intro,
.blind-container.is-revealed .review-grid {
  filter: blur(5px) grayscale(50%);
  pointer-events: none; 
}

/* --- 헤더 --- */
.section-intro {
  text-align: center;
  margin-bottom: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.5s ease;
}

.icon-wrapper {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: floatIcon 3s ease-in-out infinite;
}

@keyframes floatIcon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.intro-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #111111;
  margin-bottom: 0.8rem;
  letter-spacing: -0.03em;
}

.intro-desc {
  font-size: 1.1rem;
  color: #666666;
  line-height: 1.6;
}

/* --- 리뷰 그리드 --- */
.review-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
  perspective: 1000px;
}

@keyframes floatCard {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
  100% { transform: translateY(0px); }
}

.review-card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  cursor: pointer;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 260px;
  position: relative;
  transition: all 0.3s ease;
  animation: floatCard 4s ease-in-out infinite;
}

.review-card:hover {
  animation-play-state: paused;
  transform: scale(1.05) translateY(-10px);
  box-shadow: 0 20px 40px rgba(122, 108, 250, 0.2);
  border-color: #7A6CFA;
  z-index: 10;
}

.card-content {
  text-align: center;
  width: 100%;
}

.quote-mark {
  font-size: 3rem;
  color: #7A6CFA;
  opacity: 0.3;
  display: block;
  margin-bottom: 1rem;
  font-family: serif;
  line-height: 1;
}

.review-text {
  font-size: 1.15rem;
  font-weight: 600;
  color: #333;
  line-height: 1.6;
  margin-bottom: 2rem;
  word-break: keep-all;
}

.click-guide {
  font-size: 0.8rem;
  color: #aaa;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s;
  display: block;
}

.review-card:hover .click-guide {
  opacity: 1;
  transform: translateY(0);
  color: #7A6CFA;
}

/* --- 결과 공개 (운명의 카드) --- */
.reveal-enter-active,
.reveal-leave-active {
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.reveal-enter-from,
.reveal-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(50px);
}

.reveal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.4); 
}

.reveal-card {
  background: white;
  width: 100%;
  max-width: 850px;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 50px 100px -20px rgba(122, 108, 250, 0.5);
  display: flex;
  flex-direction: column;
  position: relative;
  border: 4px solid #fff;
  background-clip: padding-box;
}

.reveal-card::after {
  content: '';
  position: absolute;
  top: -4px; bottom: -4px;
  left: -4px; right: -4px;
  background: linear-gradient(135deg, #7A6CFA, #FF7EB3);
  z-index: -1;
  border-radius: 32px;
}

.card-header {
  background: #F8F7FF;
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.match-badge {
  color: #7A6CFA;
  font-weight: 900;
  letter-spacing: 0.2em;
  font-size: 0.9rem;
}

.content-wrapper {
  display: flex;
}

.poster-section {
  width: 40%;
  background: #000;
  position: relative;
  overflow: hidden;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.info-section {
  width: 60%;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}

.movie-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.date {
  color: #555;
  font-weight: 600;
}

.divider {
  width: 1px;
  height: 12px;
  background-color: #ddd;
}

.genres {
  color: #7A6CFA;
  font-weight: 700;
}

.review-highlight {
  background-color: #F8F7FF;
  padding: 1.5rem;
  border-radius: 16px;
  border-left: 5px solid #7A6CFA;
  margin-bottom: 2.5rem;
  position: relative;
}

.review-highlight .icon {
  position: absolute;
  top: -15px; left: 15px;
  font-size: 1.5rem;
}

.review-highlight p {
  font-size: 1.1rem;
  color: #555;
  font-weight: 600;
  line-height: 1.6;
  font-style: italic;
}

.action-area {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.action-btn.primary {
  background-color: #7A6CFA;
  color: white;
  box-shadow: 0 4px 15px rgba(122, 108, 250, 0.4);
}

.action-btn.primary:hover {
  background-color: #695AE0;
  transform: translateY(-2px);
}

.action-btn.outline {
  background-color: white;
  border: 1px solid #ddd;
  color: #666;
}

.action-btn.outline:hover {
  border-color: #7A6CFA;
  color: #7A6CFA;
  background-color: #F8F7FF;
}

.action-btn.outline.active {
  background-color: #F0FFF4;
  border-color: #48BB78;
  color: #2F855A;
}

.action-btn.text-only {
  background: none;
  color: #999;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.action-btn.text-only:hover {
  color: #555;
  text-decoration: underline;
}

.status-container {
  text-align: center;
  padding: 4rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.status-container p { color: #888; font-size: 1.1rem; }

.spinner {
  width: 50px; height: 50px;
  border: 4px solid #F3F0FF;
  border-top: 4px solid #7A6CFA;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .content-wrapper { flex-direction: column; }
  .poster-section { width: 100%; height: 300px; }
  .info-section { width: 100%; padding: 2rem 1.5rem; }
  .movie-title { font-size: 1.8rem; }
  .review-grid { grid-template-columns: 1fr; }
}
</style>