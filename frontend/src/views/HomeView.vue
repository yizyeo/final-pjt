<template>
  <div>
    <h1>Home</h1>
    <HomeMainCarousel />
    <HomeActionButtons />
    
    <div class="container">
      <HomeHotMovies />
      <HomeHotReviews />
    </div>
  </div>
</template>

<script setup>
import HomeMainCarousel from '@/components/home/HomeMainCarousel.vue'
import HomeActionButtons from '@/components/home/HomeActionButtons.vue'
import HomeHotMovies from '@/components/home/HomeHotMovies.vue'
import HomeHotReviews from '@/components/home/HomeHotReviews.vue'

</script>

<style>

</style>
