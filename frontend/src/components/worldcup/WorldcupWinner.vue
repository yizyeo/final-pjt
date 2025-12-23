<template>
  <div class="winner-screen">
    <h1>🏆 우승 🏆</h1>
    
    <div class="winner-card">
        <img :src="getPosterUrl(winner?.poster_path)" :alt="winner?.title" class="winner-poster">
        <div class="winner-info">
            <h2>{{ winner?.title }}</h2>
            <p>{{ winner?.release_date }}</p>
            <p class="genres">{{ getGenreNames(winner?.genres) }}</p>
        </div>
    </div>

    <div class="action-buttons">
        <button @click="goToDetail">자세히 보기</button>
        <button @click="toggleWish" :class="{ active: isWished }">
            {{ isWished ? '볼 영화에서 삭제' : '볼 영화 추가' }}
        </button>
        <button @click="resetGame">한번 더 하기</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
    winner: Object,
    isWished: Boolean
});

const emit = defineEmits(['go-to-detail', 'toggle-wish', 'reset-game']);

const getPosterUrl = (path) => {
    if (!path) return '/placeholder.png';
    return `https://image.tmdb.org/t/p/w500${path}`;
};

const getGenreNames = (genres) => {
    if (!genres || genres.length === 0) return '장르 없음';
    return genres.map(g => g.name_kr).join(', ');
};

const goToDetail = () => {
    emit('go-to-detail', props.winner?.tmdb_id);
};

const toggleWish = () => {
    emit('toggle-wish', props.winner);
};

const resetGame = () => {
    emit('reset-game');
};
</script>

<style scoped>
.winner-card {
    margin: 2rem auto;
    max-width: 300px;
}

.winner-poster {
    width: 100%;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(229, 9, 20, 0.5);
}

.winner-info {
    margin-top: 1rem;
}

.winner-info h2 {
    margin: 0;
}

.winner-info p {
    color: #ccc;
    margin: 0.5rem 0;
}

.action-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
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

button:hover {
    background-color: #555;
}

button.active {
    background-color: #e50914;
    border-color: #e50914;
}
</style>
