<template>
  <nav class="navbar">
    <div class="navbar-left">
      <a href="#" @click.prevent="goToHome" class="navbar-brand">
        <span class="icon">🎬</span>
        <span class="text">Home</span>
      </a>
    </div>
    <div class="navbar-right">
      <div class="search-bar">
        <input type="text" placeholder="Search movies..." />
      </div>
      
      <!-- Logged In State -->
      <div v-if="isLoggedIn" class="user-info">
        <span>환영합니다, {{ username }}님!</span>
        <div class="dropdown">
          <button @click="toggleDropdown" class="dropdown-toggle">▼</button>
          <ul v-show="dropdownOpen" class="dropdown-menu">
            <li><a href="#">마이페이지</a></li>
            <li><a href="#">개인정보수정</a></li>
            <li><a href="#" @click.prevent="logout">로그아웃</a></li>
          </ul>
        </div>
      </div>

      <!-- Logged Out State -->
      <div v-else class="auth-links">
        <a href="#">Login</a>
        <a href="#">Signup</a>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

// 실제 인증 상태를 대신하는 임시 데이터입니다.
// 실제 앱에서는 Pinia와 같은 상태 관리 라이브러리에서 가져와야 합니다.
const isLoggedIn = ref(true); // 기본적으로 로그인된 상태로 설정
const username = ref('Gemini'); // 임시 사용자 이름

const dropdownOpen = ref(false);

const goToHome = () => {
  // 추후 router.push('/') 등을 사용하여 메인 페이지로 이동합니다.
  console.log('Navigate to home');
};

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

const logout = () => {
  isLoggedIn.value = false;
  dropdownOpen.value = false; // 로그아웃 시 드롭다운 닫기
  // 실제 앱에서는 토큰 삭제 및 로그아웃 API를 호출해야 합니다.
  console.log('User logged out');
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 2rem;
  background-color: #141414;
  color: white;
  font-family: Arial, sans-serif;
  border-bottom: 1px solid #333;
}

.navbar-brand {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-brand .icon {
  margin-right: 0.5rem;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.search-bar input {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #555;
  background-color: #333;
  color: white;
  font-size: 0.9rem;
}

.search-bar input::placeholder {
  color: #aaa;
}

.auth-links a, .user-info span {
  color: #e5e5e5;
  text-decoration: none;
  margin-left: 1rem;
  font-size: 0.9rem;
}

.auth-links a:hover {
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
}

.dropdown {
  position: relative;
  display: inline-block;
  margin-left: 0.75rem;
}

.dropdown-toggle {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 0.8rem;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 150%;
  background-color: #222;
  border: 1px solid #444;
  list-style: none;
  padding: 0.5rem 0;
  margin: 0;
  border-radius: 4px;
  width: 160px;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

.dropdown-menu li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #e5e5e5;
  text-decoration: none;
  font-size: 0.9rem;
}

.dropdown-menu li a:hover {
  background-color: #333;
  color: white;
}
</style>
