<template>
  <div v-if="profile" class="profile-container">
    <header class="profile-header">
      <div class="rank-badge">
        <img :src="userTier.icon" :alt="userTier.label" class="tier-icon">
        <p class="tier-label">{{ userTier.label }}</p>
      </div>
      
      <div v-if="!isEditing" class="user-info">
        <h1>{{ profile.username }}님의 프로필</h1>
        <p class="ai-bio">{{ profile.bio || "AI 생성 한 줄 소개" }}</p>
        <button v-if="accountStore.username === route.params.username" @click="startEdit" class="btn-edit-trigger">
          내 정보 수정하기
        </button>
      </div>

      <div v-else class="user-info-edit">
        <h1>정보 수정</h1>
        <div class="edit-form">
          <label>Email: </label>
          <input v-model.trim="editData.email" type="email" placeholder="이메일">
          <label>Age: </label>
          <input v-model.number="editData.age" type="number" placeholder="나이">
          <p>성별</p>
          <label>
            <input type="radio" value="M" v-model="editData.gender">남성
          </label>
          <label>
            <input type="radio" value="F" v-model="editData.gender">여성
          </label>
          <p>선호 장르</p>
          <div class="genre-grid">
            <label v-for="genre in genres" :key="genre.genre_id">
              <input 
                type="checkbox" 
                :value="genre.genre_id"  v-model="editData.favorite_genres"
              >
              {{ genre.name_kr }}
            </label>
          </div>
          <div class="edit-actions">
            <button @click="updateInfo" class="btn-save">저장</button>
            <button @click="isEditing = false" class="btn-cancel">취소</button>
          </div>
        </div>
      </div>
    </header>

    <hr>

    <section class="list-section">
      <h3>내가 작성한 리뷰 ({{ profile.review_count }})</h3>
      <div v-if="profile.reviews.length" class="review-grid">
        <div v-for="review in profile.reviews" :key="review.id" class="review-card">
          <h4>{{ review.movie_title }}</h4>
          <p>{{ review.content }}</p>
          <span>{{ review.rating }}점</span>
        </div>
      </div>
      <p v-else>아직 작성한 리뷰가 없습니다.</p>
    </section>

    <section class="movie-lists">
      <div class="tabs">
        <button :class="{ active: currentTab === 'liked' }" @click="currentTab = 'liked'">좋아요</button>
        <button :class="{ active: currentTab === 'wish' }" @click="currentTab = 'wish'">볼 영화</button>
        <button :class="{ active: currentTab === 'watched' }" @click="currentTab = 'watched'">본 영화</button>
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
const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL

const profile = ref(null)
const genres = ref([])
const currentTab = ref('liked')

const isEditing = ref(false)
const editData = ref({
  email: '',
  age: null,
  gender: '',
  favorite_genres: []
})

onMounted(async () => {
  try {
    // 프로필 정보 조회
    const res = await axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/${route.params.username}/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    profile.value = res.data

    // 장르 목록 조회
    const genreRes = await axios.get(`${API_URL}/movies/genres/`)
    genres.value = genreRes.data
  } catch (err) {
    console.error('데이터 로딩 실패', err)
  }
})

// 수정 모드
const startEdit = () => {
  if (!profile.value) return
  
  const currentGenres = profile.value.favorite_genres || []

  editData.value = {
    email: profile.value.email,
    age: profile.value.age,
    gender: profile.value.gender,
    // DB의 장르 객체 리스트에서 genre_id만 추출하여 배열 생성
    favorite_genres: currentGenres.map(g => {
      // 서버 응답 필드명에 따라 g.genre_id 혹은 g.id 중 맞는 것을 선택하세요.
      return typeof g === 'object' ? (g.genre_id || g.id) : g
    })
  }
  isEditing.value = true
}


const updateInfo = async () => {
  if (!editData.value.email || !editData.value.age || !editData.value.gender) {
    alert('필수 정보를 모두 입력해주세요.')
    return
  }
  if (editData.value.favorite_genres.length === 0) {
    alert('선호 장르를 최소 1개 선택해주세요.')
    return
  }

  try {
    const res = await axios({
      method: 'put',
      url: `${API_URL}/accounts/update/`,
      data: editData.value,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    profile.value = { ...profile.value, ...res.data }
    isEditing.value = false
    alert('회원정보가 수정되었습니다.')
  } catch (err) {
    console.error('수정 실패:', err.response?.data)
    alert('정보 수정에 실패했습니다.')
  }
}

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

</style>