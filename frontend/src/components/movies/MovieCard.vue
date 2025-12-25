<template>
  <div class="movie-card h-100" @click="goToDetail">
    <div class="card bg-transparent border-0 h-100">
      <div class="poster-wrapper">
        <img 
          :src="posterUrl" 
          :alt="movie.title" 
          class="card-img-top rounded-3"
          @error="handleImageError"
        >
        <div class="rating-badge">
          ⭐ {{ movie.vote_average?.toFixed(1) }}
        </div>
      </div>
      
      <div class="card-body px-1 py-2">
        <h6 class="card-title text-white text-truncate mb-0">
          {{ movie.title }}
        </h6>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  movie: {
    type: Object,
    required: true
  }
})

const router = useRouter()

// TMDB 이미지 URL 계산
const posterUrl = computed(() => {
  if (props.movie.poster_path) {
    return `https://image.tmdb.org/t/p/w500${props.movie.poster_path}`
  }
  // 포스터가 없을 때 보여줄 기본 이미지 (대체 이미지 서비스 이용)
  return 'https://via.placeholder.com/500x750?text=No+Poster'
})

// 상세 페이지로 이동
const goToDetail = () => {
  router.push({ 
    name: 'MovieDetailView', 
    params: { movieId: props.movie.tmdb_id } 
  })
}

// 이미지 로드 실패 시 처리
const handleImageError = (e) => {
  e.target.src = 'https://via.placeholder.com/500x750?text=No+Poster'
}
</script>

<style scoped>
.movie-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-10px);
}

.poster-wrapper {
  position: relative;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.rating-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: #ffc107;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  backdrop-filter: blur(4px);
}

.card-title {
  font-size: 0.95rem;
  font-weight: 600;
}
</style>