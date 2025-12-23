<template>
  <div>
    <h3>Hot Reviews</h3>
    <button @click="goMore">더보기</button>

    <div v-if="reviewStore.hotReviews?.length > 0">
      <div v-for="review in reviewStore.hotReviews" :key="review.id">
        <ReviewCard :review="review" />
      </div>
    </div>

    <div v-else>
      <p>등록된 리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'
import ReviewCard from '@/components/review/ReviewCard.vue'

const reviewStore = useReviewStore()
const router = useRouter()

onMounted(() => {
  reviewStore.fetchHotReviews()
})

const goMore = () => {
  router.push({ 
    name: 'ReviewListView', 
  })
}
</script>