<template>
  <section class="list-section">
    <h3>내가 작성한 리뷰 ({{ reviewCount }})</h3>
    <div v-if="reviews.length" class="review-grid">
      <div v-for="review in reviews" :key="review.id" class="review-card">
        <h4>{{ review.movie_title }}</h4>
        <p>{{ review.content }}</p>
        <span>{{ review.rating }}점</span>
      </div>
    </div>
    <p v-else>아직 작성한 리뷰가 없습니다.</p>
  </section>
</template>

<script setup>
defineProps(['reviews', 'reviewCount'])
</script>