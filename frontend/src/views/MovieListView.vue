<template>
  <div class="page-container">
    
    <div class="page-header">
      <h2 class="page-title">전체 영화 목록 🎬</h2>
      <p class="page-desc">
        다양한 장르와 시대의 영화를 탐색하고<br class="mobile-break" />
        새로운 인생 영화를 발견해보세요.
      </p>
    </div>

    <div class="control-bar">
      <!-- <div class="total-count">
        전체 <strong>{{ movies.length }}</strong>개의 작품
      </div> -->
      <div class="filter-wrapper">
        <MovieListFilter @filter-change="onFilterChange" />
      </div>
    </div>

    <div v-if="movies.length > 0" class="movie-grid">
      <div 
        v-for="movie in movies" 
        :key="movie.tmdb_id" 
        class="movie-card-wrapper"
      >
        <MovieListItem :movie="movie" />
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">🔍</div>
      <p>조건에 맞는 영화를 찾을 수 없습니다.<br>다른 필터로 검색해보세요.</p>
    </div>

    <div v-if="!isFiltered && movies.length > 0" class="load-more-container">
      <button @click="loadMore" class="load-more-btn">
        더보기 <span class="arrow">∨</span>
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import MovieListFilter from '@/components/movies/MovieListFilter.vue'
import MovieListItem from '@/components/movies/MovieListItem.vue'

const API_URL = import.meta.env.VITE_API_URL
const movies = ref([])
const page = ref(1)
const isFiltered = ref(false)
const currentFilters = ref({})

const getMovies = function (filters = {}, isLoadMore = false) {
  const params = {
    page: page.value
  }
  if (filters.genre) params.genre = filters.genre
  if (filters.year) params.year = filters.year

  axios({
    method: 'get',
    url: `${API_URL}/movies/movielist/`,
    params: params
  })
    .then(res => {
      if (isLoadMore) {
        movies.value.push(...res.data)
      } else {
        movies.value = res.data
      }
    })
    .catch(err => {
      console.log(err)
    })
}

const onFilterChange = (filters) => {
  page.value = 1
  currentFilters.value = filters
  isFiltered.value = !!(filters.genre || filters.year)
  getMovies(filters, false)
}

const loadMore = () => {
  page.value += 1
  getMovies(currentFilters.value, true)
}

onMounted(() => {
  getMovies()
})
</script>

<style scoped>
/* 전체 컨테이너 (ReviewListView와 동일) */
.page-container {
  width: 100%;
  max-width: 1080px; /* 영화 목록은 그리드라 조금 더 넓게 */
  margin: 0 auto;
  padding: 3rem 1.5rem;
  background-color: #FFFFFF;
  min-height: 100vh;
}

/* 1. 헤더 스타일 (완벽 통일) */
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

/* 2. 컨트롤 바 (완벽 통일) */
.control-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #EEEEEE;
}

.total-count strong {
  color: #7A6CFA;
  font-weight: 700;
}

.filter-wrapper {
  /* 필터 컴포넌트 크기에 맞게 */
}

/* 3. 영화 그리드 (영화는 포스터 위주라 다열 그리드 유지) */
.movie-grid {
  display: grid;
  /* 반응형: 최소 220px 너비 유지하며 자동 채움 */
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

/* 영화 카드 래퍼 (디자인 통일감 부여) */
.movie-card-wrapper {
  /* 필요하다면 여기에 카드 호버 효과 등을 추가 가능 */
  transition: transform 0.2s;
}

.movie-card-wrapper:hover {
  transform: translateY(-5px);
}

/* 4. 데이터 없음 (Empty State) */
.empty-state {
  text-align: center;
  padding: 6rem 0;
  background-color: #FAFAFA;
  border-radius: 16px;
  color: #888888;
  border: 1px dashed #DDD;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* 5. 더보기 버튼 */
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

/* 반응형 */
@media (max-width: 768px) {
  .page-title { font-size: 1.5rem; }
  .page-desc { font-size: 1rem; }

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
  
  .mobile-break { display: none; }
  
  .movie-grid {
    /* 모바일에서는 2열 그리드 */
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}
</style>