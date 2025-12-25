<template>
  <div class="worldcup-container">
    <WorldcupIntro 
      v-if="gameState === 'intro'" 
      @start-game="handleStartGame" 
    />

    <WorldcupMatch 
      v-else-if="gameState === 'playing'"
      :match="currentMatch"
      :roundName="currentRoundName"
      :matchIndex="currentMatchIndex"
      :totalMatches="currentRoundMatches.length"
      @select-winner="selectWinner"
    />

    <WorldcupWinner 
      v-else-if="gameState === 'winner'"
      :winner="winner"
      :isWished="!!movieStore.movieDetail?.is_wished"
      @go-to-detail="goToDetail"
      @toggle-wish="addToWishlist"
      @reset-game="resetGame"
    />

    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAccountStore } from '@/stores/accounts';
import { useMovieStore } from '@/stores/movie';

import WorldcupIntro from '@/components/worldcup/WorldcupIntro.vue';
import WorldcupMatch from '@/components/worldcup/WorldcupMatch.vue';
import WorldcupWinner from '@/components/worldcup/WorldcupWinner.vue';

const router = useRouter();
const accountStore = useAccountStore();
const movieStore = useMovieStore();
const API_URL = import.meta.env.VITE_API_URL;

// State
const gameState = ref('intro'); // intro, playing, winner
const movies = ref([]);
const roundMovies = ref([]); // Movies participating in the current round
const nextRoundMovies = ref([]); // Winners of the current round
const currentMatchIndex = ref(0);
const winner = ref(null);
const loading = ref(false);

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
const shuffle = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
};

const handleStartGame = async ({ count, mode }) => {
    loading.value = true;
    try {
        const endpoint = mode === 'user' ? 'user' : 'random';
        
        // 헤더 설정 (로그인 상태라면 토큰 포함)
        const headers = {};
        if (accountStore.token) {
            headers.Authorization = `Token ${accountStore.token}`;
        }

        const res = await axios.get(`${API_URL}/movies/worldcup/${endpoint}/`, {
            params: { count },
            headers: headers
        });
        
        movies.value = res.data;
        // Shuffle movies just in case backend didn't or for extra randomness
        roundMovies.value = movies.value;
        nextRoundMovies.value = [];
        currentMatchIndex.value = 0;
        gameState.value = 'playing';
    } catch (err) {
        console.error('Failed to start game:', err);
        if (err.response && err.response.status === 401) {
            alert('로그인이 필요한 서비스입니다.');
            router.push({ name: 'LogInView' });
        } else {
            alert('게임을 시작할 수 없습니다.');
        }
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
            roundMovies.value = shuffle([...nextRoundMovies.value]);
            nextRoundMovies.value = [];
            currentMatchIndex.value = 0;
        }
    }
};

const checkWishStatus = async (movieId) => {
    if (!accountStore.isLogin) return;
    await movieStore.fetchMovieDetail(movieId);
};

const addToWishlist = async (movie) => {
    if (!accountStore.isLogin) {
        alert('로그인이 필요한 서비스입니다.');
        router.push({ name: 'LogInView' });
        return;
    }
    
    await movieStore.toggleWish(movie.tmdb_id);
};

const goToDetail = (id) => {
    router.push({ name: 'MovieDetailView', params: { movieId: id } });
};

const resetGame = () => {
    gameState.value = 'intro';
    winner.value = null;
    movies.value = [];
    movieStore.movieDetail = null; // Reset movie detail
};

</script>

<style scoped>
.worldcup-container {
    color: #0F172A; /* 다크 모드 해제: 짙은 남색 텍스트 */
    background-color: #FFFFFF; /* 배경 흰색 */
    text-align: center;
    padding: 2rem 1rem;
    min-height: calc(100vh - 80px); /* 네비바 높이 고려 */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.9); /* 흰색 반투명 배경 */
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
    font-weight: 600;
    color: #7A6CFA;
    z-index: 1000;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #EEEEEE;
    border-top: 4px solid #7A6CFA;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>