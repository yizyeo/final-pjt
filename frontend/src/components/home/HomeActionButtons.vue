<template>
  <div class="btn-group">
    <div>
      <a href="#" class="btn">Review</a> <!-- /reviews -->
      <!-- <button type="button" class="btn">Reviews</button>  -->
    </div>
    <div>
      <a href="#" class="btn">Recommend</a> <!-- /reviewrecommend -->
    </div>
    <div>
      <RouterLink to="/worldcup" class="btn">Worldcup</RouterLink> <!-- /worldcup -->
    </div>
  </div>
  <hr>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
</style>
