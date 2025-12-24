<template>
  <div class="login-container">
    <div class="login-card">
      
      <div class="card-header">
        <h1 class="title">로그인</h1>
        <p class="subtitle">반갑습니다! 다시 만나서 기뻐요 👋</p>
      </div>

      <form @submit.prevent="logIn">
        
        <div class="form-group">
          <label for="username">아이디</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username" 
            class="form-input"
            placeholder="아이디를 입력하세요"
          >
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input 
            type="password" 
            id="password" 
            v-model.trim="password" 
            class="form-input"
            placeholder="비밀번호를 입력하세요"
          >
        </div>

        <button type="submit" class="btn-primary full-width">로그인</button>

      </form>

      <div class="signup-link">
        아직 계정이 없으신가요? 
        <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { RouterLink } from 'vue-router'

const accountStore = useAccountStore()

const username = ref('')
const password = ref('')

const logIn = function () {
  if (!username.value || !password.value) {
    alert('아이디와 비밀번호를 모두 입력해주세요.')
    return
  }

  const payload = {
    username: username.value,
    password: password.value,
  }
  accountStore.logIn(payload)
}
</script>

<style scoped>
/* 전체 배경 (회원가입 페이지와 동일) */
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #F8F9FA;
  
  /* 박스를 화면 중앙보다 살짝 위로 올림 */
  padding: 2rem 1rem 10rem 1rem; 
}

/* 카드 스타일 */
.login-card {
  width: 100%;
  max-width: 420px; /* 로그인 창은 입력이 적어서 조금 더 좁게 */
  background-color: #FFFFFF;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  padding: 3rem 2.5rem;
}

/* 헤더 */
.card-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.title {
  font-size: 2rem;
  font-weight: 800;
  color: #111111;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666666;
  font-size: 0.95rem;
}

/* 폼 요소 */
.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-size: 0.9rem;
  font-weight: 700;
  color: #333333;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #DDDDDD;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #FFFFFF;
  font-family: inherit; /* 폰트 상속 */
}

.form-input:focus {
  outline: none;
  border-color: #7A6CFA;
  box-shadow: 0 0 0 3px rgba(122, 108, 250, 0.1);
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #7A6CFA;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #6656E0;
}

.full-width {
  width: 100%;
  margin-top: 1rem;
}

/* 하단 링크 */
.signup-link {
  text-align: center;
  margin-top: 2rem;
  font-size: 0.9rem;
  color: #888888;
}

.signup-link a {
  color: #7A6CFA;
  text-decoration: none;
  font-weight: 700;
  margin-left: 4px;
}

.signup-link a:hover {
  text-decoration: underline;
}

/* 모바일 반응형 */
@media (max-width: 480px) {
  .login-card {
    padding: 2rem 1.5rem;
  }
  
  .title {
    font-size: 1.8rem;
  }
}
</style>