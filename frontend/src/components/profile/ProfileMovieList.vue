<template>
  <section class="profile-movies-card">
    <div class="tabs-container">
      <div class="tabs-track">
        <button 
          v-for="tab in tabs" 
          :key="tab.id" 
          class="tab-btn"
          :class="{ active: currentTab === tab.id }" 
          @click="currentTab = tab.id"
        >
          {{ tab.name }} <span class="tab-count">{{ getMovieCount(tab.id) }}</span>
        </button>
      </div>
    </div>

    <div v-if="displayMovies.length > 0" class="slider-container">
      <button class="nav-btn left" @click="scroll('left')" aria-label="Previous">
        <span class="arrow">‹</span>
      </button>

      <div class="movie-scroll-viewport" ref="scrollContainer">
        <div 
          v-for="movie in displayMovies" 
          :key="movie.tmdb_id" 
          class="movie-card-item"
          @click="goMovieDetail(movie.tmdb_id)"
        >
          <div class="poster-container">
            <img 
              :src="movie.poster_path ? 'https://image.tmdb.org/t/p/w300' + movie.poster_path : '/no-poster.png'" 
              :alt="movie.title"
              class="poster-img"
            >
          </div>
          <div class="title-wrapper">
            <p class="movie-title-text">{{ movie.title }}</p>
          </div>
        </div>
      </div>

      <button class="nav-btn right" @click="scroll('right')" aria-label="Next">
        <span class="arrow">›</span>
      </button>
    </div>

    <div v-else class="empty-state">
      <p>기록된 영화가 없습니다.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps(['profile'])
const router = useRouter()
const scrollContainer = ref(null)

const currentTab = ref('liked')
const tabs = [
  { id: 'liked', name: '좋아요' },
  { id: 'wish', name: '볼 영화' },
  { id: 'watched', name: '본 영화' }
]

const displayMovies = computed(() => {
  if (currentTab.value === 'liked') return props.profile?.like_movies || []
  if (currentTab.value === 'wish') return props.profile?.wish_movies || []
  if (currentTab.value === 'watched') return props.profile?.watched_movies || []
  return []
})

const getMovieCount = (tabId) => {
  const list = tabId === 'liked' ? props.profile?.like_movies : 
               tabId === 'wish' ? props.profile?.wish_movies : 
               props.profile?.watched_movies
  return list?.length || 0
}

const scroll = (direction) => {
  if (scrollContainer.value) {
    const offset = direction === 'left' ? -500 : 500
    scrollContainer.value.scrollBy({ left: offset, behavior: 'smooth' })
  }
}

const goMovieDetail = (movieId) => {
  router.push({ name: 'MovieDetailView', params: { movieId } })
}
</script>

<style scoped>
.profile-movies-card {
  background-color: #FFFFFF;
  border-radius: 20px;
  padding: 2.5rem 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.tabs-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.tabs-track {
  display: flex;
  background-color: #F2F2F7;
  padding: 4px;
  border-radius: 12px;
}

.tab-btn {
  border: none;
  background: none;
  padding: 8px 20px;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #8E8E93;
  cursor: pointer;
}

.tab-btn.active {
  background-color: #FFFFFF;
  color: #7A6CFA;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.tab-count {
  margin-left: 4px;
  font-size: 0.8rem;
  font-weight: 400;
}

.slider-container {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
}

.movie-scroll-viewport {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 10px 5px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.movie-scroll-viewport::-webkit-scrollbar {
  display: none;
}

/* [핵심] 너비 고정 */
.movie-card-item {
  flex: 0 0 160px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.2s;
}

.movie-card-item:hover {
  transform: translateY(-5px);
}

.poster-container {
  width: 160px;
  height: 240px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* [수정] 제목 영역: 왼쪽 정렬 및 줄바꿈 허용 */
.title-wrapper {
  margin-top: 10px;
  padding: 0 2px;
  width: 100%;
}

.movie-title-text {
  font-size: 0.85rem;
  font-weight: 700;
  color: #333;
  text-align: left; /* 왼쪽 정렬 */
  line-height: 1.4;
  /* 한 줄 제한 해제하고 2줄까지만 허용하고 싶을 때 유용한 설정 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* [수정] 네비게이션 버튼: 보라색 제거 */
.nav-btn {
  position: absolute;
  top: 110px;
  z-index: 10;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.95);
  border: 1px solid #E5E5EA;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #333;
  transition: all 0.2s;
}

.nav-btn:hover {
  background-color: #F2F2F7;
  border-color: #D1D1D6;
}

.nav-btn.left { left: 0; }
.nav-btn.right { right: 0; }

.arrow {
  font-size: 1.5rem;
  line-height: 1;
  font-weight: 300;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: #AAA;
}
</style>