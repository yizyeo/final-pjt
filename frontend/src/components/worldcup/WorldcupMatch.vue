<template>
  <div class="game-screen">
    <div class="game-header">
      <h2>{{ roundName }} - {{ matchIndex + 1 }} / {{ totalMatches }}</h2>
    </div>
    
    <div class="match-container">
      <!-- Left Movie -->
      <div class="movie-card left" @click="selectWinner(0)">
          <div class="poster-wrapper">
              <img :src="getPosterUrl(match[0]?.poster_path)" :alt="match[0]?.title">
              <div class="overlay">
                  <span class="select-text">Click to Select</span>
              </div>
          </div>
          <div class="movie-info">
              <h3>{{ match[0]?.title }}</h3>
              <p>{{ match[0]?.release_date }} | {{ getGenreNames(match[0]?.genres) }}</p>
          </div>
      </div>

      <div class="vs-badge">VS</div>

      <!-- Right Movie -->
      <div class="movie-card right" @click="selectWinner(1)">
          <div class="poster-wrapper">
              <img :src="getPosterUrl(match[1]?.poster_path)" :alt="match[1]?.title">
              <div class="overlay">
                  <span class="select-text">Click to Select</span>
              </div>
          </div>
          <div class="movie-info">
              <h3>{{ match[1]?.title }}</h3>
              <p>{{ match[1]?.release_date }} | {{ getGenreNames(match[1]?.genres) }}</p>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
    match: Array,
    roundName: String,
    matchIndex: Number,
    totalMatches: Number
});

const emit = defineEmits(['select-winner']);

const getPosterUrl = (path) => {
    if (!path) return '/placeholder.png';
    return `https://image.tmdb.org/t/p/w500${path}`;
};

const getGenreNames = (genres) => {
    // Placeholder logic from original file
    return '장르'; 
};

const selectWinner = (index) => {
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
}

.poster-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
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

.movie-card:hover .overlay {
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

.vs-badge {
    font-size: 2rem;
    font-weight: bold;
    color: #e50914;
}
</style>
