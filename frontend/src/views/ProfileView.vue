<template>
  <div v-if="profileStore.profile" class="profile-container">
    <ProfileHeader 
      :profile="profileStore.profile" 
      :genres="profileStore.genres" 
      :isOwnProfile="accountStore.username === route.params.username"
      @update-profile="updateInfo"
      @update-bio="profileStore.setBio" 
    />
    <hr>
    <ProfileReviewList 
      :reviews="profileStore.profile.reviews" 
      :reviewCount="profileStore.profile.review_count" 
    />
    <ProfileMovieList :profile="profileStore.profile" />
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
const profileStore = useProfileStore() // 스토어 사용
const API_URL = import.meta.env.VITE_API_URL

const loadData = () => {
  profileStore.fetchProfile(route.params.username, accountStore.token, API_URL)
}

onMounted(loadData)

// 다른 사람 프로필로 이동했을 때를 위해 watch 추가
watch(() => route.params.username, loadData)

const updateInfo = async (editData, callback) => {
  try {
    await profileStore.updateProfile(editData, accountStore.token, API_URL)
    callback()
    alert('정보가 수정되었습니다.')
  } catch (err) {
    alert('수정에 실패했습니다.')
  }
}
</script>