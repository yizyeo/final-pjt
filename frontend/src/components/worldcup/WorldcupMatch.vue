<template>
  <div class="game-screen">
    
    <div class="section-intro">
      <h2 class="intro-title">{{ roundName }}</h2>
      
      <div class="progress-pill">
        <span class="current">{{ matchIndex + 1 }}</span>
        <span class="divider">/</span>
        <span class="total">{{ totalMatches }}</span>
      </div>

      <p class="intro-desc">
        두 영화 중 더 마음이 가는 작품을<br class="mobile-break" /> 
        선택해주세요.
      </p>
    </div>
    
    <div class="match-container">
      <div 
        class="movie-card left" 
        :key="match[0]?.tmdb_id"
        @click="selectWinner(0)"
      >
          <div class="poster-wrapper">
              <div v-if="playingMovieId === match[0]?.tmdb_id && trailerKey" class="video-container">
                  <iframe 
                    :src="`https://www.youtube.com/embed/${trailerKey}?autoplay=1&controls=0&modestbranding=1`" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen
                  ></iframe>
              </div>
              <template v-else>
                  <img :src="getPosterUrl(match[0]?.poster_path)" :alt="match[0]?.title">
                  <div class="overlay">
                      <span class="select-text">PICK</span>
                  </div>
              </template>
          </div>
          
          <div class="movie-info">
              <h3>{{ match[0]?.title }}</h3>
              <div class="meta-tag">
                <span class="year-badge">{{ getYear(match[0]?.release_date) }}</span>
                <span class="genre-text">{{ getGenreNames(match[0]?.genres) }}</span>
              </div>
              <button class="trailer-btn" @click.stop="toggleTrailer(match[0])">
                {{ playingMovieId === match[0]?.tmdb_id ? '닫기' : '예고편 보기' }}
              </button>
          </div>
      </div>

      <div class="vs-container">
        <div class="vs-circle">
          <span class="vs-text">VS</span>
        </div>
      </div>

      <div 
        class="movie-card right" 
        :key="match[1]?.tmdb_id"
        @click="selectWinner(1)"
      >
          <div class="poster-wrapper">
              <div v-if="playingMovieId === match[1]?.tmdb_id && trailerKey" class="video-container">
                  <iframe 
                    :src="`https://www.youtube.com/embed/${trailerKey}?autoplay=1&controls=0&modestbranding=1`" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen
                  ></iframe>
              </div>
              <template v-else>
                  <img :src="getPosterUrl(match[1]?.poster_path)" :alt="match[1]?.title">
                  <div class="overlay">
                      <span class="select-text">PICK</span>
                  </div>
              </template>
          </div>

          <div class="movie-info">
              <h3>{{ match[1]?.title }}</h3>
              <div class="meta-tag">
                <span class="year-badge">{{ getYear(match[1]?.release_date) }}</span>
                <span class="genre-text">{{ getGenreNames(match[1]?.genres) }}</span>
              </div>
              <button class="trailer-btn" @click.stop="toggleTrailer(match[1])">
                {{ playingMovieId === match[1]?.tmdb_id ? '닫기' : '예고편 보기' }}
              </button>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const props = defineProps({
    match: Array,
    roundName: String,
    matchIndex: Number,
    totalMatches: Number
});

const emit = defineEmits(['select-winner']);
const API_URL = import.meta.env.VITE_API_URL;

const playingMovieId = ref(null);
const trailerKey = ref(null);

const getPosterUrl = (path) => {
    if (!path) return '/placeholder.png';
    return `https://image.tmdb.org/t/p/w500${path}`;
};

const getYear = (dateString) => {
    if (!dateString) return '';
    return dateString.split('-')[0];
}

const getGenreNames = (genres) => {
    if (!genres || genres.length === 0) return '장르 없음';
    return genres[0].name_kr; 
};

const toggleTrailer = async (movie) => {
    if (playingMovieId.value === movie.tmdb_id) {
        playingMovieId.value = null;
        trailerKey.value = null;
        return;
    }

    try {
        const res = await axios.get(`${API_URL}/movies/movie/${movie.tmdb_id}/trailer/`);
        if (res.data.videoId) {
            trailerKey.value = res.data.videoId;
            playingMovieId.value = movie.tmdb_id;
        } else {
            alert('예고편이 없습니다.');
        }
    } catch (err) {
        console.error('Failed to fetch trailer:', err);
        alert('예고편을 불러오는데 실패했습니다.');
    }
};

const selectWinner = (index) => {
    playingMovieId.value = null;
    trailerKey.value = null;
    emit('select-winner', index);
};
</script>

<style scoped>
.game-screen {
    width: 100%;
}

/* --- 1. 헤더 스타일 (Intro와 통일) --- */
.section-intro {
    text-align: center;
    margin-bottom: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.icon-wrapper {
    font-size: 3rem;
    margin-bottom: 1rem;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.intro-title {
    font-size: 2rem;
    font-weight: 800;
    color: #111111;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}

.progress-pill {
    background-color: #F3F0FF;
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 1rem;
    font-weight: 700;
    color: #7A6CFA;
}

.current {
    font-size: 1.1rem;
}

.divider {
    color: #DADADA;
    font-weight: 400;
}

.total {
    color: #A0A0A0;
    font-size: 1.1rem;
}

.intro-desc {
    font-size: 1.1rem;
    color: #666666;
    line-height: 1.6;
    font-weight: 500;
}

/* --- 대진 컨테이너 --- */
.match-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 3rem; /* VS 배지 공간 확보 */
    position: relative;
    padding-top: 1rem;
}

/* --- 카드 디자인 --- */
@keyframes cardEnter {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.movie-card {
    flex: 1;
    max-width: 380px;
    cursor: pointer;
    background: white;
    padding: 1.2rem;
    border-radius: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    border: 2px solid transparent;
    animation: cardEnter 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.movie-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(122, 108, 250, 0.15);
    border-color: #7A6CFA;
}

/* 포스터 래퍼 */
.poster-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 2/3;
    overflow: hidden;
    border-radius: 16px;
    background: #000; /* 비디오 배경을 위해 검정 */
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    display: flex; /* 비디오 중앙 정렬을 위한 flex */
    justify-content: center;
    align-items: center;
}

/* 이미지 */
.poster-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.movie-card:hover .poster-wrapper img {
    transform: scale(1.05);
}

/* 비디오 컨테이너 (수직 중앙 정렬 핵심) */
.video-container {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center; /* 수직 중앙 */
    justify-content: center; /* 수평 중앙 */
    background: black;
}

.video-container iframe {
    width: 100%;
    aspect-ratio: 16/9; /* 비율 고정 */
    height: auto; /* 비율에 맞춰 높이 자동 조절 */
    border: none;
}

/* 오버레이 */
.overlay {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(122, 108, 250, 0.45);
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.3s ease;
    backdrop-filter: blur(2px);
}

.movie-card:hover .poster-wrapper:not(:has(.video-container)) .overlay {
    opacity: 1;
}

.select-text {
    font-size: 1.4rem;
    font-weight: 800;
    color: white;
    letter-spacing: 0.1em;
    border: 2px solid white;
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    background: rgba(255,255,255,0.1);
}

/* 정보 영역 */
.movie-info {
    text-align: center;
}

.movie-info h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 700;
    color: #111111;
    word-break: keep-all;
    line-height: 1.35;
}

.meta-tag {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin-bottom: 1rem;
}

.year-badge {
    background-color: #F1F5F9;
    color: #475569;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 4px 8px;
    border-radius: 6px;
}

.genre-text {
    color: #888888;
    font-size: 0.9rem;
    font-weight: 500;
}

.trailer-btn {
    width: 100%;
    padding: 0.8rem;
    background-color: white;
    color: #666;
    border: 1px solid #EEEEEE;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.2s;
}

.trailer-btn:hover {
    background-color: #7A6CFA;
    color: white;
    border-color: #7A6CFA;
}

/* --- 2. VS 디자인 (깔끔한 버전) --- */
.vs-container {
    align-self: center; 
    z-index: 10;
    margin: 0 -20px; /* 카드 간격 좁히기 */
}

.vs-circle {
    width: 64px;
    height: 64px;
    background: #FFFFFF;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12); /* 부드러운 그림자 */
    position: relative;
}

/* VS 글자 그라데이션 */
.vs-text {
    font-size: 1.6rem;
    font-weight: 900;
    font-style: italic;
    background: linear-gradient(135deg, #7A6CFA 0%, #A29BFE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: sans-serif;
    padding-right: 4px; /* 이탤릭체 보정 */
}

/* 반응형 */
@media (max-width: 768px) {
    .match-container {
        flex-direction: column;
        align-items: center;
        gap: 2rem;
    }

    .vs-container {
        margin: -20px 0;
    }
    
    .movie-card {
        width: 100%;
        max-width: 320px;
    }

    .intro-title {
        font-size: 1.8rem;
    }
}
</style>