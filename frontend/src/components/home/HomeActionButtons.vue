<template>
  <div class="btn-group">
    <div>
      <RouterLink to="/blind-review" class="btn">Blind Review</RouterLink> <!-- /reviewrecommend -->
    </div>
    <div>
      <RouterLink to="/recommend-keyword" class="btn">Recommend by Keyword</RouterLink> <!-- /reviewrecommend -->
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
