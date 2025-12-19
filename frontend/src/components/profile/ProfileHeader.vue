<template>
  <header class="profile-header">
    <div class="rank-badge">
      <img :src="userTier.icon" :alt="userTier.label" class="tier-icon">
      <p class="tier-label">{{ userTier.label }}</p>
    </div>
    
    <div v-if="!isEditing" class="user-info">
      <h1>{{ profile.username }}님의 프로필</h1>
      <p class="ai-bio">✨ {{ profile.bio || "AI 생성 한 줄 소개가 없습니다." }} ✨</p>
      <button v-if="isOwnProfile" @click="startEdit" class="btn-edit-trigger">
        내 정보 수정하기
      </button>
    </div>

    <div v-else class="user-info-edit">
      <div class="edit-header">
        <h1>정보 수정</h1>
        <button 
          @click="onGenerateAI" 
          :disabled="isGenerating"
          class="btn-ai-gen"
        >
          {{ isGenerating ? 'AI 분석 중...' : '✨ AI 한 줄 소개 생성' }}
        </button>
      </div>

      <div class="edit-form">
        <label>한 줄 소개: </label>
        <input v-model.trim="editData.bio" type="text" placeholder="AI로 생성하거나 직접 입력">

        <label>이메일: </label>
        <input v-model.trim="editData.email" type="email">

        <label>나이: </label>
        <input v-model.number="editData.age" type="number">
        
        <p>성별</p>
        <div class="radio-group">
          <label><input type="radio" value="M" v-model="editData.gender">남성</label>
          <label><input type="radio" value="F" v-model="editData.gender">여성</label>
        </div>

        <p>선호 장르</p>
        <div class="genre-grid">
          <label v-for="genre in genres" :key="genre.genre_id" class="genre-item">
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
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const props = defineProps(['profile', 'genres', 'isOwnProfile'])
const emit = defineEmits(['update-profile', 'update-bio'])

const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL

const isEditing = ref(false)
const isGenerating = ref(false)
const editData = ref({ bio: '', email: '', age: null, gender: '', favorite_genres: [] })

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
    bio: props.profile.bio || '',
    email: props.profile.email,
    age: props.profile.age,
    gender: props.profile.gender,
    favorite_genres: currentGenres.map(g => typeof g === 'object' ? (g.genre_id || g.id) : g)
  }
  isEditing.value = true
}

const onGenerateAI = async () => {
  if (!confirm('AI 취향 분석을 시작하시겠습니까?')) return
  
  isGenerating.value = true
  try {
    const res = await axios({
      method: 'post',
      url: `${API_URL}/accounts/generate-bio/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    
    const newBio = res.data.bio
    editData.value.bio = newBio // 입력창 반영
    emit('update-bio', newBio)  // 부모(ProfileView)의 원본 데이터도 갱신해야 함
    alert('AI 한 줄 소개가 생성되었습니다!')
  } catch (err) {
    console.error('AI 생성 에러:', err)
    alert('생성에 실패했습니다. 서버 로그를 확인해주세요.')
  } finally {
    isGenerating.value = false
  }
}

const onUpdate = () => {
  emit('update-profile', editData.value, () => { isEditing.value = false })
}
</script>

<style scoped>

</style>