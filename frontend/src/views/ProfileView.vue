<template>
  <div v-if="profile" class="profile-container">
    <ProfileHeader 
      :profile="profile" 
      :genres="genres" 
      :isOwnProfile="accountStore.username === route.params.username"
      @update-profile="updateInfo"
      @update-bio="updateBio"
    />
    <hr>
    <ProfileReviewList 
      :reviews="profile.reviews" 
      :reviewCount="profile.review_count" 
    />
    <ProfileMovieList :profile="profile" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

import ProfileHeader from '@/components/profile/ProfileHeader.vue'
import ProfileReviewList from '@/components/profile/ProfileReviewList.vue'
import ProfileMovieList from '@/components/profile/ProfileMovieList.vue'

const route = useRoute()
const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL

const profile = ref(null)
const genres = ref([])

const updateBio = (newBio) => {
  if (profile.value) {
    profile.value.bio = newBio
  }
}

const fetchData = async () => {
  try {
    const [profRes, genreRes] = await Promise.all([
      axios.get(`${API_URL}/accounts/profile/${route.params.username}/`, {
        headers: { Authorization: `Token ${accountStore.token}` }
      }),
      axios.get(`${API_URL}/movies/genres/`)
    ])
    profile.value = profRes.data
    genres.value = genreRes.data
  } catch (err) {
    console.error('데이터 로딩 실패:', err)
  }
}

onMounted(fetchData)

const updateInfo = async (editData, callback) => {
  try {
    const res = await axios({
      method: 'put',
      url: `${API_URL}/accounts/update/`,
      data: editData,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    profile.value = { ...profile.value, ...res.data }
    callback()
    alert('정보가 성공적으로 수정되었습니다.')
  } catch (err) {
    console.error('수정 실패:', err)
    alert('수정에 실패했습니다.')
  }
}
</script>