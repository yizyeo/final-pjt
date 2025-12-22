<template>
  <div>
    <a href="#">Carousel</a>
    <div v-if="backdrops.length > 0">
      <h3>Movies:</h3>
      <div v-for="movie in backdrops" :key="movie.tmdb_id">
        <p>Movie: {{ movie.title }}</p>
        <div>
          <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: movie.tmdb_id } }">
            <img :src="`https://image.tmdb.org/t/p/original${movie.backdrop_paths[0]}`" alt="Backdrop" style="width: 300px; cursor: pointer;">
          </RouterLink>
        </div>
        <hr>
      </div>
    </div>
    <hr>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL
const backdrops = ref([])

// carousel 불러오기
const carousel_backdrop = function() {
  axios.get(`${API_URL}/movies/backdrops/`)
  .then((res) => {
    backdrops.value = res.data.slice(0, 10)
    console.log('Backdrops fetched:', backdrops.value)
  })
  .catch((err) => {
    console.log('Error fetching backdrops:', err)
  })
}

onMounted(() => {
  carousel_backdrop()
})
</script>

<style scoped>
</style>
