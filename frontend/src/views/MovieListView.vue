<template>
  <div class="movie-list-view">
    <h1>영화 목록</h1>
    <hr>
    <MovieListFilter @filter-change="onFilterChange" />

    <div class="movie-grid">
      <div 
        v-for="movie in movies" 
        :key="movie.tmdb_id" 
        class="movie-item"
      >
        <MovieListItem :movie="movie" />
      </div>
    </div>

    <div v-if="!isFiltered && movies.length > 0" class="load-more-container">
      <button @click="loadMore" class="load-more-btn">더보기</button>
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
  // 필터가 하나라도 있으면 isFiltered = true
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
.movie-list-view {
  padding: 20px;
}

.movie-grid {
  display: flex; 
  flex-wrap: wrap;
  margin: 0 -10px;
}

.movie-item {
  width: 25%; 
  box-sizing: border-box;
}

.load-more-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding: 10px;
}

.load-more-btn {
  width: 100%;
  max-width: 300px;
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.load-more-btn:hover {
  background-color: #e0e0e0;
}

/* 반응형 처리 */
@media (max-width: 1024px) {
  .movie-item {
    width: 33.3%;
  }
}

@media (max-width: 768px) {
  .movie-item {
    width: 50%;
  }
}

@media (max-width: 480px) {
  .movie-item {
    width: 100%;
  }
}
</style>
