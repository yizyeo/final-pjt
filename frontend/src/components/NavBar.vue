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
        <input 
          type="text" 
          placeholder="Search movies..." 
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          @focus="showHistory = true"
          @blur="hideHistory"
        />
        <div v-if="showHistory && recentSearches.length > 0" class="search-history">
          <ul>
            <li v-for="(item, index) in recentSearches" :key="index" @mousedown="selectHistory(item)">
              <span>{{ item }}</span>
              <button @mousedown.stop="removeHistory(index)" class="remove-btn">x</button>
            </li>
          </ul>
        </div>
      </div>
      <div v-if="accountStore.isLogin" class="user-info">
        <span>환영합니다, {{ accountStore.username }}님!</span>
          <div class="dropdown">
            <button @click="toggleDropdown" class="dropdown-toggle">▼</button>
            <ul v-show="dropdownOpen" class="dropdown-menu">
              <!-- 연결 링크 바꿔야 함, 일단 홈으로 연결-->
              <li><RouterLink :to="{ name: 'ProfileView', params: { username: accountStore.username } }">마이페이지</RouterLink></li> 
              <li><a href="#" @click.prevent="logOut">로그아웃</a></li>
            </ul>
          </div>
      </div>
      <div v-else class="auth-links">
        <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
        <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';

import { useRouter, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()
const dropdownOpen = ref(false)

// Search logic
const searchQuery = ref('')
const recentSearches = ref([])
const showHistory = ref(false)

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
  const query = searchQuery.value.trim()
  if (!query) return

  // Update history
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
  handleSearch()
}

const removeHistory = (index) => {
  recentSearches.value.splice(index, 1)
  saveHistory()
}

const hideHistory = () => {
  // Delay slightly to allow click event on history item
  setTimeout(() => {
    showHistory.value = false
  }, 200)
}

const logOut = function () {
  dropdownOpen.value = false
  accountStore.logOut()
}

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const goToHome = () => {
  router.push({ name: 'HomeView' })
}

onMounted(() => {
  loadHistory()
})

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

.search-bar {
  position: relative;
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

.search-history {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: rgba(30, 30, 30, 0.95);
  border: 1px solid #555;
  border-radius: 0 0 4px 4px;
  z-index: 1001;
  margin-top: 2px;
}

.search-history ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-history li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  cursor: pointer;
  border-bottom: 1px solid #444;
  font-size: 0.9rem;
  color: #e5e5e5;
}

.search-history li:last-child {
  border-bottom: none;
}

.search-history li:hover {
  background-color: #444;
}

.remove-btn {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
}

.remove-btn:hover {
  color: white;
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
