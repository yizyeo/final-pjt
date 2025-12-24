<template>
  <div>
    <h1>영화 목록 (로컬 데이터)</h1>
    <div style="display: flex; flex-wrap: wrap;">
      <div 
        v-for="movie in movies" 
        :key="movie.tmdb_id" 
        style="width: 25%; box-sizing: border-box; padding: 10px;"
      >
        <a href="#">
          <img 
            :src="BASE_URL + movie.local_poster_url" 
            :alt="movie.title"
            style="width: 100%; min-height: 200px; background-color: #333;"
          >
        </a>
        <div>
          <strong>{{ movie.title }}</strong>
          <p>평점: {{ movie.vote_average?.toFixed(1) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL
// Django 서버의 기본 주소 (예: http://127.0.0.1:8000)
const BASE_URL = API_URL.replace('/api/v1', '') 

const movies = ref([])

const getMovies = function () {
  axios.get(`${API_URL}/movies/movielist/`)
    .then(res => {
      movies.value = res.data
    })
    .catch(err => console.log(err))
}

onMounted(getMovies)
</script>