<template>
  <div>
    <h1>Home</h1>
    <a href="#">Carousel</a>
    <div v-if="backdrops.length > 0">
      <h3>Movies:</h3>
      <div v-for="movie in backdrops" :key="movie.tmdb_id">
        <p>Movie: {{ movie.title }}</p>
        <div>
          <img :src="`https://image.tmdb.org/t/p/original${movie.backdrop_paths[0]}`" alt="Backdrop" style="width: 300px;">
        </div>
        <hr>
      </div>
    </div>
    <hr>

    <div class="btn-group">
      <div>
        <a href="#" class="btn">Review</a> <!-- /reviews -->
        <!-- <button type="button" class="btn">Reviews</button>  -->
      </div>
      <div>
        <a href="#" class="btn">Recommend</a> <!-- /reviewrecommend -->
      </div>
      <div>
        <a href="#" class="btn">Worldcup</a> <!-- /worldcup -->
      </div>
    </div>
    <hr>
    <div class="container">
      <div class="hot-lists">
        <h3>Hot Movie List</h3>
        
        <div v-if="homelist.length > 0">
          <p>Movie: {{ homelist[0].title }}</p>
          <div>
            <img :src="`https://image.tmdb.org/t/p/original${homelist[0].poster_path}`" alt="poster" style="width: 300px;">
          </div>
          <hr>
        </div>
        
        <div class="carousel">
          <div class="carousel-track"></div>
          <button class="carousel-button prev"><</button>
          <button class="carousel-button next">></button>
        </div>
      </div>
      <div class="hot-reviews">
        <h3>Hot Reviews</h3>
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


  const backdrops = ref([])
  const homelist = ref([])

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
    carousel_backdrop(),
    movie_poster()
  })
  // hot review 불러오기
  const hot_review = function() {

  }

</script>

<style>

</style>