<template>
  <div>
    <div>
      <h2>커뮤니티 리뷰 피드</h2>
      
      <ReviewFilter 
        :currentSort="currentSort" 
        @change-sort="changeSort" 
      />
    </div>

    <div v-if="reviewStore.loading">
      <p>리뷰를 불러오는 중입니다...</p>
    </div>

    <div v-else>
      <div v-for="review in reviewStore.totalReviews" :key="review.id">
        <ReviewCard 
          :review="review"
          @go-movie="goMovieDetail"
          @go-detail="goDetail"
          @like="reviewStore.likeReview"
        />
      </div>
      
      <div v-if="!reviewStore.totalReviews.length">
        <h4>아직 작성된 리뷰가 없습니다.</h4>
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
const currentSort = ref('popular')

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
  reviewStore.fetchTotalReviews(currentSort.value)
})
</script>