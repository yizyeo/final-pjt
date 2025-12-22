<template>
  <div class="container mt-5 pb-5">
    <div class="d-flex justify-content-between align-items-center mb-5">
      <h2 class="fw-bold text-white mb-0">커뮤니티 리뷰 피드</h2>
      
      <ReviewFilter 
        :currentSort="currentSort" 
        @change-sort="changeSort" 
      />
    </div>

    <div v-if="reviewStore.loading" class="text-center py-5 mt-5">
      <div class="spinner-border text-warning" role="status"></div>
      <p class="text-secondary mt-3">리뷰를 불러오는 중입니다...</p>
    </div>

    <div v-else class="row g-4">
      <div v-for="review in reviewStore.totalReviews" :key="review.id" class="col-12 col-xl-6">
        <ReviewCard 
          :review="review"
          @go-movie="goMovieDetail"
          @go-detail="goDetail"
          @like="reviewStore.likeReview"
        />
      </div>
      
      <div v-if="!reviewStore.totalReviews.length" class="text-center py-5">
        <h4 class="text-secondary">아직 작성된 리뷰가 없습니다.</h4>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'

import ReviewFilter from '@/components/review/ReviewFilter.vue'
import ReviewCard from '@/components/review/ReviewCard.vue'

const reviewStore = useReviewStore()
const router = useRouter()
const currentSort = ref('latest')

const changeSort = (sort) => {
  currentSort.value = sort
  reviewStore.fetchTotalReviews(sort)
}

const goMovieDetail = (moviePk) => {
  router.push({ name: 'MovieDetailView', params: { movieId: moviePk } })
}

const goDetail = (reviewPk) => {
  router.push({ name: 'ReviewDetailView', params: { reviewId: reviewPk } })
}

onMounted(() => {
  reviewStore.fetchTotalReviews()
})
</script>