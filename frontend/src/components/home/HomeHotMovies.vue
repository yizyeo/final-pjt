<template>
  <div class="hot-movies-container">
    <div class="section-intro">
      <h2 class="intro-title">지금 가장 핫한 영화</h2>
      <p class="intro-desc">
        실시간으로 사랑받는 인기작을 확인하고<br class="mobile-break" /> 
        트렌드를 놓치지 마세요.
      </p>
      <RouterLink :to="{ name: 'MovieListView' }" class="more-link">
        전체보기 <span class="arrow">→</span>
      </RouterLink>
    </div>

    <swiper
      v-if="hotMovies.length > 0"
      :modules="modules"
      :slides-per-view="2" 
      :space-between="16"
      :navigation="{
        prevEl: prevBtn,
        nextEl: nextBtn
      }"
      :breakpoints="{
        '640': { slidesPerView: 3, spaceBetween: 20 },
        '768': { slidesPerView: 4, spaceBetween: 24 },
        '1024': { slidesPerView: 5, spaceBetween: 24 },
      }"
      class="movie-swiper"
      @swiper="onSwiper"
    >
      <swiper-slide v-for="(movie, index) in hotMovies" :key="movie.tmdb_id">
        <RouterLink 
          :to="{ name: 'MovieDetailView', params: { movieId: movie.tmdb_id } }"
          class="movie-card"
        >
          <div class="poster-wrapper">
            <img 
              :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
              :alt="movie.title"
              class="poster-img"
              loading="lazy"
            >
            <div class="rank-badge">{{ index + 1 }}</div>
            <div class="overlay"></div>
          </div>

          <div class="movie-info">
            <h3 class="movie-title">{{ movie.title }}</h3>
            <div class="movie-meta">
              <span class="rating">⭐ {{ movie.vote_average ? movie.vote_average.toFixed(1) : '0.0' }}</span>
              <span class="year" v-if="movie.release_date">・ {{ movie.release_date.split('-')[0] }}</span>
            </div>
          </div>
        </RouterLink>
      </swiper-slide>

      <div ref="prevBtn" class="swiper-button-prev"></div>
      <div ref="nextBtn" class="swiper-button-next"></div>
    </swiper>

    <div v-else class="skeleton-container">
      <div class="skeleton-card" v-for="n in 5" :key="n"></div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/navigation'

const API_URL = import.meta.env.VITE_API_URL
const hotMovies = ref([])
const modules = [Navigation]

const prevBtn = ref(null)
const nextBtn = ref(null)

const onSwiper = (swiper) => {
  nextTick(() => {
    swiper.params.navigation.prevEl = prevBtn.value
    swiper.params.navigation.nextEl = nextBtn.value
    swiper.navigation.destroy()
    swiper.navigation.init()
    swiper.navigation.update()
  })
}

const fetchHotMovies = () => {
  axios.get(`${API_URL}/movies/hot/`)
    .then((res) => {
      hotMovies.value = res.data
    })
    .catch((err) => {
      console.log('Error fetching hot movies:', err)
    })
}

onMounted(() => {
  fetchHotMovies()
})
</script>

<style scoped>
.hot-movies-container {
  width: 100%;
  position: relative;
}

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
  
  /* [수정] 설명글과 아래 링크 사이의 간격을 1.2rem -> 2.5rem으로 대폭 확대 */
  margin-bottom: 2.5rem; 
}

/* [추가] 더보기 링크 스타일 */
.more-link {
  font-size: 0.95rem;
  font-weight: 600;
  color: #7A6CFA; 
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: opacity 0.2s;
  
  /* 링크 자체에도 살짝의 패딩을 줘서 클릭 영역 확보 */
  padding: 0.5rem 1rem;
  background-color: #F9F9FF; /* 아주 연한 배경 추가 (선택사항) */
  border-radius: 20px;
}

.more-link:hover {
  opacity: 0.8;
  background-color: #F0F0FF; /* 호버 시 배경 조금 더 진하게 */
  text-decoration: none; /* 밑줄 대신 배경색으로 피드백 */
}

.arrow {
  font-size: 1.1rem;
  margin-top: -2px; /* 화살표 높이 미세 조정 */
}

.movie-swiper {
  padding: 10px 4px;
  position: relative;
}

/* 개별 영화 카드 */
.movie-card {
  display: block;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-8px);
}

/* 포스터 래퍼 */
.poster-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 2 / 3;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 12px;
  background-color: #f0f0f0;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.rank-badge {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  border-top-right-radius: 12px;
  color: white;
  font-size: 1.2rem;
  font-weight: 800;
  font-style: italic;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 2px -2px 10px rgba(0,0,0,0.1);
  z-index: 2;
  transition: background-color 0.3s ease; 
}

.movie-card:hover .rank-badge {
  background-color: rgba(122, 108, 250, 0.85); 
}

/* 정보 영역 */
.movie-info {
  padding: 0 4px;
}

.movie-title {
  font-size: 1rem;
  font-weight: 700;
  color: #111111;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.movie-meta {
  font-size: 0.85rem;
  color: #888888;
  display: flex;
  align-items: center;
}

.rating {
  font-weight: 600;
  color: #333333;
}

:deep(.swiper-button-prev),
:deep(.swiper-button-next) {
  color: white;
  width: 44px;
  height: 44px;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(2px);
  border-radius: 50%;
  transition: all 0.3s ease;
  opacity: 0; 
  
  z-index: 50 !important;
  cursor: pointer;
}

:deep(.swiper-button-prev::after),
:deep(.swiper-button-next::after) {
  font-size: 1.2rem; 
  font-weight: bold;
}

/* 컨테이너 호버 시 버튼 등장 */
.hot-movies-container:hover :deep(.swiper-button-prev),
.hot-movies-container:hover :deep(.swiper-button-next) {
  opacity: 1; 
}

/* 버튼 호버 시 조금 더 잘 보이게 */
:deep(.swiper-button-prev):hover,
:deep(.swiper-button-next):hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 비활성화된 버튼 */
:deep(.swiper-button-disabled) {
  opacity: 0 !important;
  pointer-events: none;
}

/* 스켈레톤 로딩 */
.skeleton-container {
  display: flex;
  gap: 20px;
  overflow: hidden;
}

.skeleton-card {
  min-width: 200px;
  height: 300px;
  background-color: #f5f5f5;
  border-radius: 12px;
}
</style>