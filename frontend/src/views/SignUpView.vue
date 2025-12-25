<template>
  <div class="signup-container">
    <div class="signup-card">
      
      <div class="card-header">
        <h1 class="title">회원가입</h1>
        <p class="subtitle">
          {{ step === 1 ? '기본 정보를 입력해주세요' : '상세 정보를 입력해주세요' }}
        </p>
        
        <div class="step-indicator">
          <div class="step-bar" :class="{ active: step >= 1 }"></div>
          <div class="step-bar" :class="{ active: step >= 2 }"></div>
        </div>
      </div>

      <form @submit.prevent="signUp">
        
        <div v-if="step === 1" class="step-content">
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
            <label for="email">이메일</label>
            <input 
              type="email" 
              id="email" 
              v-model.trim="email" 
              class="form-input"
              placeholder="example@email.com"
            >
          </div>

          <div class="form-group">
            <label for="password1">비밀번호</label>
            <input 
              type="password" 
              id="password1" 
              v-model.trim="password1"
              class="form-input"
              placeholder="8자 이상 입력해주세요"
              :class="{ 'error-border': password1.length > 0 && password1.length < 8 }"
            >
            <p v-if="password1.length > 0 && password1.length < 8" class="error-msg">
              비밀번호는 8자 이상이어야 합니다.
            </p>
          </div>

          <div class="form-group">
            <label for="password2">비밀번호 확인</label>
            <input 
              type="password" 
              id="password2" 
              v-model.trim="password2"
              class="form-input"
              placeholder="비밀번호를 한 번 더 입력해주세요"
              :class="{ 'error-border': password2.length > 0 && password1 !== password2 }"
            >
            <p v-if="password2.length > 0 && password1 !== password2" class="error-msg">
              비밀번호가 일치하지 않습니다.
            </p>
          </div>

          <button type="button" class="btn-primary full-width" @click="goNext">
            다음으로
          </button>
        </div>

        <div v-else class="step-content">
          <div class="form-group">
            <label for="age">나이</label>
            <input 
              type="number" 
              id="age" 
              v-model.trim="age" 
              class="form-input"
              placeholder="나이를 입력하세요"
            >
            
          </div>

          <div class="form-group">
            <label>성별</label>
            <div class="gender-selector">
              <label class="gender-btn" :class="{ active: gender === 'M' }">
                <input type="radio" name="gender" value="M" v-model="gender" class="hidden-input">
                남성
              </label>
              <label class="gender-btn" :class="{ active: gender === 'F' }">
                <input type="radio" name="gender" value="F" v-model="gender" class="hidden-input">
                여성
              </label>
            </div>
          </div>

          <div class="form-group">
            <label>
              선호 장르 
              <span class="sub-text">(최소 1개 선택)</span>
            </label>
            
            <div v-if="genres.length > 0" class="genre-grid">
              <label 
                v-for="genre in genres" 
                :key="genre.genre_id" 
                class="genre-chip"
                :class="{ active: favorite_genres.includes(genre.genre_id) }"
              >
                <input
                  type="checkbox"
                  :value="genre.genre_id"
                  v-model="favorite_genres"
                  class="hidden-input"
                >
                {{ genre.name_kr }}
              </label>
            </div>
            <div v-else class="loading-text">
              장르 목록을 불러오는 중...
            </div>
          </div>

          <div class="button-group">
            <button type="button" class="btn-secondary" @click="step = 1">이전</button>
            <button type="submit" class="btn-primary flex-grow">회원가입 완료</button>
          </div>
        </div>

      </form>
      
      <div class="login-link">
        이미 계정이 있으신가요? 
        <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { RouterLink } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL
const accountStore = useAccountStore()

// 단계 제어 (1: 계정정보, 2: 개인정보)
const step = ref(1)

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const email = ref('')
const gender = ref('')
const age = ref(null)
const favorite_genres = ref([])
const genres = ref([])

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/movies/genres/`)
    genres.value = res.data
  } catch (err) {
    console.error('영화 장르 리스트 로딩 실패', err)
  }
})


const goNext = () => {
  if (!username.value || !email.value || !password1.value || !password2.value) {
    alert('모든 필수 정보를 입력해주세요.')
    return
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    alert('유효한 이메일 형식이 아닙니다.')
    return
  }

  if (password1.value.length < 8) {
    alert('비밀번호는 최소 8자 이상이어야 합니다.')
    return
  }

  if (password1.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  step.value = 2
}

const signUp = () => {
  // [STEP 2] 유효성 검사
  if (!age.value) {
    alert('나이를 입력해주세요.')
    return
  }

  if (!gender.value) {
    alert('성별을 선택해주세요.')
    return
  }

  if (favorite_genres.value.length === 0) {
    alert('선호 장르를 최소 1개 선택해주세요.')
    return
  }

  accountStore.signUp({
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    age: age.value,
    gender: gender.value,
    favorite_genres: favorite_genres.value,
  })
}
</script>

<style scoped>
/* 전체 배경 (밝은 회색) */
.signup-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #F8F9FA;
  padding: 2rem 1rem 10rem 1rem;
}

/* 카드 스타일 (흰색 배경 + 그림자) */
.signup-card {
  width: 100%;
  max-width: 480px;
  background-color: #FFFFFF;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  padding: 2.5rem 2rem;
}

/* 헤더 */
.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #111111;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666666;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

/* 단계 표시기 */
.step-indicator {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-bottom: 1rem;
}

.step-bar {
  width: 40px;
  height: 4px;
  background-color: #EEEEEE;
  border-radius: 2px;
  transition: background-color 0.3s;
}

.step-bar.active {
  background-color: #7A6CFA; /* 활성 상태: 보라색 */
}

/* 폼 요소 공통 */
.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  font-size: 0.9rem;
  font-weight: 700;
  color: #333333;
  margin-bottom: 0.5rem;
}

.sub-text {
  font-size: 0.8rem;
  color: #7A6CFA;
  font-weight: 500;
}

/* 입력 필드 (기존 디자인 유지) */
.form-input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #DDDDDD;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #FFFFFF;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #7A6CFA;
  box-shadow: 0 0 0 3px rgba(122, 108, 250, 0.1);
}

.form-input.error-border {
  border-color: #FF4444;
  background-color: #FFF8F8;
}

.error-msg {
  color: #FF4444;
  font-size: 0.8rem;
  margin-top: 6px;
}

/* 성별 선택 (버튼형) */
.hidden-input {
  display: none;
}

.gender-selector {
  display: flex;
  gap: 10px;
}

.gender-btn {
  flex: 1;
  padding: 12px;
  border: 1px solid #EEEEEE;
  background-color: #FAFAFA;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 600;
  color: #555555;
}

.gender-btn:hover {
  background-color: #F0F0F0;
}

.gender-btn.active {
  background-color: #F0EBFF; /* 연한 보라 배경 */
  border-color: #7A6CFA;
  color: #7A6CFA;
}

/* 장르 선택 (칩 형태) */
.genre-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.genre-chip {
  padding: 8px 16px;
  background-color: #F5F5F5;
  border: 1px solid transparent;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #555555;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.genre-chip:hover {
  background-color: #EEEEEE;
}

/* 장르 선택됨: 보라색 배경 + 흰색 글씨 */
.genre-chip.active {
  background-color: #7A6CFA;
  color: white;
  border-color: #7A6CFA;
  box-shadow: 0 4px 10px rgba(122, 108, 250, 0.3);
}

.loading-text {
  font-size: 0.9rem;
  color: #888888;
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #7A6CFA;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 14px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #6656E0;
}

.btn-secondary {
  background-color: #FFFFFF;
  border: 1px solid #DDDDDD;
  color: #555555;
  border-radius: 12px;
  padding: 14px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #F5F5F5;
}

.full-width {
  width: 100%;
  margin-top: 1rem;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 1.5rem;
}

.flex-grow {
  flex: 1;
}

/* 하단 링크 */
.login-link {
  text-align: center;
  margin-top: 2rem;
  font-size: 0.9rem;
  color: #888888;
}

.login-link a {
  color: #7A6CFA;
  text-decoration: none;
  font-weight: 700;
  margin-left: 4px;
}

.login-link a:hover {
  text-decoration: underline;
}

/* 모바일 반응형 */
@media (max-width: 480px) {
  .signup-card {
    padding: 1.5rem;
  }
  
  .title {
    font-size: 1.5rem;
  }
}
</style>