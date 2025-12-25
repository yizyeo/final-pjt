<template>
  <div class="profile-header-card">
    
    <div v-if="!isEditing" class="view-mode-layout">
      
      <div class="left-column">
        <div class="tier-icon-wrapper">
          <img :src="userTier.icon" :alt="userTier.label" class="tier-icon">
        </div>
        <span class="tier-label">{{ userTier.label }}</span>
      </div>

      <div class="right-column">
        
        <div class="user-title-row">
          <h1 class="username">{{ profile.username }}</h1>
          <button v-if="isOwnProfile" @click="startEdit" class="btn-edit-sm">
            정보 수정
          </button>
        </div>

        <div class="bio-box">
          <p class="bio-text">
            <span class="quote">“</span>
            {{ profile.bio || "아직 AI가 분석한 소개가 없습니다. 버튼을 눌러 생성해보세요!" }}
            <span class="quote">”</span>
          </p>
          
        </div>

        <div v-if="isOwnProfile" class="action-row">
          <button 
            @click="onGenerateAI" 
            :disabled="isGenerating"
            class="btn-ai-gen"
            :class="{ 'loading': isGenerating }"
          >
            <span v-if="isGenerating" class="spinner-sm"></span>
            <span v-else>✨ AI 분석 & 소개 갱신</span>
          </button>
        </div>

      </div>
    </div>

    <div v-else class="edit-mode">
      <h2 class="edit-title">프로필 정보 수정</h2>
      
      <div class="edit-form">
        <div class="form-group">
          <label>이메일</label>
          <input v-model.trim="editData.email" type="email" class="form-input">
        </div>

        <div class="form-group">
          <label>나이</label>
          <input v-model.number="editData.age" type="number" class="form-input">
        </div>
        
        <div class="form-group">
          <label>성별</label>
          <div class="gender-selector">
            <label class="gender-btn" :class="{ active: editData.gender === 'M' }">
              <input type="radio" value="M" v-model="editData.gender" class="hidden-input">
              남성
            </label>
            <label class="gender-btn" :class="{ active: editData.gender === 'F' }">
              <input type="radio" value="F" v-model="editData.gender" class="hidden-input">
              여성
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>선호 장르</label>
          <div class="genre-grid">
            <label 
              v-for="genre in genres" 
              :key="genre.genre_id" 
              class="genre-chip"
              :class="{ active: editData.favorite_genres.includes(genre.genre_id) }"
            >
              <input 
                type="checkbox" 
                :value="genre.genre_id" 
                v-model="editData.favorite_genres"
                class="hidden-input"
              >
              {{ genre.name_kr }}
            </label>
          </div>
        </div>

        <div class="edit-actions">
          <button @click="isEditing = false" class="btn-cancel">취소</button>
          <button @click="onUpdate" class="btn-save">저장하기</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
// [수정 1] 공통 유틸리티 함수 import
import { getTier } from '@/utils/tierUtils'

const props = defineProps(['profile', 'genres', 'isOwnProfile'])
const emit = defineEmits(['update-profile', 'update-bio'])

const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL

const isEditing = ref(false)
const isGenerating = ref(false)
const editData = ref({ email: '', age: null, gender: '', favorite_genres: [] })

// [수정 2] getTier 함수를 사용하여 티어 계산 로직 간소화
const userTier = computed(() => {
  const count = props.profile?.review_count || 0
  return getTier(count)
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

const onGenerateAI = async () => {
  if (!confirm('내 취향을 분석해 새로운 소개글을 생성하시겠습니까?')) return
  isGenerating.value = true
  try {
    const res = await axios({
      method: 'post',
      url: `${API_URL}/accounts/generate-bio/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    const newBio = res.data.bio
    emit('update-bio', newBio) 
  } catch (err) {
    console.error('AI 생성 에러:', err)
    alert('생성에 실패했습니다.')
  } finally {
    isGenerating.value = false
  }
}

const onUpdate = () => {
  emit('update-profile', editData.value, () => { isEditing.value = false })
}
</script>

<style scoped>
/* 기존 스타일 그대로 유지 */
.profile-header-card {
  background-color: #FFFFFF;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.view-mode-layout {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.left-column {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 140px;
}

.tier-icon-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: #F8F9FA;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
  border: 4px solid #F0EBFF;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.tier-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.tier-label {
  background-color: #EFEFEF;
  color: #555;
  font-size: 0.9rem;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 20px;
}

.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.user-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1rem;
  width: 100%;
}

.username {
  font-size: 2rem;
  font-weight: 800;
  color: #111111;
  margin: 0;
}

.btn-edit-sm {
  background: none;
  border: 1px solid #DDDDDD;
  color: #888;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
}

.btn-edit-sm:hover {
  background-color: #F5F5F5;
  color: #333;
}

.bio-box {
  background-color: #F9FAFB;
  border-left: 4px solid #7A6CFA;
  padding: 1.2rem 1.5rem;
  border-radius: 0 12px 12px 0;
  width: 100%;
  margin-bottom: 1.5rem;
}

.bio-text {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #444;
  font-weight: 500;
  white-space: pre-wrap;
}

.quote {
  color: #7A6CFA;
  font-size: 1.2rem;
  font-weight: 800;
  margin: 0 4px;
}

.action-row {
  display: flex;
  justify-content: flex-start;
}

.btn-ai-gen {
  background: linear-gradient(135deg, #7A6CFA, #9D8CFC);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 50px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(122, 108, 250, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-ai-gen:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(122, 108, 250, 0.4);
}

.btn-ai-gen:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Edit Mode */
.edit-mode {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.edit-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 2rem;
}

.form-group { margin-bottom: 1.5rem; }
label { display: block; font-weight: 700; margin-bottom: 0.5rem; color: #333; font-size: 0.95rem; }
.form-input { width: 100%; padding: 12px; border: 1px solid #DDD; border-radius: 10px; font-size: 1rem; font-family: inherit; }
.form-input:focus { outline: none; border-color: #7A6CFA; }

.hidden-input { display: none; }
.gender-selector { display: flex; gap: 10px; }
.gender-btn { flex: 1; padding: 10px; border: 1px solid #EEE; background-color: #FAFAFA; border-radius: 10px; text-align: center; cursor: pointer; color: #666; font-weight: 600; }
.gender-btn.active { background-color: #F0EBFF; border-color: #7A6CFA; color: #7A6CFA; }

.genre-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.genre-chip { padding: 8px 14px; background-color: #F5F5F5; border-radius: 20px; font-size: 0.9rem; color: #555; cursor: pointer; border: 1px solid transparent; }
.genre-chip.active { background-color: #7A6CFA; color: white; box-shadow: 0 4px 10px rgba(122, 108, 250, 0.2); }

.edit-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 2rem; }
.btn-save { background-color: #7A6CFA; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; }
.btn-cancel { background-color: white; border: 1px solid #DDD; padding: 10px 20px; border-radius: 8px; cursor: pointer; }

.spinner-sm { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .view-mode-layout {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
  
  .right-column {
    align-items: center;
    width: 100%;
  }

  .user-title-row {
    justify-content: center;
  }

  .bio-box {
    text-align: left;
    border-left: none;
    border-top: 4px solid #7A6CFA;
    border-radius: 12px;
  }
  
  .action-row {
    justify-content: center;
  }
}
</style>