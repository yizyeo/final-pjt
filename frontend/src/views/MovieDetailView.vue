<template>
  <div class="page-container">
    
    <button @click="router.back()" class="back-btn-floating" title="뒤로가기">
      <span class="icon">←</span>
    </button>

    <div v-if="!movieStore.movieDetail" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else>
      <section 
        class="hero-banner"
        :style="movieStore.movieDetail.backdrop_paths?.length 
          ? { backgroundImage: `url(https://image.tmdb.org/t/p/original${movieStore.movieDetail.backdrop_paths[0]})` }
          : { backgroundColor: '#111' }"
      >
        <div class="hero-overlay"></div>
        
        <div class="content-wrapper hero-content">
          <div class="text-area">
            <h1 class="movie-title">{{ movieStore.movieDetail.title }}</h1>
            
            <div class="movie-meta-col">
              <p class="meta-item">{{ movieStore.movieDetail.release_date?.slice(0, 4) }}</p>
              
              <p class="meta-item" v-if="movieStore.movieDetail.genres?.length">
                <span v-for="(genre, idx) in movieStore.movieDetail.genres" :key="genre.id">
                  {{ genre.name_kr }}{{ idx < movieStore.movieDetail.genres.length - 1 ? ' · ' : '' }}
                </span>
              </p>
              
              <p class="meta-item">{{ movieStore.movieDetail.runtime }}분</p>
            </div>
          </div>
        </div>
      </section>

      <main class="content-wrapper main-body">
        
        <div class="top-section">
          <div class="poster-wrapper">
            <img 
              v-if="movieStore.movieDetail.poster_path"
              :src="`https://image.tmdb.org/t/p/w500${movieStore.movieDetail.poster_path}`" 
              :alt="movieStore.movieDetail.title"
              class="main-poster"
            >
            <div v-else class="no-poster">포스터 없음</div>
          </div>

          <div class="info-wrapper">
            
            <div class="rating-info">
              <div class="score-box">
                <span class="star">⭐</span>
                <span class="score">{{ (movieStore.movieDetail.vote_average / 2).toFixed(1) }}</span>
              </div>
            </div>

            <div class="overview-short">
              {{ movieStore.movieDetail.overview || "등록된 줄거리가 없습니다." }}
            </div>

            <div class="action-row">
              <button 
                @click="movieStore.toggleLike(movieId)" 
                class="action-item"
                :class="{ 'active': movieStore.movieDetail.is_liked }"
              >
                <div class="icon-circle">
                  <span>{{ movieStore.movieDetail.is_liked ? '❤️' : '🤍' }}</span>
                </div>
                <span class="action-label">좋아요</span>
              </button>

              <button 
                @click="movieStore.toggleWish(movieId)" 
                class="action-item"
                :class="{ 'active': movieStore.movieDetail.is_wished }"
              >
                <div class="icon-circle">
                  <span>{{ movieStore.movieDetail.is_wished ? '🏷️' : '🔖' }}</span>
                </div>
                <span class="action-label">볼래요</span>
              </button>

              <button 
                @click="movieStore.toggleWatched(movieId)" 
                class="action-item"
                :class="{ 'active': movieStore.movieDetail.is_watched }"
              >
                <div class="icon-circle">
                  <span>{{ movieStore.movieDetail.is_watched ? '✅' : '☑️' }}</span>
                </div>
                <span class="action-label">봤어요</span>
              </button>

              <div class="vertical-line"></div>

              <button @click="openTrailer" class="action-item trailer-btn">
                <div class="icon-circle play">
                  <span>▶</span>
                </div>
                <span class="action-label">예고편</span>
              </button>
            </div>
          </div>
        </div>

        <div class="tab-menu">
          <button 
            class="tab-btn" 
            :class="{ active: currentTab === 'info' }" 
            @click="currentTab = 'info'"
          >
            상세정보
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: currentTab === 'review' }" 
            @click="currentTab = 'review'"
          >
            실관람평 <span class="review-cnt">({{ reviewStore.movieReviews.length }})</span>
          </button>
        </div>

        <div class="tab-content">
          
          <div v-if="currentTab === 'info'" class="info-tab">
            
            <section class="detail-section" v-if="movieStore.movieDetail.credits">
              <h3 class="section-title">감독 및 출연진</h3>
              <div class="cast-grid-wrapper">
                <div v-if="movieStore.movieDetail.credits.directors?.length > 0" class="cast-group">
                  <div class="cast-role-label">감독</div>
                  <div class="cast-names">
                    {{ movieStore.movieDetail.credits.directors.join(', ') }}
                  </div>
                </div>
                <div v-if="movieStore.movieDetail.credits.actors?.length > 0" class="cast-group mt-3">
                  <div class="cast-role-label">출연</div>
                  <div class="cast-names">
                    {{ movieStore.movieDetail.credits.actors.join(', ') }}
                  </div>
                </div>
              </div>
            </section>

            <div class="divider-line"></div>

            <section v-if="movieStore.movieDetail.backdrop_paths?.length" class="detail-section">
              <h3 class="section-title">갤러리</h3>
              <div class="gallery-grid">
                <img 
                  v-for="(path, idx) in movieStore.movieDetail.backdrop_paths.slice(0, 4)" 
                  :key="idx"
                  :src="`https://image.tmdb.org/t/p/w500${path}`" 
                  class="gallery-item"
                >
              </div>
            </section>
          </div>

          <div v-if="currentTab === 'review'" class="review-tab">
            <div class="review-layout">
              <div class="write-area">
                <ReviewForm v-if="accountStore.isLogin" :moviePk="movieId" />
                <div v-else class="login-plz">
                  로그인 후 리뷰를 남겨보세요.
                  <router-link :to="{ name: 'LogInView' }" class="login-link">로그인</router-link>
                </div>
              </div>
              
              <div class="list-area">
                <ReviewItem 
                  v-for="review in reviewStore.movieReviews" 
                  :key="review.id" 
                  :review="review"
                  @like="reviewStore.likeReview"
                  @go-profile="goProfile"
                />
                <p v-if="!reviewStore.movieReviews.length" class="no-reviews">
                  첫 리뷰를 남겨주세요!
                </p>
              </div>
            </div>
          </div>

        </div>

      </main>
    </div>

    <YoutubeTrailer 
      v-if="showTrailerModal"
      :show="showTrailerModal" 
      :video-id="movieStore.trailerKey" 
      @close="closeTrailer" 
    />
  </div>
  </template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useReviewStore } from '@/stores/review'
import { useMovieStore } from '@/stores/movie'

import ReviewForm from '@/components/review/ReviewForm.vue'
import ReviewItem from '@/components/review/ReviewItem.vue'
import YoutubeTrailer from '@/components/movies/YoutubeTrailer.vue'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const reviewStore = useReviewStore()
const movieStore = useMovieStore()

const movieId = route.params.movieId
const showTrailerModal = ref(false)
const currentTab = ref('info') 

const openTrailer = async () => {
  await movieStore.fetchTrailer(movieId)
  if (movieStore.trailerKey) {
    showTrailerModal.value = true
  } else {
    alert('재생할 수 있는 예고편이 없습니다.')
  }
}

const closeTrailer = () => {
  showTrailerModal.value = false
}

const goProfile = (username) => {
  router.push({ name: 'ProfileView', params: { username: username } })
}

onMounted(() => {
  movieStore.fetchMovieDetail(movieId)
  reviewStore.fetchMovieReviews(movieId)
})
</script>

<style scoped>
/* 페이지 기본 설정 */
.page-container {
  width: 100%;
  background-color: #FFFFFF;
  min-height: 100vh;
  position: relative; /* 버튼 배치를 위해 */
  padding-bottom: 5rem;
}

.back-btn-floating {
  position: absolute;
  top: 2rem;
  left: 2rem;
  z-index: 100; /* 히어로 배너 위에 올라오도록 */
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 2.5rem;
  font-weight: 100;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: all 0.3s ease;
}

.back-btn-floating:hover {
  color: rgba(255, 255, 255, 1); /* 호버 시 밝게 */
  transform: translateX(-5px);
}

.content-wrapper {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 1.5rem;
  width: 100%;
}

/* Hero Banner */
.hero-banner {
  position: relative;
  width: 100%;
  height: 550px;
  background-size: cover;
  background-position: center top;
  display: flex;
  align-items: flex-end; /* 콘텐츠를 바닥으로 정렬 */
}

.hero-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.4) 60%, rgba(0,0,0,0.8) 100%);
}

.hero-content {
  position: relative;
  z-index: 2;
  padding-bottom: 2.5rem; /* PC 기준 하단 여백 */
  color: white;
}

.movie-title {
  font-size: 2.8rem;
  font-weight: 800;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
  line-height: 1.2;
}

.movie-meta-col {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.meta-item {
  font-size: 1.1rem;
  font-weight: 500;
  opacity: 0.95;
  margin: 0;
}

/* Top Section */
.main-body { padding-top: 2.5rem; }

.top-section {
  display: flex;
  gap: 3rem;
  margin-bottom: 4rem;
  align-items: stretch;
}

.poster-wrapper {
  flex-shrink: 0;
  width: 280px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  background-color: #EEE;
}

.main-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.no-poster {
  width: 100%; height: 400px;
  display: flex; align-items: center; justify-content: center;
  color: #AAA; font-weight: 600;
}

.info-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 5px 0;
}

.rating-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.score-box {
  display: flex;
  align-items: center;
  gap: 4px;
}
.star { color: #FFB800; font-size: 1.4rem; }
.score { font-size: 1.8rem; font-weight: 800; color: #333; }
.count { font-size: 0.95rem; color: #888; margin-top: 4px; }

.overview-short {
  font-size: 1.05rem;
  color: #444;
  line-height: 1.7;
  flex-grow: 1;
  margin-top: 3rem;
  margin-bottom: 2rem;
  white-space: pre-line;
  max-height: 200px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #DDD transparent;
}

.action-row {
  display: flex;
  align-items: center;
  gap: 2rem;
  border-top: 1px solid #F0F0F0;
  padding-top: 1.5rem;
}

.action-item {
  background: none; border: none; padding: 0;
  cursor: pointer;
  display: flex; flex-direction: column; align-items: center;
  gap: 8px; color: #888;
  transition: all 0.2s;
}

.icon-circle {
  width: 54px; height: 54px;
  border-radius: 50%; border: 1px solid #E0E0E0;
  display: flex; justify-content: center; align-items: center;
  font-size: 1.4rem; background: white;
  transition: all 0.2s;
}

.action-label { font-size: 0.85rem; font-weight: 600; }

.action-item:hover { color: #555; }
.action-item:hover .icon-circle { transform: scale(1.05); border-color: #CCC; }

.action-item.active .icon-circle {
  border-color: #7A6CFA; background-color: #7A6CFA; color: white;
}
.action-item.active .action-label { color: #7A6CFA; font-weight: 700; }

.vertical-line { width: 1px; height: 40px; background-color: #EEE; margin: 0 5px; }
.play { border-color: #7A6CFA; color: #7A6CFA; }

/* Tabs */
.tab-menu {
  display: flex;
  border-bottom: 1px solid #EEE;
  margin-bottom: 2.5rem;
}

.tab-btn {
  padding: 1rem 2rem;
  background: none; border: none;
  font-size: 1.1rem; font-weight: 600; color: #888;
  cursor: pointer; position: relative;
}

.tab-btn.active { color: #7A6CFA; font-weight: 700; }
.tab-btn.active::after {
  content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 3px; background: #7A6CFA;
}
.review-cnt { font-weight: 400; font-size: 0.9rem; }

/* Details */
.section-title { font-size: 1.4rem; font-weight: 800; color: #111; margin-bottom: 1.2rem; }
.divider-line { height: 1px; background: #F0F0F0; margin: 3rem 0; }

.cast-grid-wrapper {
  background-color: #F8F9FA;
  padding: 2rem;
  border-radius: 12px;
}
.cast-group { display: flex; align-items: flex-start; gap: 1.5rem; }
.cast-role-label { font-weight: 700; color: #333; width: 60px; flex-shrink: 0; }
.cast-names { color: #555; line-height: 1.6; }
.mt-3 { margin-top: 1.5rem; }

.gallery-grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;
}
.gallery-item {
  width: 100%; border-radius: 10px; cursor: pointer; transition: opacity 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.gallery-item:hover { opacity: 0.8; }

/* Review */
.review-layout { display: flex; flex-direction: column; gap: 2rem; }
.write-area { background: #FAFAFA; padding: 2rem; border-radius: 12px; }
.login-plz { text-align: center; color: #666; }
.login-link { color: #7A6CFA; font-weight: 700; margin-left: 5px; }
.no-reviews { text-align: center; color: #AAA; padding: 4rem; }

/* Loading */
.loading-state { height: 100vh; display: flex; justify-content: center; align-items: center; }
.spinner { width: 40px; height: 40px; border: 4px solid #EEE; border-top-color: #7A6CFA; border-radius: 50%; animation: spin 1s infinite linear; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Mobile */
@media (max-width: 768px) {
  /* [수정] 모바일에서 뒤로가기 버튼 위치 조정 */
  .back-btn-floating {
    top: 1rem;
    left: 1rem;
    font-size: 2rem;
  }

  .hero-banner { height: 550px; }
  .movie-title { font-size: 2rem; }
  .content-wrapper { padding: 0 1rem; }

  .hero-content {
    padding-bottom: 5rem;
  }

  .top-section {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    text-align: center;
  }

  .poster-wrapper { width: 180px; margin-top: -80px; z-index: 10; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
  
  .info-wrapper { align-items: center; }
  .rating-info { justify-content: center; }
  .overview-short { text-align: center; margin-top: 1.5rem; margin-bottom: 2rem; }
  
  .action-row { 
    gap: 1rem; 
    justify-content: center; 
    flex-wrap: wrap; 
    border-top: none; 
    padding-top: 0;
  }
  .icon-circle { width: 48px; height: 48px; font-size: 1.2rem; }
  
  .gallery-grid { grid-template-columns: 1fr; }
}
</style>