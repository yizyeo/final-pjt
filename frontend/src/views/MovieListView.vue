<template>
  <div class="movie-list-view">
    <h1>영화 목록</h1>
    <hr>
    <MovieListFilter />

    <div class="movie-grid">
      <div 
        v-for="movie in movies" 
        :key="movie.tmdb_id" 
        class="movie-item"
      >
        <MovieListItem :movie="movie" />
      </div>
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

const getMovies = function () {
  axios({
    method: 'get',
    url: `${API_URL}/movies/movielist/`
  })
    .then(res => {
      movies.value = res.data
    })
    .catch(err => {
      console.log(err)
    })
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
