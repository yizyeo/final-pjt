<template>
  <div class="hot-lists">
    <h3>Hot Movie List</h3>
    
    <div v-if="homelist.length > 0">
      <p>Movie: {{ homelist[0].title }}</p>
      <div>
        <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: homelist[0].tmdb_id } }">
          <img :src="`https://image.tmdb.org/t/p/original${homelist[0].poster_path}`" alt="poster" style="width: 300px; cursor: pointer;">
        </RouterLink>
      </div>
      <hr>
    </div>
    
    <div class="carousel">
      <div class="carousel-track"></div>
      <button class="carousel-button prev"><</button>
      <button class="carousel-button next">></button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL
const homelist = ref([])

// hot movie poster 불러오기
const movie_poster = function() {
  axios.get(`${API_URL}/movies/homelist`)
  .then((res) => {
    homelist.value = res.data.slice(0,10)
    console.log('HomeList fetched:', homelist.value)
  })
  .catch((err) => {
    console.log(err)
  })
}

onMounted(() => {
  movie_poster()
})
</script>

<style scoped>
</style>
