<template>
  <div class="movie-card">
    <RouterLink 
      :to="{ name: 'MovieDetailView', params: { movieId: movie.tmdb_id } }"
      class="movie-link"
    >
      <div class="poster-wrapper">
        <img 
          v-if="movie.poster_path"
          :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" 
          :alt="movie.title"
          class="poster-img"
          loading="lazy"
        >
        <div v-else class="no-poster">
          <span>이미지 없음</span>
        </div>
        <div class="poster-overlay"></div>
      </div>

      <div class="movie-info">
        <h3 class="title">{{ movie.title }}</h3>
        <div class="meta">
          <span class="rating">
            <span class="star">⭐</span> 
            {{ movie.vote_average ? (movie.vote_average / 2).toFixed(1) : '0.0' }}
          </span>
          </div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  movie: Object
})
</script>

<style scoped>
.movie-card {
  width: 100%;
  position: relative;
  /* [핵심] 카드 자체 하단에 여백을 주어 다음 행과의 간격을 넓힘 */
  padding-bottom: 20px; 
}

.movie-link {
  text-decoration: none;
  display: block;
  color: inherit;
  transition: transform 0.2s ease;
}

/* 포스터 스타일 */
.poster-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 2 / 3; 
  border-radius: 8px;
  overflow: hidden;
  background-color: #F0F0F0;
  border: 1px solid #EAEAEA;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.no-poster {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: #AAA; font-size: 0.8rem; background-color: #EEE;
}

.poster-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0);
  transition: background 0.3s ease;
  pointer-events: none;
}

/* [수정] 정보 텍스트 스타일 (간격 좁게 유지) */
.movie-info {
  margin-top: 8px; /* 원래대로 8px 유지 */
}

.title {
  font-size: 1rem;
  font-weight: 700;
  color: #222;
  margin: 0 0 4px 0; /* 제목 아래 간격을 좁게 설정 */
  line-height: 1.3;
  
  /* 긴 제목 말줄임표 처리 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  color: #666;
}

.rating {
  display: flex;
  align-items: center;
  gap: 3px;
  font-weight: 600;
}

.star {
  color: #FFC107;
  font-size: 0.9rem;
  padding-bottom: 2px;
}

/* 호버 효과 */
.movie-link:hover .poster-wrapper {
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
.movie-link:hover .poster-img {
  transform: scale(1.05);
}
.movie-link:hover .poster-overlay {
  background: rgba(0, 0, 0, 0.05);
}
.movie-link:hover .title {
  color: #7A6CFA;
}
</style>