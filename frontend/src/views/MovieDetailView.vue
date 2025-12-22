<template>
  <div class="container py-5">
    <div v-if="movie">
      <MovieInfo :movie="movie" />

      <hr class="text-secondary my-5">
      
      <section class="review-section">
        <h3 class="text-white mb-4">리뷰 ({{ reviewStore.movieReviews.length }})</h3>
        
        <ReviewForm v-if="accountStore.isLogin" :moviePk="movieId" />
        <div v-else class="alert alert-secondary text-center">
          리뷰를 작성하려면 <router-link :to="{ name: 'LogInView' }">로그인</router-link>이 필요합니다.
        </div>

        <div class="review-list mt-4">
          <ReviewItem 
            v-for="review in reviewStore.movieReviews" 
            :key="review.id" 
            :review="review"
            @like="reviewStore.likeReview"
          />
          <p v-if="!reviewStore.movieReviews.length" class="text-secondary">첫 리뷰를 기다리고 있어요!</p>
        </div>
      </section>

      <div class="mt-5 text-white">
        <h3>Backdrops</h3>
        <div class="row">
          <div v-for="(path, index) in movie.backdrop_paths" :key="index" class="col-md-6 mb-3">
            <img :src="`https://image.tmdb.org/t/p/original${path}`" class="img-fluid rounded">
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-5">
      <div class="spinner-border text-light"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useReviewStore } from '@/stores/review'
import axios from 'axios'

import MovieInfo from '@/components/movies/MovieInfo.vue'
import ReviewForm from '@/components/review/ReviewForm.vue'
import ReviewItem from '@/components/review/ReviewItem.vue'

const route = useRoute()
const accountStore = useAccountStore()
const reviewStore = useReviewStore()

const API_URL = import.meta.env.VITE_API_URL
const movieId = route.params.movieId
const movie = ref(null)

const getMovieDetail = async () => {
  try {
    const res = await axios.get(`${API_URL}/movies/movie/${movieId}/detail/`)
    movie.value = res.data
  } catch (err) {
    console.error("영화 정보 로드 실패:", err)
  }
}

onMounted(() => {
  getMovieDetail()
  reviewStore.fetchMovieReviews(movieId)
})
</script>

<style scoped>
.star { color: #444; }
.star.filled { color: #ffc107; }
</style>