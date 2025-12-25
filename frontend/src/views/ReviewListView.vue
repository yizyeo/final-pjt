<template>
  <div class="review-list-page">
    
    <div class="section-intro">
      <div class="icon-wrapper">💬</div>
      <h2 class="intro-title">리뷰 피드</h2>
      <p class="intro-desc">
        다양한 영화에 대한 솔직한 감상평을 확인하고<br class="mobile-break" />
        자유롭게 이야기를 나눠보세요.
      </p>
    </div>

    <div class="control-bar">
      <div class="total-count">
        전체 <strong>{{ reviewStore.totalReviews.length }}</strong>개의 리뷰
      </div>
      <div class="filter-wrapper">
        <ReviewFilter 
          :currentSort="currentSort" 
          @change-sort="changeSort" 
        />
      </div>
    </div>

    <div v-if="reviewStore.loading" class="skeleton-grid">
      <div class="skeleton-card" v-for="n in 5" :key="n"></div>
    </div>

    <div v-else-if="reviewStore.totalReviews.length > 0" class="review-grid">
      <div 
        v-for="review in displayedReviews" 
        :key="review.id"
        class="review-card-wrapper"
      >
        <ReviewCard 
          :review="review"
          @go-movie="goMovieDetail"
          @go-detail="goDetail"
          @go-profile="goProfile" 
          @like="reviewStore.likeReview"
        />
      </div>
    </div>

    <div v-if="hasMore" class="load-more-container">
      <button @click="loadMore" class="load-more-btn">
        더보기 <span class="arrow">∨</span>
      </button>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">📝</div>
      <p>아직 작성된 리뷰가 없습니다.<br>첫 번째 리뷰의 주인공이 되어보세요!</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'

import ReviewFilter from '@/components/review/ReviewFilter.vue'
import ReviewCard from '@/components/review/ReviewCard.vue'

const reviewStore = useReviewStore()
const router = useRouter()
const currentSort = ref('popular')

const limit = ref(20) // 처음에 보여줄 개수
const step = 20

const displayedReviews = computed(() => {
  return reviewStore.totalReviews.slice(0, limit.value)
})

const hasMore = computed(() => {
  return limit.value < reviewStore.totalReviews.length
})

const loadMore = () => {
  limit.value += step
}

const changeSort = (sort) => {
  currentSort.value = sort
  limit.value = step
  reviewStore.fetchTotalReviews(sort)
}

const goMovieDetail = (movie) => {
  const movieId = (typeof movie === 'object') ? (movie.tmdb_id || movie.id) : movie
  router.push({ name: 'MovieDetailView', params: { movieId: movieId } })
}

const goDetail = (reviewPk) => {
  router.push({ name: 'ReviewDetailView', params: { reviewId: reviewPk } })
}

const goProfile = (username) => {
  router.push({ name: 'ProfileView', params: { username: username } })
}

onMounted(() => {
  reviewStore.fetchTotalReviews(currentSort.value)
})
</script>

<style scoped>
.review-list-page {
  width: 100%;
  max-width: 900px; 
  margin: 0 auto;
  padding: 3rem 1.5rem;
}

/* [수정] 헤더 스타일 통일 (BlindReviewView와 동일) */
.section-intro {
  text-align: center;
  margin-bottom: 4rem; /* 여백 넉넉하게 */
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.5s ease;
}

.icon-wrapper {
  font-size: 3rem;
  margin-bottom: 1rem;
  /* 둥둥 떠다니는 애니메이션 적용 */
  animation: floatIcon 3s ease-in-out infinite;
}

@keyframes floatIcon {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.intro-title {
  font-size: 2.2rem; /* 폰트 사이즈 키움 */
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

/* 컨트롤 바 */
.control-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #EEEEEE;
}

.total-count {
  font-size: 1rem;
  color: #555555;
}

.total-count strong {
  color: #7A6CFA;
  font-weight: 700;
}

.filter-wrapper {
  min-width: 120px;
}

/* 리뷰 그리드: 1열 */
.review-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

/* 카드 래퍼 */
.review-card-wrapper {
  background-color: #FFFFFF;
  border: 1px solid #EEEEEE;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  
  height: auto; 
  min-height: 180px;
}

.review-card-wrapper:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(122, 108, 250, 0.15);
  border-color: #7A6CFA;
  background-color: #FBFAFF;
}

/* 스켈레톤 로딩 */
.skeleton-grid {
  display: grid;
  grid-template-columns: 1fr;
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

.load-more-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.load-more-btn {
  width: 100%;
  max-width: 400px;
  padding: 12px 0;
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  color: #555;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.load-more-btn:hover {
  background-color: #F8F9FA;
  border-color: #CCC;
  color: #333;
}

.arrow { font-size: 0.8rem; font-weight: bold; }

/* 데이터 없음 */
.empty-state {
  text-align: center;
  padding: 6rem 0;
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
  /* [참고] 다른 뷰들과 통일성을 위해 폰트 사이즈를 강제로 줄이지 않음 (원하면 수정 가능) */
  
  .control-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .filter-wrapper {
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
}
</style>