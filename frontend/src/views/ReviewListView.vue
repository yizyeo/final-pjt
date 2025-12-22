<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold text-white">커뮤니티 리뷰</h2>
      
      <div class="btn-group">
        <button 
          @click="changeSort('latest')" 
          class="btn btn-outline-light" 
          :class="{ active: currentSort === 'latest' }"
        >최신순</button>
        <button 
          @click="changeSort('popular')" 
          class="btn btn-outline-light" 
          :class="{ active: currentSort === 'popular' }"
        >인기순</button>
      </div>
    </div>

    <div v-if="reviewStore.loading" class="text-center text-white">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else class="row g-4">
      <div v-for="review in reviewStore.totalReviews" :key="review.id" class="col-12 col-md-6">
        <div class="card bg-dark text-white h-100 border-secondary review-card">
          <div class="row g-0">
            <div class="col-4 movie-poster-wrapper" @click="goMovieDetail(review.movie)">
              <img :src="getImageUrl(review.movie_poster)" class="img-fluid rounded-start h-100" alt="poster">
            </div>
            
            <div class="col-8">
              <div class="card-body d-flex flex-column h-100">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h5 class="card-title text-truncate mb-0" @click="goMovieDetail(review.movie)">
                    {{ review.movie_title }}
                  </h5>
                  <div class="star-rating">
                    <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating / 2 }">
                      ★
                    </span>
                  </div>
                </div>

                <p 
                  @click="goDetail(review.id)" 
                  class="card-text flex-grow-1 review-content" 
                  style="cursor: pointer;"
                >
                  {{ review.content }}
                </p>

                <div class="d-flex justify-content-between align-items-center mt-3">
                  <span class="text-secondary small">by {{ review.username }}</span>
                  <div class="d-flex align-items-center gap-3">
                    <button @click="reviewStore.likeReview(review.id)" class="btn-like">
                      <span :class="{ 'liked': review.is_liked }">
                        {{ review.is_liked ? '❤️' : '🤍' }}
                      </span>
                      <span class="ms-1">{{ review.like_count }}</span>
                    </button>
                    <button @click="goDetail(review.id)" class="btn btn-sm btn-outline-secondary">댓글</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useReviewStore } from '@/stores/review'
import { useRouter } from 'vue-router'

const reviewStore = useReviewStore()
const router = useRouter()
const currentSort = ref('latest')

const changeSort = (sort) => {
  currentSort.value = sort
  reviewStore.fetchTotalReviews(sort)
}

const getImageUrl = (path) => path ? `https://image.tmdb.org/t/p/w200${path}` : '/no-image.png'
const goMovieDetail = (moviePk) => router.push({ name: 'MovieDetailView', params: { movieId: moviePk } })
const goDetail = (reviewPk) => router.push({ name: 'ReviewDetailView', params: { reviewId: reviewPk } })

onMounted(() => {
  reviewStore.fetchTotalReviews()
})
</script>

<style scoped>
.review-card {
  transition: transform 0.2s;
}
.review-card:hover {
  transform: translateY(-5px);
}
.movie-poster-wrapper {
  cursor: pointer;
  overflow: hidden;
}
.movie-poster-wrapper img {
  object-fit: cover;
}

/* 별점 CSS */
.star-rating {
  color: #444; /* 비어있는 별 색상 */
  font-size: 0.9rem;
}
.star.filled {
  color: #ffc107; /* 채워진 별 색상 (노란색) */
}

.review-content {
  font-size: 0.95rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.btn-like {
  background: none;
  border: none;
  color: white;
  padding: 0;
  display: flex;
  align-items: center;
}

.liked {
  transform: scale(1.2);
  transition: 0.2s;
}
</style>