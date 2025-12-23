<template>
  <div class="game-screen">
    <div class="game-header">
      <h2>{{ roundName }} - {{ matchIndex + 1 }} / {{ totalMatches }}</h2>
    </div>
    
    <div class="match-container">
      <!-- Left Movie -->
      <div class="movie-card left" @click="selectWinner(0)">
          <div class="poster-wrapper">
              <div v-if="playingMovieId === match[0]?.tmdb_id && trailerKey" class="video-container">
                  <iframe 
                    :src="`https://www.youtube.com/embed/${trailerKey}?autoplay=1`" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen
                  ></iframe>
              </div>
              <template v-else>
                  <img :src="getPosterUrl(match[0]?.poster_path)" :alt="match[0]?.title">
                  <div class="overlay">
                      <span class="select-text">Click to Select</span>
                  </div>
              </template>
          </div>
          <div class="movie-info">
              <h3>{{ match[0]?.title }}</h3>
              <p>{{ match[0]?.release_date }} | {{ getGenreNames(match[0]?.genres) }}</p>
              <button class="trailer-btn" @click.stop="toggleTrailer(match[0])">
                {{ playingMovieId === match[0]?.tmdb_id ? '예고편 닫기' : '예고편 보기' }}
              </button>
          </div>
      </div>

      <div class="vs-badge">VS</div>

      <!-- Right Movie -->
      <div class="movie-card right" @click="selectWinner(1)">
          <div class="poster-wrapper">
              <div v-if="playingMovieId === match[1]?.tmdb_id && trailerKey" class="video-container">
                  <iframe 
                    :src="`https://www.youtube.com/embed/${trailerKey}?autoplay=1`" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen
                  ></iframe>
              </div>
              <template v-else>
                  <img :src="getPosterUrl(match[1]?.poster_path)" :alt="match[1]?.title">
                  <div class="overlay">
                      <span class="select-text">Click to Select</span>
                  </div>
              </template>
          </div>
          <div class="movie-info">
              <h3>{{ match[1]?.title }}</h3>
              <p>{{ match[1]?.release_date }} | {{ getGenreNames(match[1]?.genres) }}</p>
              <button class="trailer-btn" @click.stop="toggleTrailer(match[1])">
                {{ playingMovieId === match[1]?.tmdb_id ? '예고편 닫기' : '예고편 보기' }}
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

const getGenreNames = (genres) => {
    if (!genres || genres.length === 0) return '장르 없음';
    return genres[0].name_kr; 
};

const toggleTrailer = async (movie) => {
    // If clicking the same movie that is playing, stop it
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
    // Reset trailer when moving to next match
    playingMovieId.value = null;
    trailerKey.value = null;
    emit('select-winner', index);
};
</script>

<style scoped>
.game-header {
    margin-bottom: 2rem;
}

.match-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
}

.movie-card {
    flex: 1;
    max-width: 400px;
    cursor: pointer;
    transition: transform 0.2s;
    border: 2px solid transparent;
}

.movie-card:hover {
    transform: scale(1.02);
    border-color: #e50914;
}

.poster-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 2/3;
    overflow: hidden;
    border-radius: 8px;
    background: black;
}

.poster-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.video-container {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    background: black;
}

.video-container iframe {
    width: 100%;
    aspect-ratio: 16/9; 
    height: auto;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.2s;
}

/* Only show overlay if not playing video */
.movie-card:hover .poster-wrapper:not(:has(.video-container)) .overlay {
    opacity: 1;
}

.select-text {
    font-size: 1.5rem;
    font-weight: bold;
    border: 2px solid white;
    padding: 0.5rem 1rem;
}

.movie-info {
    margin-top: 1rem;
}

.movie-info h3 {
    margin: 0;
    font-size: 1.2rem;
}

.movie-info p {
    color: #ccc;
    font-size: 0.9rem;
}

.trailer-btn {
    margin-top: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: #333;
    color: white;
    border: 1px solid #555;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.trailer-btn:hover {
    background-color: #555;
}

.vs-badge {
    font-size: 2rem;
    font-weight: bold;
    color: #e50914;
}
</style>
