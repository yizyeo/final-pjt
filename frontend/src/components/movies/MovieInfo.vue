<template>
  <div class="row info text-white">
    <div class="col-md-4 posterpath">
      <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" alt="poster" class="img-fluid rounded shadow">
    </div>
    <div class="col-md-8">
      <h2 class="title fw-bold">{{ movie.title }}</h2>
      <p class="text-secondary">{{ movie.release_date }} | {{ movie.runtime }} mins</p>
      <div class="badge bg-warning text-dark mb-3">평점: {{ movie.vote_average?.toFixed(1) }}</div>
      <div class="genres mb-4">
        <span v-for="genre in movie.genres" :key="genre.id" class="badge rounded-pill bg-secondary me-2">
          {{ genre.name }}
        </span>
      </div>
      
      <button @click="$emit('show-trailer')" class="btn btn-danger mb-4">
        🎬 예고편 보기
      </button>

      <h4>줄거리</h4>
      <p class="overview">{{ movie.overview }}</p>

      <div v-if="movie.credits" class="mt-4">
        <div v-if="movie.credits.directors?.length > 0">
          <strong>감독:</strong> {{ movie.credits.directors.join(', ') }}
        </div>
        <div v-if="movie.credits.actors?.length > 0" class="mt-2">
          <strong>출연:</strong> {{ movie.credits.actors.join(', ') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['movie'])
defineEmits(['show-trailer'])
</script>