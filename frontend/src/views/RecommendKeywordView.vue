<template>
  <div class="page-container">
    
    <div class="header-section">
      <h1 class="page-title">AI 큐레이터 🤖</h1>
      <p class="page-desc">
        기분, 상황, 분위기 무엇이든 적어주세요.<br class="mobile-break" />
        AI가 당신을 위한 딱 맞는 영화를 찾아드립니다.
      </p>
    </div>

    <div class="input-section">
      <div class="search-box-wrapper" :class="{ focused: isFocused }">
        <input 
          v-model="userInput" 
          @keyup.enter="getRecommendation"
          @focus="isFocused = true"
          @blur="isFocused = false"
          type="text" 
          class="search-input" 
          placeholder="어떤 영화를 찾고 계신가요?"
          :disabled="isLoading"
        >
        <button 
          @click="getRecommendation" 
          class="search-btn" 
          :disabled="isLoading || !userInput.trim()"
        >
          <span v-if="isLoading" class="spinner"></span>
          <span v-else>추천받기</span>
        </button>
      </div>

      <div class="keyword-chips">
        <span class="chip-label">예시 키워드:</span>
        <button 
          v-for="keyword in keywords" 
          :key="keyword"
          class="chip-btn"
          @click="selectKeyword(keyword)"
        >
          #{{ keyword }}
        </button>
      </div>
    </div>

    <div class="divider"></div>

    <div class="result-section">
      
      <div v-if="isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>AI가 영화를 분석하고 있습니다...</p>
      </div>

      <div v-else-if="movies.length > 0" class="movie-grid-wrapper">
        <h3 class="result-title">큐레이터의 추천 리스트</h3>
        <div class="movie-grid">
          <div v-for="movie in movies" :key="movie.tmdb_id" class="movie-item">
            <MovieListItem :movie="movie" />
          </div>
        </div>
      </div>

      <div v-else-if="searched" class="empty-state">
        <div class="empty-icon">🤔</div>
        <p>조건에 맞는 영화를 찾지 못했습니다.<br>조금 더 구체적으로 질문해 주시겠어요?</p>
      </div>

      <div v-else class="initial-state">
        <p class="guide-text">위 검색창에 원하시는 영화 스타일을 입력해보세요.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
// [중요] 일관된 디자인을 위해 이전에 만든 MovieListItem 사용 권장
import MovieListItem from '@/components/movies/MovieListItem.vue'

const accountStore = useAccountStore()
const userInput = ref('')
const movies = ref([])
const isLoading = ref(false)
const searched = ref(false)
const isFocused = ref(false)

const API_URL = import.meta.env.VITE_API_URL

// 추천 키워드 목록
const keywords = ['선풍기 앞에 누워서 보기 좋은', '마라탕과 어울리는', '눈 오는 날 보기 좋은']

const selectKeyword = (keyword) => {
  userInput.value = keyword
}

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
/* 전체 레이아웃 */
.page-container {
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
  padding: 4rem 1.5rem;
  min-height: 80vh;
}

/* 1. 헤더 섹션 */
.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.page-desc {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
}

/* 2. 입력 섹션 */
.input-section {
  max-width: 700px;
  margin: 0 auto 4rem auto;
}

.search-box-wrapper {
  display: flex;
  align-items: center;
  background-color: #FFF;
  border: 2px solid #E0E0E0;
  border-radius: 50px; /* 둥근 알약 모양 */
  padding: 6px 6px 6px 24px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.search-box-wrapper.focused {
  border-color: #7A6CFA;
  box-shadow: 0 4px 20px rgba(122, 108, 250, 0.15);
}

.search-input {
  flex: 1;
  border: none;
  font-size: 1.1rem;
  color: #333;
  outline: none;
  background: transparent;
}

.search-input::placeholder {
  color: #AAA;
}

.search-btn {
  background-color: #7A6CFA;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 28px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  min-width: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-btn:hover:not(:disabled) {
  background-color: #6859D4;
}

.search-btn:disabled {
  background-color: #CCC;
  cursor: not-allowed;
}

/* 키워드 칩 */
.keyword-chips {
  margin-top: 1.2rem;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.chip-label {
  font-size: 0.9rem;
  color: #888;
  margin-right: 4px;
}

.chip-btn {
  background-color: #F3F0FF;
  color: #7A6CFA;
  border: 1px solid transparent;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.chip-btn:hover {
  background-color: #EBE5FF;
  transform: translateY(-2px);
}

/* 구분선 */
.divider {
  height: 1px;
  background-color: #EEE;
  margin-bottom: 3rem;
}

/* 3. 결과 섹션 */
.result-section {
  min-height: 300px;
}

.result-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1.5rem;
}

/* 그리드 (MovieListView와 동일한 규격) */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 3rem 1.5rem;
  animation: fadeIn 0.5s ease-out;
}

/* 로딩 상태 */
.loading-state {
  text-align: center;
  padding: 4rem 0;
  color: #7A6CFA;
}

.loading-spinner {
  width: 40px; height: 40px;
  border: 4px solid #E0E0E0;
  border-top-color: #7A6CFA;
  border-radius: 50%;
  margin: 0 auto 1rem auto;
  animation: spin 1s infinite linear;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* 결과 없음 */
.empty-state, .initial-state {
  text-align: center;
  padding: 4rem 0;
  color: #888;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.guide-text {
  color: #CCC;
  font-size: 1.1rem;
}

/* 애니메이션 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 반응형 */
@media (max-width: 768px) {
  .page-title { font-size: 1.8rem; }
  .page-desc { font-size: 1rem; }
  
  .search-box-wrapper {
    padding: 4px 4px 4px 16px;
  }
  
  .search-btn {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
  
  .keyword-chips {
    justify-content: flex-start; /* 모바일에서 좌측 정렬 */
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 5px;
  }
  
  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem 12px;
  }
  
  .mobile-break { display: none; }
}
</style>