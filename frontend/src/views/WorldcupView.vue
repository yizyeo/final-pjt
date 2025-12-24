<template>
  <div class="worldcup-container">
    <!-- Intro: Mode and Count Selection -->
    <WorldcupIntro 
      v-if="gameState === 'intro'" 
      @start-game="handleStartGame" 
    />

    <!-- Game: Match -->
    <WorldcupMatch 
      v-else-if="gameState === 'playing'"
      :match="currentMatch"
      :roundName="currentRoundName"
      :matchIndex="currentMatchIndex"
      :totalMatches="currentRoundMatches.length"
      @select-winner="selectWinner"
    />

    <!-- Winner -->
    <WorldcupWinner 
      v-else-if="gameState === 'winner'"
      :winner="winner"
      :isWished="!!movieStore.movieDetail?.is_wished"
      @go-to-detail="goToDetail"
      @toggle-wish="addToWishlist"
      @reset-game="resetGame"
    />

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
        alert('로그인이 필요합니다.');
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
    color: white;
    text-align: center;
    padding: 2rem;
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
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
