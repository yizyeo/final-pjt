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

    <SearchResults v-else :movies="movies" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import SearchResults from '@/components/search/SearchResults.vue';

const route = useRoute();
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

onMounted(() => {
    fetchMovies();
});

watch(() => route.query.q, () => {
    fetchMovies();
});

</script>

<style scoped>
.search-view {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    margin-bottom: 2rem;
}

.loading, .no-results {
    text-align: center;
    padding: 3rem;
    font-size: 1.2rem;
    color: #888;
}
</style>
