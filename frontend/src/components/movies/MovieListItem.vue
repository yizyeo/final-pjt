<template>
  <div class="movie-card">
    <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: movie.tmdb_id } }">
      <img 
        :src="'https://image.tmdb.org/t/p/w300' + movie.poster_path" 
        :alt="movie.title"
        class="poster-img"
      >
    </RouterLink>
    <div class="movie-info">
      <strong>{{ movie.title }}</strong>
      <p>평점: {{ movie.vote_average?.toFixed(1) }}</p>
    </div>
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
  padding: 10px;
}

.poster-img {
  width: 100%;
}

.movie-info {
  margin-top: 8px;
}
</style>
