<template>
  <div v-if="profile" class="profile-container">
    <header class="profile-header">
      <div class="rank-badge">
        <img :src="userTier.icon" :alt="userTier.label" class="tier-icon">
        <p class="tier-label">{{ userTier.label }}</p>
      </div>
      
      <div class="user-info">
        <h1>{{ profile.username }}님의 프로필</h1>
        <p class="ai-bio">{{ profile.bio || "AI 생성 한 줄 소개" }}</p>
      </div>
    </header>

    <hr>

    <section class="list-section">
      <h3>내가 작성한 리뷰 ({{ profile.review_count }})</h3>
      <div v-if="profile.reviews.length" class="review-grid">
        <div v-for="review in profile.reviews" :key="review.id" class="review-card">
          <h4>{{ review.movie_title }}</h4>
          <p>{{ review.content }}</p>
          <span>⭐ {{ review.rating }}점</span>
        </div>
      </div>
      <p v-else>아직 작성한 리뷰가 없습니다.</p>
    </section>

    <section class="movie-lists">
      <div class="tabs">
        <button @click="currentTab = 'liked'">좋아요</button>
        <button @click="currentTab = 'wish'">볼 영화</button>
        <button @click="currentTab = 'watched'">본 영화</button>
      </div>

      <div class="movie-grid">
        <div v-for="movie in displayMovies" :key="movie.tmdb_id" class="movie-card">
          <img :src="'https://image.tmdb.org/t/p/w200' + movie.poster_path" :alt="movie.title">
          <p>{{ movie.title }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const route = useRoute()
const store = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL

const profile = ref(null)
const currentTab = ref('liked')

onMounted(async () => {
  try {
    const res = await axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/${route.params.username}/`,
      headers: { Authorization: `Token ${store.token}` }
    })
    profile.value = res.data
  } catch (err) {
    console.error('프로필 로딩 실패', err)
  }
})

const userTier = computed(() => {
  const count = profile.value?.review_count || 0
  if (count >= 10) return { label: '시네마 마스터', icon: '/icons/rank_5.png' }
  if (count >= 5) return { label: '영화 전문가', icon: '/icons/rank_4.png' }
  if (count >= 3) return { label: '영화 애호가', icon: '/icons/rank_3.png' }
  if (count >= 1) return { label: '뉴비 평론가', icon: '/icons/rank_2.png' }
  return { label: '관객', icon: '/icons/rank_1.png' }
})

const displayMovies = computed(() => {
  if (currentTab.value === 'liked') return profile.value?.like_movies
  if (currentTab.value === 'wish') return profile.value?.wish_movies
  if (currentTab.value === 'watched') return profile.value?.watched_movies
  return []
})
</script>

<style scoped>
/* 간단한 스타일링 */
/* .profile-container { max-width: 800px; margin: 0 auto; padding: 20px; }
.profile-header { display: flex; align-items: center; gap: 30px; margin-bottom: 30px; }
.tier-icon { width: 80px; height: 80px; border-radius: 50%; background: #f0f0f0; }
.tier-label { font-weight: bold; text-align: center; margin-top: 5px; }
.movie-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; margin-top: 20px; }
.movie-card img { width: 100%; border-radius: 8px; }
.tabs { display: flex; gap: 10px; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
.review-card { border: 1px solid #eee; padding: 15px; border-radius: 8px; margin-bottom: 10px; } */
</style>