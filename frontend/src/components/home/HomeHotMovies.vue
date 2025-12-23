<template>
  <div class="hot-movies">
    <h3>🔥 Hot Movies</h3>
    
    <div class="slider-container" v-if="hotMovies.length > 0">
      <button class="slider-btn prev" @click="scrollLeft">&lt;</button>
      
      <div class="slider-track" ref="sliderTrack">
        <RouterLink 
          v-for="movie in hotMovies" 
          :key="movie.tmdb_id"
          :to="{ name: 'MovieDetailView', params: { movieId: movie.tmdb_id } }"
          class="movie-card"
        >
          <img 
            :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" 
            :alt="movie.title"
          >
          <p>{{ movie.title }}</p>
        </RouterLink>
      </div>
      
      <button class="slider-btn next" @click="scrollRight">&gt;</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL
const hotMovies = ref([])
const sliderTrack = ref(null)

const fetchHotMovies = () => {
  axios.get(`${API_URL}/movies/hot/`)
    .then((res) => {
      hotMovies.value = res.data
    })
    .catch((err) => {
      console.log('Error:', err)
    })
}

const scrollLeft = () => {
  sliderTrack.value.scrollBy({ left: -300, behavior: 'smooth' })
}

const scrollRight = () => {
  sliderTrack.value.scrollBy({ left: 300, behavior: 'smooth' })
}

onMounted(() => {
  fetchHotMovies()
})
</script>

<style scoped>
.hot-movies {
  padding: 20px;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.slider-track {
  display: flex;
  gap: 15px;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none;
}

.slider-track::-webkit-scrollbar {
  display: none;
}

.movie-card {
  flex-shrink: 0;
  width: 150px;
  text-decoration: none;
  color: white;
}

.movie-card img {
  width: 100%;
  border-radius: 8px;
}

.movie-card p {
  margin-top: 8px;
  font-size: 14px;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.slider-btn {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  font-size: 24px;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 4px;
}

.slider-btn:hover {
  background: rgba(255,255,255,0.3);
}
</style>