<template>
  <div class="filter-container">
    <div class="filter-item">
      <label>장르: </label>
      <select v-model="selectedGenre" @change="emitFilter">
        <option :value="null">전체</option>
        <option v-for="genre in genres" :key="genre.genre_id" :value="genre.genre_id">
          {{ genre.name_kr }}
        </option>
      </select>
    </div>
    
    <div class="filter-item">
      <label>개봉 연도: </label>
      <div class="year-selector">
        <input 
          type="text"
          v-model="inputYear" 
          @focus="openDropdown"
          @click="openDropdown"
          @input="handleInput"
          @blur="closeDropdown"
          @keydown.enter="applyYearFilter"
          placeholder="연도 검색/선택"
          autocomplete="off"
        >
        <ul v-show="showDropdown" class="year-dropdown">
          <li 
            v-for="year in years" 
            :key="year" 
            @mousedown.prevent="selectYear(year)"
            class="year-option"
          >
            {{ year }}
          </li>
          <li v-if="filteredYears.length === 0" class="no-result">
            결과 없음
          </li>
        </ul>
      </div>
    </div>

    <button @click="resetFilter" class="reset-btn">필터 초기화</button>
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

// Custom Dropdown State
const inputYear = ref('')
const showDropdown = ref(false)

const fetchGenres = async () => {
  try {
    const res = await axios.get(`${API_URL}/movies/genres/`)
    genres.value = res.data
  } catch (err) {
    console.error('장르 목록을 불러오는데 실패했습니다.', err)
  }
}

const generateYears = () => {
  const currentYear = new Date().getFullYear()
  for (let i = currentYear + 0; i >= 1900; i--) {
    years.value.push(i)
  }
}

const filteredYears = computed(() => {
  if (!inputYear.value) return years.value
  return years.value.filter(year => String(year).includes(inputYear.value))
})

const openDropdown = () => {
  showDropdown.value = true
}

const handleInput = () => {
  showDropdown.value = true
}

const closeDropdown = () => {
  // blur 시 바로 닫히면 클릭 이벤트를 못 받을 수 있으므로 mousedown.prevent를 사용하거나 delay를 줌
  // 여기서는 li에 @mousedown.prevent를 사용하여 blur가 발생하지 않게 처리함
  showDropdown.value = false
}

const selectYear = (year) => {
  inputYear.value = String(year)
  selectedYear.value = year
  showDropdown.value = false
  emitFilter()
}

const applyYearFilter = () => {
  // 입력된 값이 유효한 연도인지 확인하거나, 그냥 입력된 값으로 검색
  // 여기서는 목록에 있는 연도인 경우에만 필터 적용, 비어있으면 초기화
  if (inputYear.value === '') {
    selectedYear.value = null
    emitFilter()
    showDropdown.value = false
    return
  }

  const year = parseInt(inputYear.value)
  if (years.value.includes(year)) {
    selectedYear.value = year
    emitFilter()
  } else {
    // 유효하지 않은 연도 입력 시 처리 (선택사항: 그냥 무시하거나 전체로 돌리거나)
    // "화면 유지" 요구사항에 따라 유효하지 않으면 아무것도 안 하거나, 
    // 입력값을 유지하되 필터는 적용 안 할 수 있음. 
    // 여기서는 유효한 연도가 아니면 필터 적용 안함.
  }
  showDropdown.value = false
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
  emitFilter()
}

onMounted(() => {
  fetchGenres()
  generateYears()
})
</script>

<style scoped>
.filter-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.year-selector {
  position: relative;
}

select, input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.year-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0;
  margin: 0;
  list-style: none;
  z-index: 1000;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.year-option {
  padding: 8px 10px;
  cursor: pointer;
  color: #333;
}

.year-option:hover {
  background-color: #f0f0f0;
  color: #000;
}

.no-result {
  padding: 8px 10px;
  color: #888;
  cursor: default;
}

.reset-btn {
  padding: 5px 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.reset-btn:hover {
  background-color: #e0e0e0;
}
</style>