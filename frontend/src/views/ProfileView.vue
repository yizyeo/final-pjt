<template>
  <div class="profile-page">
    
    <div v-if="!profileStore.profile" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else class="profile-container">
      
      <section class="header-section">
        <ProfileHeader 
          :profile="profileStore.profile" 
          :genres="profileStore.genres" 
          :isOwnProfile="accountStore.username === route.params.username"
          @update-profile="updateInfo"
          @update-bio="profileStore.setBio" 
        />
      </section>

      <div class="section-divider"></div>

      <section class="content-section">
        <ProfileReviewList 
          :reviews="profileStore.profile.reviews" 
          :reviewCount="profileStore.profile.review_count" 
        />
      </section>

      <div class="section-divider"></div>

      <section class="content-section">
        <ProfileMovieList :profile="profileStore.profile" />
      </section>

    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useProfileStore } from '@/stores/profile'

import ProfileHeader from '@/components/profile/ProfileHeader.vue'
import ProfileReviewList from '@/components/profile/ProfileReviewList.vue'
import ProfileMovieList from '@/components/profile/ProfileMovieList.vue'

const route = useRoute()
const accountStore = useAccountStore()
const profileStore = useProfileStore()
const API_URL = import.meta.env.VITE_API_URL

const loadData = () => {
  profileStore.fetchProfile(route.params.username, accountStore.token, API_URL)
}

onMounted(loadData)

watch(() => route.params.username, loadData)

const updateInfo = async (editData, callback) => {
  try {
    await profileStore.updateProfile(editData, accountStore.token, API_URL)
    callback()
    // alert('정보가 수정되었습니다.') -> UX상 성공 메시지는 토스트나 모달이 좋지만, 일단 제거하거나 유지
  } catch (err) {
    alert('수정에 실패했습니다.')
  }
}
</script>

<style scoped>
/* 전체 페이지 배경 */
.profile-page {
  min-height: 100vh;
  background-color: #F8F9FA; /* 밝은 회색 배경 */
  padding: 3rem 1rem 6rem; /* 상단, 좌우, 하단 여백 */
}

/* 중앙 정렬 컨테이너 */
.profile-container {
  max-width: 1000px; /* 너무 넓지 않게 제한 */
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem; /* 섹션 간 간격 */
}

/* 섹션 스타일 (개별 컴포넌트가 카드 스타일을 가질 예정이므로 여기선 레이아웃만 관여) */
.header-section, 
.content-section {
  width: 100%;
  animation: fadeIn 0.5s ease-out;
}

/* 섹션 구분선 (hr 대신 사용) */
.section-divider {
  height: 1px;
  background-color: #E0E0E0;
  width: 100%;
  margin: 0.5rem 0;
  display: none; /* 카드형 디자인에서는 구분선 없이 간격(gap)으로 띄우는 게 더 깔끔해서 숨김 처리함. 원하면 block으로 변경 */
}

/* 로딩 스피너 */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #E0E0E0;
  border-top: 5px solid #7A6CFA;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .profile-page {
    padding: 1rem 1rem 4rem;
  }
  
  .profile-container {
    gap: 1.5rem;
  }
}
</style>