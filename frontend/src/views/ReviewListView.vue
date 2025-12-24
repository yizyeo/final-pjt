<template>
  <div class="review-list-page">
    
    <div class="page-header">
      <h2 class="page-title">커뮤니티 리뷰 피드 💬</h2>
      <p class="page-desc">
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
        v-for="review in reviewStore.totalReviews" 
        :key="review.id"
        class="review-card-wrapper"
      >
        <ReviewCard 
          :review="review"
          @go-movie="goMovieDetail"
          @go-detail="goDetail"
          @like="reviewStore.likeReview"
        />
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">📝</div>
      <p>아직 작성된 리뷰가 없습니다.<br>첫 번째 리뷰의 주인공이 되어보세요!</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'

import ReviewFilter from '@/components/review/ReviewFilter.vue'
import ReviewCard from '@/components/review/ReviewCard.vue'

const reviewStore = useReviewStore()
const router = useRouter()
const currentSort = ref('popular')

const changeSort = (sort) => {
  currentSort.value = sort
  reviewStore.fetchTotalReviews(sort)
}

const goMovieDetail = (movie) => {
  const movieId = (typeof movie === 'object') ? (movie.tmdb_id || movie.id) : movie
  router.push({ name: 'MovieDetailView', params: { movieId: movieId } })
}

const goDetail = (reviewPk) => {
  router.push({ name: 'ReviewDetailView', params: { reviewId: reviewPk } })
}

onMounted(() => {
  reviewStore.fetchTotalReviews(currentSort.value)
})
</script>

<style scoped>
.review-list-page {
  width: 100%;
  /* [수정] 1열 피드형 디자인이므로 너무 넓으면 가독성이 떨어질 수 있어 최대 폭을 조금 줄임 (선택사항) */
  max-width: 900px; 
  margin: 0 auto;
  padding: 3rem 1.5rem;
}

/* 헤더 */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111111;
  margin-bottom: 0.8rem;
  letter-spacing: -0.03em;
}

.page-desc {
  font-size: 1.1rem;
  color: #666666;
  line-height: 1.6;
  font-weight: 500;
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

/* [핵심 수정] 리뷰 그리드: 무조건 1열(1fr) */
.review-grid {
  display: grid;
  grid-template-columns: 1fr; /* PC에서도 1개씩 */
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
  
  /* 높이 유연하게 */
  height: auto; 
  min-height: 180px;
}

.review-card-wrapper:hover {
  transform: translateY(-3px); /* 1열일 때는 살짝만 움직이는 게 더 고급스러움 */
  box-shadow: 0 12px 24px rgba(122, 108, 250, 0.15);
  border-color: #7A6CFA;
  background-color: #FBFAFF;
}

/* 스켈레톤 로딩 (1열) */
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
  .page-title {
    font-size: 1.5rem;
  }
  
  .page-desc {
    font-size: 1rem;
  }

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
  
  .mobile-break {
    display: none;
  }
}
</style>