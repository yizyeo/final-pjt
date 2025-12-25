<template>
  <div class="carousel-container">
    <swiper
      v-if="backdrops.length > 0"
      :modules="modules"
      :slides-per-view="1"
      :space-between="0"
      :loop="true"
      :autoplay="{ delay: 5000, disableOnInteraction: false }"
      :pagination="{ clickable: true }"
      :navigation="{
        prevEl: prevBtn,
        nextEl: nextBtn
      }"
      class="my-swiper"
      @swiper="onSwiper"
    >
      <swiper-slide v-for="movie in backdrops" :key="movie.tmdb_id">
        <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: movie.tmdb_id } }" class="slide-link">
          <div 
            class="slide-content"
            :style="{ backgroundImage: `url(https://image.tmdb.org/t/p/original${movie.backdrop_paths[0]})` }"
          >
            <div class="gradient-overlay">
              <div class="movie-info">
                <h2 class="movie-title">{{ movie.title }}</h2>
                <p class="movie-meta">
                  <span class="year">{{ movie.release_date?.split('-')[0] }}</span>
                </p>
              </div>
            </div>
          </div>
        </RouterLink>
      </swiper-slide>

      <div ref="prevBtn" class="swiper-button-prev"></div>
      <div ref="nextBtn" class="swiper-button-next"></div>
      <div class="swiper-pagination"></div>
    </swiper>

    <div v-else class="loading-skeleton"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination, Navigation } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'

const API_URL = import.meta.env.VITE_API_URL
const backdrops = ref([])
const modules = [Autoplay, Pagination, Navigation]

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

const carousel_backdrop = function() {
  axios.get(`${API_URL}/movies/backdrops/`)
  .then((res) => {
    backdrops.value = res.data.slice(0, 10)
  })
  .catch((err) => {
    console.error('Error fetching backdrops:', err)
  })
}

onMounted(() => {
  carousel_backdrop()
})
</script>

<style scoped>
/* 컨테이너 */
.carousel-container {
  width: 100%;
  position: relative;
  border-radius: 12px; 
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

/* Swiper 높이 */
.my-swiper {
  width: 100%;
  height: 600px;
  position: relative; /* 버튼 위치 기준 */
}

.slide-link {
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none;
}

.slide-content {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
}

/* 그라데이션 */
.gradient-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50%; 
  background: linear-gradient(to top, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0) 100%);
  display: flex;
  align-items: flex-end; 
  padding: 2.5rem 3rem; 
}

/* 텍스트 스타일 */
.movie-info {
  color: white;
  width: 100%;
  text-shadow: none; 
}

.movie-title {
  font-size: 2.2rem; 
  font-weight: 700; 
  margin-bottom: 0.5rem;
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.movie-meta {
  font-size: 1rem;
  font-weight: 400; 
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.year {
  letter-spacing: -0.02em;
}

/* [수정] 네비게이션 버튼 (화살표) */
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
  
  /* [핵심] Z-Index를 높여서 링크보다 위에 배치 & 클릭 가능하게 설정 */
  z-index: 50 !important;
  cursor: pointer;
}

:deep(.swiper-button-prev::after),
:deep(.swiper-button-next::after) {
  font-size: 1.2rem;
  font-weight: bold;
}

.carousel-container:hover :deep(.swiper-button-prev),
.carousel-container:hover :deep(.swiper-button-next) {
  opacity: 1;
}

/* 버튼 호버 시 조금 더 잘 보이게 */
:deep(.swiper-button-prev):hover,
:deep(.swiper-button-next):hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 페이지네이션 (하단 점) */
:deep(.swiper-pagination-bullet) {
  background: white;
  opacity: 0.3;
  width: 8px;
  height: 8px;
  margin: 0 5px !important;
}

:deep(.swiper-pagination-bullet-active) {
  background: white;
  opacity: 1;
  width: 8px; 
}

/* 로딩 스켈레톤 */
.loading-skeleton {
  width: 100%;
  height: 600px;
  background-color: #f0f0f0;
  border-radius: 12px;
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .my-swiper {
    height: 400px;
  }
  
  .gradient-overlay {
    padding: 1.5rem;
  }
  
  .movie-title {
    font-size: 1.6rem;
  }
  
  :deep(.swiper-button-prev),
  :deep(.swiper-button-next) {
    display: none;
  }
}
</style>