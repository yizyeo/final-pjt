<template>
  <header class="profile-header">
    <div class="rank-badge">
      <img :src="userTier.icon" :alt="userTier.label" class="tier-icon">
      <p class="tier-label">{{ userTier.label }}</p>
    </div>
    
    <div v-if="!isEditing" class="user-info">
      <h1>{{ profile.username }}님의 프로필</h1>
      <p class="ai-bio">{{ profile.bio || "AI 생성 한 줄 소개" }}</p>
      <button v-if="isOwnProfile" @click="startEdit" class="btn-edit-trigger">
        내 정보 수정하기
      </button>
    </div>

    <div v-else class="user-info-edit">
      <h1>정보 수정</h1>
      <div class="edit-form">
        <label>Email: </label>
        <input v-model.trim="editData.email" type="email">
        <label>Age: </label>
        <input v-model.number="editData.age" type="number">
        <p>성별</p>
        <label><input type="radio" value="M" v-model="editData.gender">남성</label>
        <label><input type="radio" value="F" v-model="editData.gender">여성</label>
        <p>선호 장르</p>
        <div class="genre-grid">
          <label v-for="genre in genres" :key="genre.genre_id">
            <input type="checkbox" :value="genre.genre_id" v-model="editData.favorite_genres">
            {{ genre.name_kr }}
          </label>
        </div>
        <div class="edit-actions">
          <button @click="onUpdate" class="btn-save">저장</button>
          <button @click="isEditing = false" class="btn-cancel">취소</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps(['profile', 'genres', 'isOwnProfile'])
const emit = defineEmits(['update-profile'])

const isEditing = ref(false)
const editData = ref({ email: '', age: null, gender: '', favorite_genres: [] })

const userTier = computed(() => {
  const count = props.profile?.review_count || 0
  if (count >= 10) return { label: '시네마 마스터', icon: '/icons/rank_5.png' }
  if (count >= 5) return { label: '영화 전문가', icon: '/icons/rank_4.png' }
  if (count >= 3) return { label: '영화 애호가', icon: '/icons/rank_3.png' }
  if (count >= 1) return { label: '뉴비 평론가', icon: '/icons/rank_2.png' }
  return { label: '관객', icon: '/icons/rank_1.png' }
})

const startEdit = () => {
  const currentGenres = props.profile.favorite_genres || []
  editData.value = {
    email: props.profile.email,
    age: props.profile.age,
    gender: props.profile.gender,
    favorite_genres: currentGenres.map(g => typeof g === 'object' ? (g.genre_id || g.id) : g)
  }
  isEditing.value = true
}

const onUpdate = () => {
  emit('update-profile', editData.value, () => { isEditing.value = false })
}
</script>