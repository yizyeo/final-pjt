<template>
  <div class="movie-filter-wrapper">
    
    <div class="filter-group">
      <span class="label">장르</span>
      <div class="custom-dropdown-wrapper">
        <div 
          class="dropdown-trigger" 
          :class="{ active: showGenreDropdown }"
          @click="toggleGenreDropdown"
        >
          <span class="selected-text">{{ selectedGenreLabel }}</span>
          <span class="arrow-icon" :class="{ rotated: showGenreDropdown }">▼</span>
        </div>

        <ul v-if="showGenreDropdown" class="dropdown-list">
          <li 
            @click.stop="selectGenre(null)" 
            class="dropdown-item all"
          >
            모든 장르
          </li>
          <li 
            v-for="genre in genres" 
            :key="genre.genre_id" 
            @click.stop="selectGenre(genre.genre_id)"
            class="dropdown-item"
            :class="{ active: selectedGenre === genre.genre_id }"
          >
            {{ genre.name_kr }}
          </li>
        </ul>
      </div>
    </div>

    <div class="filter-group">
      <span class="label">개봉년도</span>
      <div class="custom-dropdown-wrapper">
        <input 
          type="text"
          v-model="inputYear" 
          @focus="openYearDropdown"
          @click="openYearDropdown"
          @input="handleYearInput"
          @keydown.enter="applyYearFilter"
          placeholder="모든 연도"
          class="custom-input"
          autocomplete="off"
        >
        
        <ul v-if="showYearDropdown" class="dropdown-list">
          <li @mousedown.prevent="selectYear(null)" class="dropdown-item all">
            모든 연도 보기
          </li>
          <li 
            v-for="year in filteredYears" 
            :key="year" 
            @mousedown.prevent="selectYear(year)"
            class="dropdown-item"
            :class="{ active: selectedYear === year }"
          >
            {{ year }}
          </li>
          <li v-if="filteredYears.length === 0" class="dropdown-item empty">
            결과 없음
          </li>
        </ul>
      </div>
    </div>

    <button @click="resetFilter" class="reset-btn">
      필터 초기화
    </button>

    <div v-if="showGenreDropdown || showYearDropdown" class="overlay" @click="closeAllDropdowns"></div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['filter-change'])
const API_URL = import.meta.env.VITE_API_URL

const genres = ref([])
const years = ref([])
const selectedGenre = ref(null)
const selectedYear = ref(null)
const inputYear = ref('')
const showGenreDropdown = ref(false)
const showYearDropdown = ref(false)

const fetchGenres = async () => {
  try {
    const res = await axios.get(`${API_URL}/movies/genres/`)
    genres.value = res.data
  } catch (err) {
    console.error('장르 로드 실패:', err)
  }
}

const generateYears = () => {
  const currentYear = new Date().getFullYear()
  for (let i = currentYear; i >= 1900; i--) {
    years.value.push(i)
  }
}

const selectedGenreLabel = computed(() => {
  if (!selectedGenre.value) return '모든 장르'
  const found = genres.value.find(g => g.genre_id === selectedGenre.value)
  return found ? found.name_kr : '모든 장르'
})

const filteredYears = computed(() => {
  if (!inputYear.value) return years.value
  return years.value.filter(year => String(year).includes(inputYear.value))
})

const toggleGenreDropdown = () => {
  showGenreDropdown.value = !showGenreDropdown.value
  showYearDropdown.value = false
}

const selectGenre = (genreId) => {
  selectedGenre.value = genreId
  showGenreDropdown.value = false
  emitFilter()
}

const openYearDropdown = () => { 
  showYearDropdown.value = true 
  showGenreDropdown.value = false
}
const handleYearInput = () => { showYearDropdown.value = true }

const selectYear = (year) => {
  selectedYear.value = year
  inputYear.value = year ? String(year) : ''
  showYearDropdown.value = false
  emitFilter()
}

const applyYearFilter = () => {
  if (inputYear.value === '') {
    selectYear(null)
    return
  }
  const year = parseInt(inputYear.value)
  if (years.value.includes(year)) {
    selectYear(year)
  }
}

const closeAllDropdowns = () => {
  showGenreDropdown.value = false
  showYearDropdown.value = false
}

const emitFilter = () => {
  emit('filter-change', {
    genre: selectedGenre.value,
    year: selectedYear.value
  })
}

const resetFilter = () => {
  selectedGenre.value = null
  selectedYear.value = null
  inputYear.value = ''
  closeAllDropdowns()
  emitFilter()
}

onMounted(() => {
  fetchGenres()
  generateYears()
})
</script>

<style scoped>
/* 전체 컨테이너: 배경색 제거 */
.movie-filter-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
  /* background-color, border, padding 제거 */
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.label {
  font-size: 0.95rem;
  font-weight: 700;
  color: #444;
}

/* 드롭다운 래퍼 */
.custom-dropdown-wrapper {
  position: relative;
  width: 140px;
}

/* 장르 트리거 */
.dropdown-trigger {
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.9rem;
  color: #333;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s;
  height: 40px; /* 높이 고정 */
}

.dropdown-trigger:hover, .dropdown-trigger.active {
  border-color: #7A6CFA;
  box-shadow: 0 0 0 2px rgba(122, 108, 250, 0.1);
}

.selected-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 90px;
}

/* 연도 Input */
.custom-input {
  width: 100%;
  height: 40px; /* 높이 고정 */
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.9rem;
  color: #333;
  transition: all 0.2s;
}

.custom-input:focus {
  border-color: #7A6CFA;
  box-shadow: 0 0 0 2px rgba(122, 108, 250, 0.1);
  outline: none;
}

/* 화살표 아이콘 */
.arrow-icon {
  font-size: 0.7rem;
  color: #AAA;
  transition: transform 0.2s;
}
.arrow-icon.rotated {
  transform: rotate(180deg);
  color: #7A6CFA;
}

/* 드롭다운 리스트 */
.dropdown-list {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  width: 100%;
  max-height: 260px;
  overflow-y: auto;
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 12px;
  padding: 6px;
  list-style: none;
  z-index: 100;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.dropdown-list::-webkit-scrollbar { width: 6px; }
.dropdown-list::-webkit-scrollbar-track { background: transparent; }
.dropdown-list::-webkit-scrollbar-thumb { background-color: #DDD; border-radius: 3px; }
.dropdown-list::-webkit-scrollbar-thumb:hover { background-color: #CCC; }

.dropdown-item {
  padding: 10px 12px;
  font-size: 0.9rem;
  color: #444;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.1s ease;
  margin-bottom: 2px;
}

.dropdown-item:hover {
  background-color: #F3F0FF;
  color: #7A6CFA;
  font-weight: 500;
}

.dropdown-item.active {
  background-color: #7A6CFA;
  color: #FFFFFF;
  font-weight: 600;
}

.dropdown-item.all {
  color: #7A6CFA;
  font-weight: 600;
  border-bottom: 1px solid #F5F5F5;
  margin-bottom: 4px;
}
.dropdown-item.all:hover { background-color: #F3F0FF; }

.dropdown-item.empty {
  color: #AAA;
  cursor: default;
  text-align: center;
  padding: 20px 0;
}

/* [수정] 초기화 버튼 (버튼 스타일 적용) */
.reset-btn {
  height: 40px;
  background-color: #FFFFFF; /* 흰색 배경 */
  border: 1px solid #E0E0E0; /* 테두리 */
  color: #7A6CFA; /* 보라색 텍스트 */
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0 16px;
  border-radius: 8px;
  transition: all 0.2s;
  margin-left: auto; /* 우측 끝으로 */
}

.reset-btn:hover {
  background-color: #F3F0FF;
  border-color: #7A6CFA;
}

/* 오버레이 */
.overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  z-index: 99;
  cursor: default;
}

/* 반응형 */
@media (max-width: 768px) {
  .movie-filter-wrapper {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .filter-group {
    justify-content: space-between;
  }
  
  .custom-dropdown-wrapper {
    width: 65%; 
  }
  
  .reset-btn {
    width: 100%;
    margin-left: 0;
    margin-top: 4px;
  }
}
</style>