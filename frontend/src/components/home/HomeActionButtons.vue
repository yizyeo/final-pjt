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
      
      <a 
        href="#" 
        class="action-card"
        @click.prevent="handleProtectedMove('/blind-review')"
      >
        <div class="card-top">
          <div class="icon-wrapper">🔮</div>
          <h3 class="card-title">Blind Pick</h3>
          <p class="card-desc">
            영화에 대한 편견을 지우세요.<br />
            오직 리뷰 텍스트로만 선택하는 영화.
          </p>
        </div>
        <div class="card-bottom">
          <span class="service-label">Review Pick</span>
          <span class="icon-arrow">→</span>
        </div>
      </a>

      <a 
        href="#" 
        class="action-card"
        @click.prevent="handleProtectedMove('/recommend-keyword')"
      >
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
      </a>

      <RouterLink to="/worldcup" class="action-card">
        <div class="card-top">
          <div class="icon-wrapper">🏆</div>
          <h3 class="card-title">Movie Worldcup</h3>
          <p class="card-desc">
            가장 끌리는 영화를 골라보세요.<br />
            오직 나를 위한 영화 토너먼트.
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
import { useRouter, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()

// 로그인 체크 및 이동 핸들러
const handleProtectedMove = (path) => {
  if (!accountStore.isLogin) {
    const isConfirmed = confirm('로그인이 필요한 서비스입니다.\n로그인 페이지로 이동하시겠습니까?')
    if (isConfirmed) {
      router.push({ name: 'LogInView' })
    }
    return
  }
  // 로그인 상태라면 정상 이동
  router.push(path)
}
</script>

<style scoped>
.action-container {
  width: 100%;
  padding: 4rem 0 2rem;
}

/* --- 섹션 헤더 --- */
.section-intro {
  text-align: center;
  margin-bottom: 2.5rem;
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
  
  min-height: 240px;
  height: 100%;
  
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  position: relative;
  overflow: hidden;
  cursor: pointer; /* a 태그는 기본적으로 pointer지만 명시 */
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
  margin-bottom: 1.5rem; 
}

/* 하단 영역 */
.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  margin-top: auto;
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

/* 반응형 */
@media (max-width: 1024px) {
  .grid-layout {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .grid-layout {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .action-card {
    min-height: 200px;
  }
}
</style>