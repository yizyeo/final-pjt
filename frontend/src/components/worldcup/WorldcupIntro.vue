<template>
  <div class="intro-container">
    
    <div class="section-intro">
      <div class="icon-wrapper">🏆</div>
      <h2 class="intro-title">나만의 영화 월드컵</h2>
      <p class="intro-desc">
        두근거리는 선택의 순간!<br class="mobile-break" />
        더 마음에 드는 영화를 골라보세요.
      </p>
    </div>

    <div class="options-container">
      
      <div class="option-group">
        <h3 class="option-label">1. 추천 방식</h3>
        <div class="mode-grid">
          <div 
            class="mode-card" 
            :class="{ active: mode === 'random' }"
            @click="mode = 'random'"
          >
            <span class="mode-icon">🎲</span>
            <div class="mode-text">
              <h4>랜덤 매치</h4>
              <p>무작위 영화 대결</p>
            </div>
            <div class="check-circle"></div>
          </div>

          <div 
            class="mode-card" 
            :class="{ active: mode === 'user' }"
            @click="mode = 'user'"
          >
            <span class="mode-icon">👤</span>
            <div class="mode-text">
              <h4>취향 매치</h4>
              <p>내 취향 기반 추천</p>
            </div>
            <div class="check-circle"></div>
          </div>
        </div>
      </div>

      <div class="option-group">
        <h3 class="option-label">2. 라운드 수</h3>
        <div class="round-grid">
          <button 
            v-for="cnt in [4, 8, 16]" 
            :key="cnt"
            class="round-btn"
            :class="{ active: selectedRound === cnt }"
            @click="selectedRound = cnt"
          >
            {{ cnt }}강
          </button>
        </div>
      </div>

    </div>

    <button class="start-btn" @click="startGame">
      Game Start
    </button>

  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['start-game']);

// 상태 관리
const mode = ref('random');      // 기본값: 랜덤
const selectedRound = ref(16);   // 기본값: 16강

// 게임 시작 함수
const startGame = () => {
  emit('start-game', { count: selectedRound.value, mode: mode.value });
};
</script>

<style scoped>
.intro-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
}

/* --- 1. 헤더 스타일 (HomeView와 통일) --- */
.section-intro {
  text-align: center;
  margin-bottom: 3rem;
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
  margin-bottom: 0.8rem;
  letter-spacing: -0.03em;
}

.intro-desc {
  font-size: 1.1rem;
  color: #666666;
  line-height: 1.6;
  font-weight: 500;
}

/* --- 2. 옵션 영역 --- */
.options-container {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  margin-bottom: 3rem;
}

.option-label {
  font-size: 1rem;
  font-weight: 700;
  color: #333333;
  margin-bottom: 1rem;
  display: block;
}

/* 모드 카드 그리드 */
.mode-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.mode-card {
  background: white;
  border: 2px solid #EEEEEE;
  border-radius: 16px;
  padding: 1.5rem 1rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.mode-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* 선택된 모드 스타일 */
.mode-card.active {
  border-color: #7A6CFA;
  background-color: #F8F7FF;
}

.mode-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.mode-text h4 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111111;
  margin-bottom: 0.2rem;
}

.mode-text p {
  font-size: 0.85rem;
  color: #888888;
}

/* 체크 아이콘 (우측 상단) */
.check-circle {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 20px;
  height: 20px;
  border: 2px solid #DDDDDD;
  border-radius: 50%;
  transition: all 0.2s;
}

.mode-card.active .check-circle {
  background-color: #7A6CFA;
  border-color: #7A6CFA;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white' width='12px' height='12px'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
}

/* 라운드 버튼 그리드 */
.round-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.round-btn {
  padding: 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: #666666;
  background-color: #F5F5F5;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.round-btn:hover {
  background-color: #EEEEEE;
  color: #111111;
}

/* 선택된 라운드 스타일 */
.round-btn.active {
  background-color: #111111;
  color: #FFFFFF;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

/* --- 3. 시작 버튼 --- */
.start-btn {
  width: 100%;
  padding: 1.2rem;
  background-color: #7A6CFA;
  color: white;
  font-size: 1.2rem;
  font-weight: 700;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(122, 108, 250, 0.3);
}

.start-btn:hover {
  background-color: #695AE0;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(122, 108, 250, 0.4);
}

.start-btn:active {
  transform: translateY(0);
}

/* 모바일 반응형 */
@media (max-width: 640px) {
  .mode-grid {
    grid-template-columns: 1fr; /* 모바일에서 세로 배치 */
  }
}
</style>