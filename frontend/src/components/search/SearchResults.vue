<template>
  <div class="movie-grid">
    <div 
      v-for="movie in movies" 
      :key="movie.tmdb_id" 
      class="movie-card" 
      @click="goToDetail(movie.tmdb_id)"
    >
      <div class="poster-wrapper">
        <img 
          v-if="movie.poster_path"
          :src="getPosterUrl(movie.poster_path)" 
          :alt="movie.title" 
          class="poster-img"
          loading="lazy"
        />
        <div v-else class="no-poster">
          <span>이미지 없음</span>
        </div>
        
        <div class="poster-overlay"></div>
      </div>

      <div class="movie-info">
        <h3 class="title">{{ movie.title }}</h3>
        
        <div class="meta">
          <span class="year" v-if="movie.release_date">
            {{ movie.release_date.split('-')[0] }} · 
          </span>
          <span class="rating">
            <span class="star">★</span> 
            {{ movie.vote_average ? (movie.vote_average / 2).toFixed(1) : '0.0' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  movies: {
    type: Array,
    required: true
  }
});

const router = useRouter();

const getPosterUrl = (path) => {
  if (!path) return ''; 
  // 만약 API에서 전체 URL을 주는 경우가 있다면 처리, 아니면 기본 경로 붙이기
  if (path.startsWith('http')) return path;
  return `https://image.tmdb.org/t/p/w500${path}`;
};

const goToDetail = (id) => {
  router.push({ name: 'MovieDetailView', params: { movieId: id } });
};
</script>

<style scoped>
/* 그리드 레이아웃 (MovieListView와 통일) */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 3rem 1.5rem; /* 세로 3rem, 가로 1.5rem */
}

/* 카드 스타일 */
.movie-card {
  width: 100%;
  position: relative;
  padding-bottom: 20px; /* 하단 여백 확보 */
  cursor: pointer; /* 클릭 가능 표시 */
}

/* 포스터 래퍼 */
.poster-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 2 / 3; /* 비율 고정 */
  border-radius: 8px;
  overflow: hidden;
  background-color: #F0F0F0;
  border: 1px solid #EAEAEA;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  transition: box-shadow 0.3s ease;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.no-poster {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #AAA;
  font-size: 0.8rem;
  background-color: #EEE;
}

/* 호버 오버레이 */
.poster-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0);
  transition: background 0.3s ease;
  pointer-events: none;
}

/* 정보 영역 */
.movie-info {
  margin-top: 8px;
}

.title {
  font-size: 1rem;
  font-weight: 700;
  color: #222;
  margin: 0 0 4px 0;
  line-height: 1.3;
  
  /* 2줄 말줄임표 처리 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  height: 2.6em; /* 레이아웃 틀어짐 방지용 높이 확보 */
}

.meta {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  color: #888;
}

.rating {
  display: flex;
  align-items: center;
  gap: 3px;
  color: #555;
  font-weight: 600;
}

.star {
  color: #FFC107;
  font-size: 0.9rem;
  padding-bottom: 2px;
}

.year {
  margin-left: 4px;
  color: #999;
  font-weight: 400;
}

/* 호버 효과 (MovieListItem과 동일) */
.movie-card:hover .poster-wrapper {
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.movie-card:hover .poster-img {
  transform: scale(1.05);
}

.movie-card:hover .poster-overlay {
  background: rgba(0, 0, 0, 0.05);
}

.movie-card:hover .title {
  color: #7A6CFA;
}

/* 반응형 */
@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem 12px;
  }
}
</style>