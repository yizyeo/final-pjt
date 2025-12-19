<template>
  <section class="movie-lists">
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.id" 
              :class="{ active: currentTab === tab.id }" 
              @click="currentTab = tab.id">
        {{ tab.name }}
      </button>
    </div>
    <div class="movie-grid">
      <div v-for="movie in displayMovies" :key="movie.tmdb_id" class="movie-card">
        <img :src="'https://image.tmdb.org/t/p/w200' + movie.poster_path" :alt="movie.title">
        <p>{{ movie.title }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
const props = defineProps(['profile'])

const currentTab = ref('liked')
const tabs = [
  { id: 'liked', name: '좋아요' },
  { id: 'wish', name: '볼 영화' },
  { id: 'watched', name: '본 영화' }
]

const displayMovies = computed(() => {
  if (currentTab.value === 'liked') return props.profile?.like_movies || []
  if (currentTab.value === 'wish') return props.profile?.wish_movies || []
  if (currentTab.value === 'watched') return props.profile?.watched_movies || []
  return []
})
</script>