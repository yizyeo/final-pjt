<template>
  <div class="home-view">
    
    <section class="hero-section">
      <HomeMainCarousel />
    </section>

    <div class="content-wrapper">
      
      <section class="action-section">
        <HomeActionButtons />
      </section>
      
      <div class="spacer"></div>

      <section class="movie-section">
        <HomeHotMovies />
      </section>

      <div class="spacer"></div>

      <section class="review-section">
        <HomeHotReviews />
      </section>
      
    </div>
  </div>
</template>

<script setup>
import HomeMainCarousel from '@/components/home/HomeMainCarousel.vue'
import HomeActionButtons from '@/components/home/HomeActionButtons.vue'
import HomeHotMovies from '@/components/home/HomeHotMovies.vue'
import HomeHotReviews from '@/components/home/HomeHotReviews.vue'
</script>

<style scoped>
/* HomeView.vue - style scoped */

/* 전체 페이지 배경 */
.home-view {
  width: 100%;
  min-height: 100vh;
  background-color: #FFFFFF;
  padding-bottom: 5rem;
}

/* [수정] 중앙 정렬을 위한 공통 래퍼 (Mixin 개념) */
.content-wrapper {
  max-width: 1080px; /* NavBar와 동일하게 맞춤 */
  margin: 0 auto;    /* 중앙 정렬 */
  padding: 0 1.5rem; /* 모바일 대응을 위한 최소 여백 */
  width: 100%;
}

/* 1. 히어로 섹션 (캐러셀) */
.hero-section {
  width: 100%;
  margin-bottom: 3rem;
  /* 캐러셀도 너비를 제한해서 너무 길어지지 않게 함 */
  max-width: 1080px; 
  margin-left: auto;
  margin-right: auto;
  padding: 0 1.5rem; /* 패딩 추가하여 라인 맞춤 */
}

/* 2. 액션 버튼 섹션 */
.action-section {
  margin-bottom: 2rem;
}

/* 3. 섹션 공통 스타일 */
.movie-section, .review-section {
  position: relative;
}

/* 섹션 헤더 (제목 + 더보기) */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 1.5rem;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111111;
  letter-spacing: -0.02em;
}

.more-link {
  font-size: 0.9rem;
  font-weight: 500;
  color: #888888;
  transition: color 0.2s;
}

.more-link:hover {
  color: #7A6CFA;
}

/* 섹션 간 간격 */
.spacer {
  height: 4rem;
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .hero-section {
    padding: 0 1rem;
    margin-bottom: 2rem;
  }
  
  .content-wrapper {
    padding: 0 1rem;
  }
  
  .title {
    font-size: 1.25rem;
  }
  
  .spacer {
    height: 3rem;
  }
}
</style>