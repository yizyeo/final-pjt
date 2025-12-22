<template>
  <div class="movie-grid">
    <div v-for="movie in movies" :key="movie.tmdb_id" class="movie-card" @click="goToDetail(movie.tmdb_id)">
      <div class="poster-wrapper">
          <img :src="getPosterUrl(movie.poster_path)" :alt="movie.title" class="poster-image" />
      </div>
      <div class="movie-info">
          <h3>{{ movie.title }}</h3>
          <p>{{ movie.release_date }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  movies: {
    type: Array,
    required: true
  }
});

const router = useRouter();

const getPosterUrl = (path) => {
    if (!path) return '/placeholder.png'; // Fallback
    if (path.startsWith('http')) return path;
    return `https://image.tmdb.org/t/p/w500${path}`;
};

const goToDetail = (id) => {
    router.push({ name: 'MovieDetailView', params: { movieId: id } });
};
</script>

<style scoped>
.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 2rem;
}

.movie-card {
    overflow: hidden;
}

.poster-wrapper {
    width: 100%;
    aspect-ratio: 2/3;
}

.poster-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.movie-info {
    padding: 1rem;
}

.movie-info h3 {
    margin: 0;
}

.movie-info p {
    margin: 0;
}
</style>
