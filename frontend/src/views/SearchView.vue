<template>
  <div class="search-view">
    <div class="header">
        <h1>"{{ query }}" 검색 결과</h1>
    </div>
    
    <div v-if="loading" class="loading">
        검색 중...
    </div>

    <div v-else-if="movies.length === 0" class="no-results">
        검색 결과가 없습니다.
    </div>

    <div v-else class="movie-grid">
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
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const query = ref('');
const movies = ref([]);
const loading = ref(false);
const API_URL = import.meta.env.VITE_API_URL;

const fetchMovies = async () => {
    const q = route.query.q;
    query.value = q;
    
    if (!q) {
        movies.value = [];
        return;
    }

    loading.value = true;
    try {
        const response = await axios.get(`${API_URL}/movies/search/`, {
            params: { q: q }
        });
        movies.value = response.data;
    } catch (error) {
        console.error('검색 실패:', error);
    } finally {
        loading.value = false;
    }
};

const getPosterUrl = (path) => {
    if (!path) return '/placeholder.png'; // Fallback
    if (path.startsWith('http')) return path;
    return `https://image.tmdb.org/t/p/w500${path}`;
};

const goToDetail = (id) => {
    router.push({ name: 'MovieDetailView', params: { movieId: id } });
};

onMounted(() => {
    fetchMovies();
});

watch(() => route.query.q, () => {
    fetchMovies();
});

</script>

<style scoped>

</style>