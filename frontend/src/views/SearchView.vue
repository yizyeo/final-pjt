<template>
  <div class="page-container">
    
    <div class="search-header">
      <h1 class="search-title">
        "<span class="highlight">{{ query }}</span>" 검색 결과
      </h1>
      <p v-if="!loading" class="result-count">
        총 <span class="count-num">{{ movies.length }}</span>개의 작품을 찾았습니다.
      </p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else-if="movies.length === 0" class="empty-state">
      <div class="empty-icon">🤔</div>
      <p class="empty-msg">검색 결과가 없습니다.</p>
      <p class="empty-desc">단어의 철자가 정확한지 확인해 보거나,<br>다른 검색어로 다시 시도해 보세요.</p>
    </div>

    <div v-else class="result-container">
      <SearchResults :movies="movies" />
    </div>

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
/* 페이지 컨테이너 (다른 뷰들과 통일) */
.page-container {
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
  padding: 3rem 1.5rem;
  background-color: #FFFFFF;
  min-height: 100vh;
}

/* 1. 헤더 스타일 */
.search-header {
  margin-bottom: 3rem;
  border-bottom: 1px solid #F0F0F0;
  padding-bottom: 1.5rem;
}

.search-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 0.5rem;
  word-break: break-all; /* 긴 검색어 줄바꿈 */
}

.highlight {
  color: #7A6CFA; /* 브랜드 컬러 */
}

.result-count {
  font-size: 1rem;
  color: #666;
}

.count-num {
  font-weight: 700;
  color: #333;
}

/* 2. 로딩 상태 */
.loading-state {
  display: flex;
  justify-content: center;
  padding: 5rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #F3F3F3;
  border-top: 4px solid #7A6CFA;
  border-radius: 50%;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 3. 결과 없음 */
.empty-state {
  text-align: center;
  padding: 6rem 0;
  background-color: #FAFAFA;
  border-radius: 16px;
  color: #888;
  border: 1px dashed #DDD;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-msg {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.empty-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #999;
}

/* 4. 결과 컨테이너 */
.result-container {
  width: 100%;
}

/* 반응형 */
@media (max-width: 768px) {
  .search-title {
    font-size: 1.6rem;
  }
  
  .page-container {
    padding: 2rem 1rem;
  }
}
</style>