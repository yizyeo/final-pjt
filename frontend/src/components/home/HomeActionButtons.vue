<template>
  <div class="action-container">
    
    <div class="section-intro">
      <h2 class="intro-title">나에게 딱 맞는 영화 찾기</h2>
      <p class="intro-desc">
        세 가지 특별한 방법으로 취향을 저격하는<br class="mobile-break" /> 
        완벽한 영화를 발견해보세요.
      </p>
    </div>

    <div class="grid-layout">
      
      <RouterLink to="/blind-review" class="action-card">
        <div class="card-top">
          <div class="icon-wrapper">📝</div>
          <h3 class="card-title">Blind Review</h3>
          <p class="card-desc">
            영화의 편견을 지우세요.<br />
            오직 리뷰 텍스트로만 선택하는 영화.
          </p>
        </div>
        <div class="card-bottom">
          <span class="service-label">Review Pick</span>
          <span class="icon-arrow">→</span>
        </div>
      </RouterLink>

      <RouterLink to="/recommend-keyword" class="action-card">
        <div class="card-top">
          <div class="icon-wrapper">✨</div>
          <h3 class="card-title">Keyword Pick</h3>
          <p class="card-desc">
            오늘 기분은 어떠신가요?<br />
            키워드로 딱 맞는 영화를 찾아드려요.
          </p>
        </div>
        <div class="card-bottom">
          <span class="service-label">AI Recommend</span>
          <span class="icon-arrow">→</span>
        </div>
      </RouterLink>

      <RouterLink to="/worldcup" class="action-card">
        <div class="card-top">
          <div class="icon-wrapper">🏆</div>
          <h3 class="card-title">Movie Worldcup</h3>
          <p class="card-desc">
            최고의 영화를 가려보세요.<br />
            나만의 인생 영화 토너먼트.
          </p>
        </div>
        <div class="card-bottom">
          <span class="service-label">Tournament</span>
          <span class="icon-arrow">→</span>
        </div>
      </RouterLink>

    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.action-container {
  width: 100%;
  padding: 4rem 0 2rem;
}

/* --- 섹션 헤더 --- */
.section-intro {
  text-align: center;
  margin-bottom: 3rem;
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

/* --- 그리드 레이아웃 --- */
.grid-layout {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  /* 카드 높이 통일 (가장 긴 내용 기준) */
  align-items: stretch;
}

/* --- 카드 스타일 --- */
.action-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  
  background-color: #FFFFFF;
  border: 1px solid #EEEEEE;
  border-radius: 16px;
  padding: 2rem;
  
  /* [수정 1] 고정 높이 제거 & 최소 높이 설정 */
  /* height: 280px; -> 삭제 */
  min-height: 240px; /* 내용이 적어도 이 정도 높이는 유지 */
  height: 100%; /* 그리드 셀 높이에 꽉 차게 */
  
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  position: relative;
  overflow: hidden;
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(122, 108, 250, 0.2);
  border-color: #7A6CFA;
  background-color: #F3F0FF;
}

/* 상단 영역 */
.card-top {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.icon-wrapper {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  background-color: #F5F5F5;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  transition: background-color 0.3s;
}

.action-card:hover .icon-wrapper {
  background-color: #FFFFFF; 
  box-shadow: 0 4px 10px rgba(122, 108, 250, 0.1);
}

.card-title {
  color: #111111;
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.card-desc {
  color: #666666;
  font-size: 0.95rem;
  line-height: 1.5;
  font-weight: 500;
  letter-spacing: -0.02em;
  margin-top: 0.5rem;
  /* [수정 2] 하단 여백을 줄여서 푸터가 너무 아래로 쳐지지 않게 조정 */
  margin-bottom: 1.5rem; 
}

/* 하단 영역 */
.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  margin-top: auto; /* 내용이 적어도 바닥에 붙게 유지 */
  padding-top: 1.5rem;
  border-top: 1px solid #F5F5F5;
  transition: border-color 0.3s;
}

.action-card:hover .card-bottom {
  border-color: rgba(122, 108, 250, 0.1); 
}

.service-label {
  color: #7A6CFA;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.icon-arrow {
  color: #DDDDDD;
  font-size: 1.2rem;
  transition: all 0.3s;
}

.action-card:hover .icon-arrow {
  color: #7A6CFA;
  transform: translateX(5px);
}

/* [수정 3] 반응형 브레이크포인트 추가 및 수정 */

/* 1024px 이하 (태블릿 가로/작은 노트북): 2열 배치 */
@media (max-width: 1024px) {
  .grid-layout {
    grid-template-columns: repeat(2, 1fr); /* 3열 -> 2열로 변경 */
  }
}

/* 768px 이하 (모바일): 1열 배치 */
@media (max-width: 768px) {
  .intro-title {
    font-size: 1.5rem;
  }
  
  .intro-desc {
    font-size: 1rem;
  }

  .grid-layout {
    grid-template-columns: 1fr; /* 1열 배치 */
    gap: 1rem;
  }

  .action-card {
    min-height: 200px;
  }

  .mobile-break {
    display: none;
  }
}
</style>