<template>
  <nav class="navbar">
    <div class="navbar-content">
      <a href="#" @click.prevent="goToHome" class="navbar-brand">
        <span class="logo-text">mootti</span>
      </a>

      <div class="desktop-menu">
        <div class="nav-links">
          <a href="" @click.prevent="goToMovieList" :class="{ active: route.name === 'MovieListView' }">영화</a>
          <a href="" @click.prevent="goToReviewList" :class="{ active: route.name === 'ReviewListView' }">리뷰</a>
        </div>

        <div class="navbar-right">
          <div class="search-container">
            <div class="search-bar" :class="{ 'focused': showHistory }">
              <span class="search-icon">🔍</span>
              <input 
                type="text" 
                placeholder="영화를 검색해보세요!" 
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                @focus="showHistory = true"
                @blur="hideHistory"
              />
            </div>
            <div v-if="showHistory && recentSearches.length > 0" class="search-history glass-panel">
              <div class="history-header">최근 검색어</div>
              <ul>
                <li v-for="(item, index) in recentSearches" :key="index" @mousedown="selectHistory(item)">
                  <span class="history-item">{{ item }}</span>
                  <button @mousedown.stop="removeHistory(index)" class="remove-btn">×</button>
                </li>
              </ul>
            </div>
          </div>

          <div v-if="accountStore.isLogin" class="user-info">
            <div class="dropdown">
              <button @click="toggleDropdown" class="profile-btn">
                <span class="username">{{ accountStore.username }}님</span>
                <span class="chevron">▼</span>
              </button>
              <ul v-show="dropdownOpen" class="dropdown-menu">
                <li><RouterLink :to="{ name: 'ProfileView', params: { username: accountStore.username } }">마이페이지</RouterLink></li> 
                <li><a href="#" @click.prevent="logOut">로그아웃</a></li>
              </ul>
            </div>
          </div>
          <div v-else class="auth-links">
            <RouterLink :to="{ name: 'LogInView' }" class="login-link">로그인</RouterLink>
            <RouterLink :to="{ name: 'SignUpView' }" class="signup-btn">회원가입</RouterLink>
          </div>
        </div>
      </div>

      <button class="hamburger-btn" @click="toggleMobileMenu" :class="{ 'active': isMobileMenuOpen }">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </button>
    </div>

    <transition name="slide-fade">
      <div v-if="isMobileMenuOpen" class="mobile-menu-container glass-panel">
        
        <div class="mobile-search">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            placeholder="영화를" 
            v-model="searchQuery"
            @keyup.enter="handleMobileSearch"
          />
        </div>

        <div class="mobile-links">
          <a href="" @click.prevent="goToMovieList" :class="{ active: route.name === 'MovieListView' }">영화</a>
          <a href="" @click.prevent="goToReviewList" :class="{ active: route.name === 'ReviewListView' }">리뷰</a>
        </div>

        <div class="mobile-divider"></div>

        <div v-if="accountStore.isLogin" class="mobile-auth">
          <div class="mobile-user-profile">
            <span class="username">{{ accountStore.username }}님</span>
          </div>
          <RouterLink :to="{ name: 'ProfileView', params: { username: accountStore.username } }" class="mobile-link">마이페이지</RouterLink>
          <a href="#" @click.prevent="logOut" class="mobile-link logout">로그아웃</a>
        </div>
        <div v-else class="mobile-auth-buttons">
          <RouterLink :to="{ name: 'LogInView' }" class="mobile-login-btn">로그인</RouterLink>
          <RouterLink :to="{ name: 'SignUpView' }" class="mobile-signup-btn">회원가입</RouterLink>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const dropdownOpen = ref(false)
const isMobileMenuOpen = ref(false) // 모바일 메뉴 상태

// Search logic
const searchQuery = ref('')
const recentSearches = ref([])
const showHistory = ref(false)

// 라우트 변경 시 메뉴 닫기 (모바일 UX)
watch(() => route.name, (newName) => {
  if (newName !== 'SearchView') {
    searchQuery.value = ''
  }
  isMobileMenuOpen.value = false // 페이지 이동 시 모바일 메뉴 닫기
})

const loadHistory = () => {
  const history = localStorage.getItem('searchHistory')
  if (history) {
    recentSearches.value = JSON.parse(history)
  }
}

const saveHistory = () => {
  localStorage.setItem('searchHistory', JSON.stringify(recentSearches.value))
}

const handleSearch = () => {
  performSearch(searchQuery.value)
}

const handleMobileSearch = () => {
  performSearch(searchQuery.value)
  isMobileMenuOpen.value = false
}

const performSearch = (queryInput) => {
  const query = queryInput.trim()
  if (!query) return

  const index = recentSearches.value.indexOf(query)
  if (index > -1) {
    recentSearches.value.splice(index, 1)
  }
  recentSearches.value.unshift(query)
  if (recentSearches.value.length > 10) {
    recentSearches.value.pop()
  }
  saveHistory()
  
  showHistory.value = false
  router.push({ name: 'SearchView', query: { q: query } })
}

const selectHistory = (item) => {
  searchQuery.value = item
  performSearch(item)
}

const removeHistory = (index) => {
  recentSearches.value.splice(index, 1)
  saveHistory()
}

const hideHistory = () => {
  setTimeout(() => {
    showHistory.value = false
  }, 200)
}

const logOut = function () {
  dropdownOpen.value = false
  isMobileMenuOpen.value = false
  accountStore.logOut()
}

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const goToHome = () => {
  router.push({ name: 'HomeView' })
}

const goToMovieList = () => {
  router.push({ name: 'MovieListView' })
}

const goToReviewList = () => {
  router.push({ name: 'ReviewListView' })
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
/* =========================================
   1. Base Navbar Styles (Desktop First)
   ========================================= */
.navbar {
  position: sticky;
  top: 0;
  width: 100%;
  height: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  
  /* Glass Effect */
  background-color: rgba(255, 255, 255, 0.95); 
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid #EEEEEE; /* Neutral Gray Border */
}

.navbar-content {
  width: 100%;
  /* [수정] 1280px -> 1080px로 축소하여 중앙 집중 */
  max-width: 1080px; 
  padding: 0 1.5rem; /* 좌우 여백도 살짝 조정 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin: 0 auto; /* 중앙 정렬 필수 */
}

/* Brand */
.navbar-brand {
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  z-index: 1002; /* 햄버거 메뉴보다 위에 */
}

.logo-text {
  color: #111111;
}

/* Desktop Menu Container */
.desktop-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-left: 3rem;
}

/* Links */
.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  color: #666666;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.nav-links a:hover, .nav-links a.active {
  color: #7A6CFA; /* Point Color */
  transform: translateY(-1px);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* Search Bar (Desktop) */
.search-container {
  position: relative;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #F5F5F5;
  border: 1px solid transparent;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  width: 240px;
  transition: all 0.3s ease;
}

.search-bar.focused {
  background-color: #FFFFFF;
  border-color: #7A6CFA;
  box-shadow: 0 0 0 4px rgba(122, 108, 250, 0.15);
  width: 280px;
}

.search-icon {
  font-size: 0.9rem;
  margin-right: 0.5rem;
  opacity: 0.6;
  color: #888888;
}

.search-bar input {
  border: none;
  background: none;
  outline: none;
  width: 100%;
  font-size: 0.95rem;
  color: #111111;
}

.search-bar input::placeholder {
  color: #AAAAAA;
}

/* Auth Links (Desktop) */
.auth-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.login-link {
  color: #666666;
  font-weight: 600;
  font-size: 0.95rem;
}

.login-link:hover {
  color: #111111;
}

.signup-btn {
  padding: 0.5rem 1.2rem;
  background-color: #7A6CFA;
  color: white;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(122, 108, 250, 0.4);
}

.signup-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(122, 108, 250, 0.5);
  opacity: 0.95;
}

/* User Profile (Desktop) */
.user-info {
  display: flex;
  align-items: center;
  height: 100%;
}

.dropdown {
  position: relative;
  display: flex;
  align-items: center;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 160px;
  padding: 0.5rem;
  z-index: 2000;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border: 1px solid #EEEEEE;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  list-style: none;
  margin: 0;
}

.dropdown-menu li a {
  display: block;
  padding: 0.7rem 1rem;
  color: #333333;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.2s;
  text-decoration: none;
}

.dropdown-menu li a:hover {
  background-color: #F5F5F5;
  color: #7A6CFA;
}

.profile-btn {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  transition: background 0.2s;
}

.profile-btn:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.username {
  font-weight: 600;
  color: #111111;
  font-size: 0.95rem;
}

.chevron {
  font-size: 0.7rem;
  color: #999999;
  margin-top: 2px;
}

/* Search History (Shared) */
.glass-panel {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border: 1px solid #EEEEEE;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  border-radius: 16px;
  overflow: hidden;
}

.search-history {
  position: absolute;
  top: 120%;
  right: 0;
  width: 100%;
  left: 0;
  z-index: 1001;
}

.history-header {
  padding: 0.75rem 1rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #888888;
  background-color: #FAFAFA;
}

.search-history li {
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 0.9rem;
  color: #333333;
}

.search-history li:hover {
  background-color: #F5F5F5;
}

.remove-btn {
  background: none;
  border: none;
  color: #CCCCCC;
  font-size: 1.2rem;
  cursor: pointer;
}

/* =========================================
   2. Mobile Styles (Responsiveness)
   ========================================= */

/* 햄버거 버튼 (기본 숨김) */
.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 24px;
  height: 18px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 1002;
}

.hamburger-btn .bar {
  width: 100%;
  height: 2px;
  background-color: #111111;
  border-radius: 2px;
  transition: all 0.3s ease;
}

/* 햄버거 버튼 활성화 애니메이션 */
.hamburger-btn.active .bar:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.hamburger-btn.active .bar:nth-child(2) {
  opacity: 0;
}
.hamburger-btn.active .bar:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

/* 768px 이하 (태블릿/모바일) */
@media (max-width: 768px) {
  .desktop-menu {
    display: none; /* 데스크탑 메뉴 숨김 */
  }

  .hamburger-btn {
    display: flex; /* 햄버거 버튼 표시 */
  }

  .navbar-content {
    padding: 0 1.5rem; /* 패딩 축소 */
  }
}

/* --- Mobile Menu Container --- */
.mobile-menu-container {
  position: absolute;
  top: 70px; /* 네비게이션 바 높이만큼 띄움 */
  left: 0;
  width: 100%;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  border-radius: 0 0 20px 20px;
  border-top: none;
  z-index: 999;
}

/* Mobile Search */
.mobile-search {
  display: flex;
  align-items: center;
  background-color: #F5F5F5;
  border-radius: 12px;
  padding: 0.8rem 1rem;
}

.mobile-search input {
  border: none;
  background: none;
  outline: none;
  width: 100%;
  margin-left: 0.5rem;
  font-size: 1rem;
}

/* Mobile Links */
.mobile-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-links a {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333333;
  padding: 0.5rem 0;
}

.mobile-links a.active {
  color: #7A6CFA;
}

.mobile-divider {
  height: 1px;
  background-color: #EEEEEE;
  width: 100%;
}

/* Mobile Auth */
.mobile-auth {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-user-profile {
  font-weight: 700;
  color: #111111;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.mobile-link {
  color: #666666;
  text-decoration: none;
  font-weight: 500;
}

.mobile-link.logout {
  color: #FF4444;
}

.mobile-auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.mobile-login-btn {
  text-align: center;
  padding: 0.8rem;
  color: #666666;
  font-weight: 600;
  border-radius: 12px;
  background-color: #F5F5F5;
}

.mobile-signup-btn {
  text-align: center;
  padding: 0.8rem;
  background-color: #7A6CFA;
  color: white;
  font-weight: 700;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(122, 108, 250, 0.3);
}

/* Slide Animation */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>