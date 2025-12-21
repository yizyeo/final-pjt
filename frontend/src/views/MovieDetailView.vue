<template>
  <div>
    <h1>Movie Detail</h1>
    <hr>
    <div v-if="movie">
      <div class="info">
        <div class="title">{{ movie.title }}</div>
        <div class="posterpath">
          <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" alt="poster">
        </div>
        <div class="releasedate">{{ movie.release_date }}</div>
        <div class="vote_average">{{ movie.vote_average }}</div>
        <div class="genres">
          <span v-for="genre in movie.genres" :key="genre.id">{{ genre.name }}</span>
        </div>
        <div class="runtime">{{ movie.runtime }} minutes</div>
      </div>
      <div class="detail">
        <div class="overview">{{ movie.overview }}</div>
        <div class="backdrop-container">
          <h3>Backdrops</h3>
          <div v-if="movie.backdrop_paths && movie.backdrop_paths.length > 0">
            <div v-for="(path, index) in movie.backdrop_paths" :key="index" class="backdrop-item">
              <img 
                :src="`https://image.tmdb.org/t/p/original${path}`" 
                alt="backdrop" 
                style="width: 100%; margin-bottom: 10px;"
              >
            </div>
          </div>
          <p v-else>등록된 배경 이미지가 없습니다.</p>
        </div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { onMounted, ref, computed } from 'vue'
  import { useAccountStore } from '@/stores/accounts'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const store = useAccountStore()
  const API_URL = import.meta.env.VITE_API_URL
  const movieId = route.params.movieId

  const movie = ref(null)
  
  const get_movie_detail = function() {

    axios.get(`${API_URL}/movies/movie/${movieId}/detail/`)
    .then((res) => {
      movie.value = res.data
      // const data = res.data

      // if (typeof data.backdrop_paths === 'string') {
      //   try {
      //     data.backdrop_paths = JSON.parse(data.backdrop_paths.replace(/'/g, '"'))
      //   } catch (e) {
      //     console.error("Backdrop parsing error", e)
      //     data.backdrop_paths = []
      //   }
      // }
      // movie.value = data
    })
    .catch((err) => {
      console.log(err)
    })
  }

  onMounted(() => {
    get_movie_detail()
  })

</script>

<style scoped>

</style>