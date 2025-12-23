<template>
  <div class="container py-5">
    <div v-if="movieStore.movieDetail">
      
      <MovieInfo :movie="movieStore.movieDetail" @show-trailer="openTrailer" />

      <div class="action-buttons mt-4">
        <button 
          @click="movieStore.toggleLike(movieId)" 
          class="action-btn"
          :class="{ 'active': movieStore.movieDetail.is_liked }"
        >
          {{ movieStore.movieDetail.is_liked ? '❤️ 좋아요 취소' : '🤍 좋아요' }}
        </button>

        <button 
          @click="movieStore.toggleWish(movieId)" 
          class="action-btn"
          :class="{ 'active': movieStore.movieDetail.is_wished }"
        >
          {{ movieStore.movieDetail.is_wished ? '🔷 찜 취소' : '🔖 볼거에요' }}
        </button>

        <button 
          @click="movieStore.toggleWatched(movieId)" 
          class="action-btn"
          :class="{ 'active': movieStore.movieDetail.is_watched }"
        >
          {{ movieStore.movieDetail.is_watched ? '✅ 봤어요' : '☑️ 안 봤어요' }}
        </button>
      </div>

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

      <div class="mt-5 text-white" v-if="Array.isArray(movieStore.movieDetail.backdrop_paths) && movieStore.movieDetail.backdrop_paths.length > 0">
        <h3>Backdrops</h3>
        <div class="row">
          <div v-for="(path, index) in movieStore.movieDetail.backdrop_paths" :key="index" class="col-md-6 mb-3">
            <img :src="`https://image.tmdb.org/t/p/original${path}`" class="img-fluid rounded">
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-5">
      <div class="spinner-border text-light"></div>
    </div>

    <YoutubeTrailer 
      v-if="showTrailerModal"
      :show="showTrailerModal" 
      :video-id="movieStore.trailerKey" 
      @close="closeTrailer" 
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useReviewStore } from '@/stores/review'
import { useMovieStore } from '@/stores/movie'

import MovieInfo from '@/components/movies/MovieInfo.vue'
import ReviewForm from '@/components/review/ReviewForm.vue'
import ReviewItem from '@/components/review/ReviewItem.vue'
import YoutubeTrailer from '@/components/movies/YoutubeTrailer.vue'

const route = useRoute()
const accountStore = useAccountStore()
const reviewStore = useReviewStore()
const movieStore = useMovieStore()

const movieId = route.params.movieId

// 예고편 모달 UI 상태 (UI 로직은 컴포넌트에 남김)
const showTrailerModal = ref(false)

const openTrailer = async () => {
  // 1. Store를 통해 키 가져오기
  await movieStore.fetchTrailer(movieId)
  
  // 2. 키가 있으면 모달 열기
  if (movieStore.trailerKey) {
    showTrailerModal.value = true
  }
}

const closeTrailer = () => {
  showTrailerModal.value = false
}

onMounted(() => {
  // Store 액션 호출로 데이터 로드
  movieStore.fetchMovieDetail(movieId)
  reviewStore.fetchMovieReviews(movieId)
})
</script>

<style scoped>
/* 버튼 레이아웃 */
.action-buttons {
  display: flex;
  gap: 15px;
}

/* 버튼 디자인 */
.action-btn {
  padding: 8px 16px;
  border: 1px solid #666;
  border-radius: 20px;
  background-color: transparent;
  color: #ddd;
  cursor: pointer;
  transition: all 0.2s;
}

/* 활성화 상태 (눌렀을 때) */
.action-btn.active {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: #fff;
  color: #ffc107; /* 포인트 컬러 */
  font-weight: bold;
}

.action-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>