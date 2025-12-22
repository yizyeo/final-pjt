<template>
  <div class="intro-screen">
    <h1>영화 이상형 월드컵</h1>
    
    <div class="selection-section">
      <h3>1. 추천 방식 선택</h3>
      <div class="button-group">
          <button 
              :class="{ active: mode === 'random' }" 
              @click="setMode('random')"
          >
              랜덤 추천
          </button>
          <button 
              :class="{ active: mode === 'user' }" 
              @click="setMode('user')"
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
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['start-game']);
const mode = ref('random');

const setMode = (selectedMode) => {
    mode.value = selectedMode;
};

const startGame = (count) => {
    emit('start-game', { count, mode: mode.value });
};
</script>

<style scoped>
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
</style>
