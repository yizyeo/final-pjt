<template>
  <div class="hot-reviews-container">
    
    <div class="section-intro">
      <h2 class="intro-title">화제의 리뷰 💬</h2>
      <p class="intro-desc">
        다른 관객들은 어떻게 봤을까요?<br class="mobile-break" /> 
        생생한 감상평을 확인해보세요.
      </p>
      <a href="#" @click.prevent="goMore" class="more-link">
        전체보기 <span class="arrow">→</span>
      </a>
    </div>

    <div v-if="reviewStore.hotReviews?.length > 0" class="review-grid">
      <div 
        v-for="review in reviewStore.hotReviews.slice(0, 4)" 
        :key="review.id" 
        class="review-card-wrapper"
      >
        <ReviewCard 
          :review="review" 
          @go-movie="goMovie"
          @go-detail="goDetail"
        />
      </div>
    </div>

    <div v-else-if="isLoading" class="skeleton-grid">
      <div class="skeleton-card" v-for="n in 4" :key="n"></div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">📭</div>
      <p>아직 등록된 핫 리뷰가 없어요.</p>
    </div>

  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'
import ReviewCard from '@/components/review/ReviewCard.vue'

const reviewStore = useReviewStore()
const router = useRouter()
const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  await reviewStore.fetchHotReviews()
  setTimeout(() => {
    isLoading.value = false
  }, 300)
})

const goMore = () => {
  router.push({ name: 'ReviewListView' })
}

// [추가] 영화 상세 페이지로 이동
const goMovie = (movie) => {
  // review.movie가 객체일 수도 있고 ID일 수도 있으므로 안전하게 처리
  // (백엔드 데이터 구조에 따라 movie.tmdb_id 혹은 movie.id 확인 필요)
  const movieId = (typeof movie === 'object') ? (movie.tmdb_id || movie.id) : movie
  router.push({ name: 'MovieDetailView', params: { movieId: movieId } })
}

// [추가] 리뷰 상세 페이지로 이동
const goDetail = (reviewId) => {
  router.push({ name: 'ReviewDetailView', params: { reviewId: reviewId } })
}
</script>

<style scoped>
.hot-reviews-container {
  width: 100%;
  padding-top: 2rem;
  padding-bottom: 2rem;
}

/* 섹션 헤더 */
.section-intro {
  text-align: center;
  margin-bottom: 2.5rem;
}

.intro-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111111;
  margin-bottom: 0.8rem;
  letter-spacing: -0.03em;
}

.intro-desc {
  font-size: 1.1rem;
  color: #666666;
  line-height: 1.6;
  font-weight: 500;
  margin-bottom: 2.5rem;
}

.more-link {
  font-size: 0.95rem;
  font-weight: 600;
  color: #7A6CFA;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 0.5rem 1rem;
  background-color: #F9F9FF;
  border-radius: 20px;
  transition: all 0.2s;
}

.more-link:hover {
  background-color: #F0F0FF;
  opacity: 0.8;
}

.arrow {
  font-size: 1.1rem;
  margin-top: -2px;
}

/* 리뷰 그리드 */
.review-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); 
  gap: 1.5rem; 
}

/* 카드 래퍼 */
.review-card-wrapper {
  position: relative;
  background-color: #FFFFFF;
  border: 1px solid #EEEEEE;
  border-radius: 16px;
  padding: 1.5rem; 
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  overflow: hidden;
  height: 100%;
  min-height: 180px; 
}

.review-card-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(122, 108, 250, 0.15);
  border-color: #7A6CFA;
  background-color: #FBFAFF;
}

/* 스켈레톤 로딩 */
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.skeleton-card {
  height: 180px;
  background-color: #f5f5f5;
  border-radius: 16px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* 데이터 없음 */
.empty-state {
  text-align: center;
  padding: 4rem 0;
  background-color: #FAFAFA;
  border-radius: 16px;
  color: #888888;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* 반응형 */
@media (max-width: 768px) {
  .intro-title {
    font-size: 1.5rem;
  }
  
  .intro-desc {
    font-size: 1rem;
  }

  .review-grid, .skeleton-grid {
    grid-template-columns: 1fr;
  }
  
  .mobile-break {
    display: none;
  }
}
</style>