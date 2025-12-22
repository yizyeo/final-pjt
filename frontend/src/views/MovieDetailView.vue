<template>
  <div class="container py-5">
    <h1 class="text-white mb-4">Movie Detail</h1>
    <hr class="border-secondary">
    
    <div v-if="movie">
      <div class="row info text-white">
        <div class="col-md-4 posterpath">
          <img 
            :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
            alt="poster" 
            class="img-fluid rounded shadow"
          >
        </div>
        <div class="col-md-8">
          <h2 class="title fw-bold">{{ movie.title }}</h2>
          <p class="text-secondary">{{ movie.release_date }} | {{ movie.runtime }} minutes</p>
          <div class="vote_average mb-3">
            <span class="badge bg-warning text-dark">TMDB 평점: {{ movie.vote_average }}</span>
          </div>
          <div class="genres mb-4">
            <span v-for="genre in movie.genres" :key="genre.id" class="badge rounded-pill bg-secondary me-2">
              {{ genre.name }}
            </span>
          </div>
          <div class="overview-section">
            <h4>줄거리</h4>
            <p class="overview">{{ movie.overview }}</p>
          </div>
        </div>
      </div>

      <hr class="text-secondary my-5">
      
      <section class="review-section">
        <h3 class="text-white mb-4">리뷰 ({{ reviewStore.movieReviews.length }})</h3>
        
        <ReviewForm v-if="accountStore.token" :moviePk="movieId" />
        <p v-else class="text-secondary">리뷰를 작성하려면 <router-link :to="{ name: 'Login' }">로그인</router-link>이 필요합니다.</p>

        <div class="review-list mt-4">
          <div v-if="reviewStore.movieReviews.length > 0">
            <div 
              v-for="review in reviewStore.movieReviews" 
              :key="review.id" 
              class="review-item bg-dark p-3 rounded mb-3 border border-secondary"
            >
              <div class="d-flex justify-content-between align-items-center">
                <div class="user-info text-white">
                  <strong>{{ review.username }}</strong>
                  <div class="star-rating d-inline-block ms-2">
                    <span 
                      v-for="i in 5" :key="i" 
                      class="star" 
                      :class="{ filled: i <= review.rating / 2 }"
                    >★</span>
                  </div>
                </div>
                <span class="text-secondary small">{{ formatDate(review.created_at) }}</span>
              </div>
              <p class="text-white mt-2">{{ review.content }}</p>
              
              <button @click="reviewStore.likeReview(review.id)" class="btn btn-sm border-0 p-0 text-white">
                {{ review.is_liked ? '❤️' : '🤍' }} {{ review.like_count }}
              </button>
            </div>
          </div>
          <p v-else class="text-secondary mt-3">아직 작성된 리뷰가 없습니다. 첫 리뷰를 남겨보세요!</p>
        </div>
      </section>

      <div class="detail mt-5 text-white">
        <div class="backdrop-container">
          <h3>Backdrops</h3>
          <div v-if="movie.backdrop_paths && movie.backdrop_paths.length > 0" class="row">
            <div v-for="(path, index) in movie.backdrop_paths" :key="index" class="col-md-6 mb-3">
              <img 
                :src="`https://image.tmdb.org/t/p/original${path}`" 
                alt="backdrop" 
                class="img-fluid rounded"
              >
            </div>
          </div>
          <p v-else class="text-secondary">등록된 배경 이미지가 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useReviewStore } from '@/stores/review' // 리뷰 스토어 추가
import { useRoute } from 'vue-router'
import axios from 'axios'
import ReviewForm from '@/components/review/ReviewForm.vue' // 리뷰 폼 컴포넌트 추가

const route = useRoute()
const accountStore = useAccountStore()
const reviewStore = useReviewStore() // 스토어 사용
const API_URL = import.meta.env.VITE_API_URL
const movieId = route.params.movieId

const movie = ref(null)

// 영화 상세 정보 가져오기
const get_movie_detail = function() {
  axios.get(`${API_URL}/movies/movie/${movieId}/detail/`)
    .then((res) => {
      movie.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
}

const formatDate = (date) => new Date(date).toLocaleDateString()

onMounted(() => {
  get_movie_detail()
  // 4. 해당 영화의 리뷰 목록 로드
  reviewStore.fetchMovieReviews(movieId)
})
</script>

<style scoped>
.star { color: #444; }
.star.filled { color: #ffc107; }
.review-item { transition: 0.3s; }
.review-item:hover { border-color: #ffc107 !important; }
</style>