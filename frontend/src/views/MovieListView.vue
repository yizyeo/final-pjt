<template>
  <div>
    <h1>영화 목록</h1>
    <hr>
    <div class="dropdown">장르</div>
    <div>연도</div>
    <hr>

    <div style="display: flex; flex-wrap: wrap;">
      <div 
        v-for="movie in movies" 
        :key="movie.tmdb_id" 
        style="width: 25%; box-sizing: border-box; padding: 10px;"
      >
        <a href="#">
          <img 
            :src="'https://image.tmdb.org/t/p/w300' + movie.poster_path" 
            :alt="movie.title"
            style="width: 100%;"
          >
        </a>
        <div>
          <strong>{{ movie.title }}</strong>
          <p>평점: {{ movie.vote_average }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// API URL 설정 (상황에 맞게 조정)
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