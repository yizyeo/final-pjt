<template>
  <div class="winner-screen">
    
    <div class="winner-header">
      <h1 class="page-title">Winner !</h1>
      <p class="page-desc">
        치열한 경쟁 끝에 선택된 영화입니다.
      </p>
    </div>
    
    <div class="winner-card">
        <div class="poster-wrapper">
             <img :src="getPosterUrl(winner?.poster_path)" :alt="winner?.title" class="winner-poster">
             <div class="crown">👑</div>
        </div>
        
        <div class="winner-info">
            <h2>{{ winner?.title }}</h2>
            <div class="meta-info">
              <span class="date">{{ winner?.release_date?.split('-')[0] }}</span>
              <span class="divider"></span>
              <span class="genres">{{ getGenreNames(winner?.genres) }}</span>
            </div>
        </div>
    </div>

    <div class="action-buttons">
        <button 
          @click="toggleWish" 
          class="action-btn outline"
          :class="{ active: isWished }"
        >
          {{ isWished ? '✅ 등록 완료' : '➕ 볼 영화 등록' }}
        </button>
        <button @click="goToDetail" class="action-btn primary">상세 정보 보기</button>
        <button @click="resetGame" class="action-btn text-only">다시 하기</button>
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
    // 3. 구분자 변경 (, -> ·)
    return genres.map(g => g.name_kr).join(' · ');
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
.winner-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* --- 1. 헤더 스타일 개선 --- */
.winner-header {
    text-align: center;
    margin-bottom: 2.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.page-title {
    font-size: 2rem;
    font-weight: 800;
    color: #111111;
    margin-bottom: 0.5rem;
    letter-spacing: -0.03em;
}

.page-desc {
    font-size: 1.1rem;
    color: #666666;
    line-height: 1.6;
}

/* --- 카드 스타일 --- */
.winner-card {
    background: white;
    padding: 2rem;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid #EEEEEE;
    margin-bottom: 2rem;
    width: 100%;
    max-width: 340px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

/* 배경 장식 (선택 사항 - 은은한 빛) */
.winner-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(122,108,250,0.05) 0%, rgba(255,255,255,0) 70%);
    pointer-events: none;
}

.poster-wrapper {
    position: relative;
    width: 180px; /* 포스터 크기 적절히 고정 */
    margin: 0 auto 1.5rem;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.winner-poster {
    width: 100%;
    border-radius: 12px;
    display: block;
}

.crown {
    position: absolute;
    top: -30px;
    left: 50%;
    transform: translateX(-50%) rotate(-5deg);
    font-size: 3rem;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    animation: bounce 2s infinite;
    z-index: 10;
}

@keyframes bounce {
  0%, 100% { transform: translateX(-50%) rotate(-5deg) translateY(0); }
  50% { transform: translateX(-50%) rotate(-5deg) translateY(-8px); }
}

.winner-info h2 {
    margin: 0 0 0.8rem 0;
    font-size: 1.5rem;
    font-weight: 800;
    color: #111111;
    word-break: keep-all;
    line-height: 1.3;
}

.meta-info {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    color: #666666;
    font-size: 0.95rem;
}

.divider {
    width: 1px;
    height: 12px;
    background-color: #DDDDDD;
}

.date {
    font-weight: 500;
}

.genres {
    color: #7A6CFA;
    font-weight: 600;
}

/* --- 버튼 그룹 --- */
.action-buttons {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    max-width: 340px;
}

.action-btn {
    padding: 1rem;
    border-radius: 16px;
    font-weight: 700;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
}

/* Primary Button */
.action-btn.primary {
    background-color: #7A6CFA;
    color: white;
    box-shadow: 0 4px 12px rgba(122, 108, 250, 0.3);
}

.action-btn.primary:hover {
    background-color: #695AE0;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(122, 108, 250, 0.4);
}

/* Outline Button */
.action-btn.outline {
    background-color: white;
    border: 2px solid #EEEEEE;
    color: #333333;
}

.action-btn.outline:hover {
    background-color: #F9F9F9;
    border-color: #BBBBBB;
    transform: translateY(-2px);
}

.action-btn.outline.active {
    background-color: #F0FFF4; /* 아주 연한 초록색 배경 */
    border-color: #48BB78;
    color: #2F855A;
}

/* Text Only Button */
.action-btn.text-only {
    background-color: transparent;
    color: #888888;
    font-size: 0.95rem;
    padding: 0.5rem;
    font-weight: 500;
}

.action-btn.text-only:hover {
    color: #333333;
    text-decoration: underline;
}

@media (max-width: 480px) {
    .page-title {
        font-size: 1.6rem;
    }
}
</style>