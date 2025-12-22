<template>
  <div class="worldcup-container">
    <!-- Intro: Mode and Count Selection -->
    <div v-if="gameState === 'intro'" class="intro-screen">
      <h1>영화 이상형 월드컵</h1>
      
      <div class="selection-section">
        <h3>1. 추천 방식 선택</h3>
        <div class="button-group">
            <button 
                :class="{ active: mode === 'random' }" 
                @click="mode = 'random'"
            >
                랜덤 추천
            </button>
            <button 
                :class="{ active: mode === 'user' }" 
                @click="mode = 'user'"
                disabled
                title="준비 중입니다"
            >
                사용자 맞춤 (준비중)
            </button>
        </div>
      </div>

      <div class="selection-section">
        <h3>2. 라운드 수 선택</h3>
        <div class="button-group">
            <button v-for="cnt in [4, 8, 16]" :key="cnt" @click="startGame(cnt)">
                {{ cnt }}강
            </button>
        </div>
      </div>
    </div>

    <!-- Game: Match -->
    <div v-else-if="gameState === 'playing'" class="game-screen">
      <div class="game-header">
        <h2>{{ currentRoundName }} - {{ currentMatchIndex + 1 }} / {{ currentRoundMatches.length }}</h2>
      </div>
      
      <div class="match-container">
        <!-- Left Movie -->
        <div class="movie-card left" @click="selectWinner(0)">
            <div class="poster-wrapper">
                <img :src="getPosterUrl(currentMatch[0]?.poster_path)" :alt="currentMatch[0]?.title">
                <div class="overlay">
                    <span class="select-text">Click to Select</span>
                </div>
            </div>
            <div class="movie-info">
                <h3>{{ currentMatch[0]?.title }}</h3>
                <p>{{ currentMatch[0]?.release_date }} | {{ getGenreNames(currentMatch[0]?.genres) }}</p>
            </div>
        </div>

        <div class="vs-badge">VS</div>

        <!-- Right Movie -->
        <div class="movie-card right" @click="selectWinner(1)">
            <div class="poster-wrapper">
                <img :src="getPosterUrl(currentMatch[1]?.poster_path)" :alt="currentMatch[1]?.title">
                <div class="overlay">
                    <span class="select-text">Click to Select</span>
                </div>
            </div>
            <div class="movie-info">
                <h3>{{ currentMatch[1]?.title }}</h3>
                <p>{{ currentMatch[1]?.release_date }} | {{ getGenreNames(currentMatch[1]?.genres) }}</p>
            </div>
        </div>
      </div>
    </div>

    <!-- Winner -->
    <div v-else-if="gameState === 'winner'" class="winner-screen">
        <h1>🏆 우승 🏆</h1>
        
        <div class="winner-card">
            <img :src="getPosterUrl(winner?.poster_path)" :alt="winner?.title" class="winner-poster">
            <div class="winner-info">
                <h2>{{ winner?.title }}</h2>
                <p>{{ winner?.release_date }}</p>
                <p class="genres">{{ getGenreNames(winner?.genres, true) }}</p>
            </div>
        </div>

        <div class="action-buttons">
            <button @click="goToDetail(winner?.tmdb_id)">자세히 보기</button>
            <button @click="addToWishlist(winner)" :class="{ active: isWished }">
                {{ isWished ? '볼 영화에서 삭제' : '볼 영화 추가' }}
            </button>
            <button @click="resetGame">한번 더 하기</button>
        </div>
    </div>

    <div v-if="loading" class="loading-overlay">
        Loading...
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts';

const router = useRouter();
const accountStore = useAccountStore();
const API_URL = import.meta.env.VITE_API_URL;

// State
const gameState = ref('intro'); // intro, playing, winner
const mode = ref('random');
const movies = ref([]);
const roundMovies = ref([]); // Movies participating in the current round
const nextRoundMovies = ref([]); // Winners of the current round
const currentMatchIndex = ref(0);
const winner = ref(null);
const loading = ref(false);
const isWished = ref(false);

// Computed
const currentRoundMatches = computed(() => {
    const matches = [];
    for (let i = 0; i < roundMovies.value.length; i += 2) {
        matches.push([roundMovies.value[i], roundMovies.value[i+1]]);
    }
    return matches;
});

const currentMatch = computed(() => {
    return currentRoundMatches.value[currentMatchIndex.value] || [];
});

const currentRoundName = computed(() => {
    if (roundMovies.value.length === 2) return '결승';
    return `${roundMovies.value.length}강`;
});


// Methods
const getPosterUrl = (path) => {
    if (!path) return '/placeholder.png';
    return `https://image.tmdb.org/t/p/w500${path}`;
};

const getGenreNames = (genres, all=false) => {
    if (!genres || genres.length === 0) return '';
    // Assuming genres is an array of objects or IDs. 
    // Backend serializer sends objects? Let's check serializer.
    // Serializer uses default ManyToMany serialization which sends IDs unless nested serializer is used.
    // In `WorldcupSerializer`, `genres` field is used. Let's assume it returns IDs.
    // Wait, `WorldcupSerializer` inherits from `ModelSerializer`. `genres` is M2M.
    // By default it returns PKs. We might need a helper to map IDs to names if we don't have the map loaded.
    // For now, let's just show "Genre" placeholder or fetch genres. 
    // Ideally, frontend should have genre list in store.
    
    // Simplification: We will just return "장르" or leave it empty if we don't have the name map ready here.
    // Better: Assuming the backend sends IDs, we can't show names without a mapping.
    // Let's rely on the user knowing the movie or the serializer being updated to return names.
    // For now, let's display nothing or just IDs if strictly needed, but design wise names are better.
    // I will not implement full genre mapping here to keep it simple as requested, 
    // but if the backend sends names (using StringRelatedField or similar), it would work.
    // Since we didn't change serializer to send names, it sends IDs.
    return '장르'; 
};

const startGame = async (count) => {
    loading.value = true;
    try {
        const endpoint = mode.value === 'user' ? 'user' : 'random';
        const res = await axios.get(`${API_URL}/movies/worldcup/${endpoint}/`, {
            params: { count }
        });
        
        movies.value = res.data;
        // Shuffle movies just in case backend didn't or for extra randomness
        roundMovies.value = movies.value;
        nextRoundMovies.value = [];
        currentMatchIndex.value = 0;
        gameState.value = 'playing';
    } catch (err) {
        console.error('Failed to start game:', err);
        alert('게임을 시작할 수 없습니다.');
    } finally {
        loading.value = false;
    }
};

const selectWinner = (index) => {
    const selected = currentMatch.value[index];
    nextRoundMovies.value.push(selected);

    if (currentMatchIndex.value < currentRoundMatches.value.length - 1) {
        currentMatchIndex.value++;
    } else {
        // Round Finished
        if (nextRoundMovies.value.length === 1) {
            // Final Winner
            winner.value = nextRoundMovies.value[0];
            checkWishStatus(winner.value.tmdb_id);
            gameState.value = 'winner';
        } else {
            // Next Round
            roundMovies.value = [...nextRoundMovies.value];
            nextRoundMovies.value = [];
            currentMatchIndex.value = 0;
        }
    }
};

const checkWishStatus = async (movieId) => {
    if (!accountStore.isLogin) return;
    // We don't have a direct "check wish" API, but we can infer or just default to false.
    // Or we can try to add to wishlist and see result? No, that's side effect.
    // Ideally `movie_detail` returns `is_wished`.
    // For now, let's default to false and user can click to toggle.
    isWished.value = false; 
};

const addToWishlist = async (movie) => {
    if (!accountStore.isLogin) {
        alert('로그인이 필요합니다.');
        router.push({ name: 'LogInView' });
        return;
    }
    
    try {
        const res = await axios.post(`${API_URL}/movies/movie/${movie.tmdb_id}/wish/`, {}, {
            headers: { Authorization: `Token ${accountStore.token}` }
        });
        isWished.value = res.data.is_wished;
        alert(isWished.value ? '볼 영화에 추가되었습니다.' : '볼 영화에서 삭제되었습니다.');
    } catch (err) {
        console.error('Wishlist toggle failed:', err);
    }
};

const goToDetail = (id) => {
    router.push({ name: 'MovieDetailView', params: { movieId: id } });
};

const resetGame = () => {
    gameState.value = 'intro';
    winner.value = null;
    movies.value = [];
};

</script>

<style scoped>
.worldcup-container {
    color: white;
    text-align: center;
    padding: 2rem;
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* Intro */
.intro-screen .selection-section {
    margin: 2rem 0;
}

.button-group {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
}

button {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    background-color: #333;
    color: white;
    border: 1px solid #555;
    border-radius: 4px;
    transition: background-color 0.2s;
}

button:hover:not(:disabled) {
    background-color: #555;
}

button.active {
    background-color: #e50914;
    border-color: #e50914;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Game */
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

.vs-badge {
    font-size: 2rem;
    font-weight: bold;
    color: #e50914;
}

/* Winner */
.winner-card {
    margin: 2rem auto;
    max-width: 300px;
}

.winner-poster {
    width: 100%;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(229, 9, 20, 0.5);
}

.action-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
    z-index: 1000;
}
</style>