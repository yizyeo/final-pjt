<template>
  <div class="recommend-container container py-5">
    <div class="text-center mb-5">
      <h1 class="display-5 fw-bold text-white mb-3">AI 영화 소믈리에 🍷</h1>
      <p class="text-secondary lead">
        "비 오는 날 혼자 보기 좋은 잔잔한 영화 추천해줘"<br>
        상황이나 기분을 적으면 AI가 딱 맞는 영화를 골라드려요.
      </p>
    </div>

    <div class="search-wrapper mx-auto mb-5" style="max-width: 650px;">
      <div class="input-group shadow-lg">
        <input 
          v-model="userInput" 
          @keyup.enter="getRecommendation"
          type="text" 
          class="form-control form-control-lg bg-dark text-white border-secondary" 
          placeholder="어떤 영화를 찾으시나요?"
          :disabled="isLoading"
        >
        <button 
          @click="getRecommendation" 
          class="btn btn-primary px-4" 
          :disabled="isLoading || !userInput.trim()"
        >
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          {{ isLoading ? '분석 중...' : '추천받기' }}
        </button>
      </div>
      <div class="mt-2 text-start small text-muted px-2">
        추천 키워드: #새벽감성 #심장쫄깃한스릴러 #가족과함께 #인생영화
      </div>
    </div>

    <hr class="border-secondary my-5">

    <div v-if="movies.length > 0" class="results-area">
      <h3 class="text-white mb-4">🍷 소믈리에가 엄선한 리스트</h3>
      <div class="row row-cols-2 row-cols-md-3 row-cols-lg-5 g-4">
        <div v-for="movie in movies" :key="movie.tmdb_id" class="col">
          <MovieCard :movie="movie" />
        </div>
      </div>
    </div>

    <div v-else-if="!isLoading && searched" class="text-center py-5">
      <p class="text-secondary fs-4">검색 결과가 없습니다. 다른 키워드로 입력해보세요!</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import MovieCard from '@/components/movies/MovieCard.vue'

const accountStore = useAccountStore()
const userInput = ref('')
const movies = ref([])
const isLoading = ref(false)
const searched = ref(false)

const API_URL = import.meta.env.VITE_API_URL

const getRecommendation = async () => {
  if (!userInput.value.trim()) return

  isLoading.value = true
  searched.value = true
  movies.value = []

  try {
    const res = await axios.post(
      `${API_URL}/movies/recommend/keyword/`,
      { content: userInput.value },
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    movies.value = res.data
  } catch (err) {
    console.error('추천 요청 에러:', err)
    alert('AI 추천 서버와 통신 중 문제가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.recommend-container {
  min-height: 70vh;
}

.search-wrapper input:focus {
  background-color: #2c2c2c !important;
  border-color: #6a11cb;
  box-shadow: 0 0 10px rgba(106, 17, 203, 0.3);
}

.btn-primary {
  background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
  border: none;
}

.btn-primary:hover {
  filter: brightness(1.1);
}

/* 추천 리스트 페이드인 애니메이션 */
.results-area {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>