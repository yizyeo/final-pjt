<template>
  <div class="row info text-white">
    <div class="col-md-4 posterpath">
      <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" alt="poster" class="img-fluid rounded shadow">
    </div>
    <div class="col-md-8">
      <h2 class="title fw-bold">{{ movie.title }}</h2>
      <p class="text-secondary">{{ movie.release_date }} | {{ movie.runtime }} mins</p>
      <div class="badge bg-warning text-dark mb-3">평점: {{ movie.vote_average }}</div>
      <div class="genres mb-4">
        <span v-for="genre in movie.genres" :key="genre.id" class="badge rounded-pill bg-secondary me-2">
          {{ genre.name }}
        </span>
      </div>
      <h4>줄거리</h4>
      <p class="overview">{{ movie.overview }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps(['movie'])
</script>