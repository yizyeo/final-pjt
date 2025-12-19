import { defineStore } from 'pinia'
import axios from 'axios'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    profile: null,
    genres: [],
  }),
  
  getters: {
    // 추후, 추천 시스템에 필요한 데이터
    recommendationData: (state) => {
      if (!state.profile) return null
      return {
        favoriteGenres: state.profile.favorite_genres,
        likedMovies: state.profile.like_movies,
        reviews: state.profile.reviews,
        watchedMovies: state.profile.watched_movies,
        wishlist: state.profile.wishlist,
      }
    }
  },

  actions: {
    // 1. 프로필 정보 및 장르 목록 가져오기
    async fetchProfile(username, token, API_URL) {
      try {
        const [profRes, genreRes] = await Promise.all([
          axios.get(`${API_URL}/accounts/profile/${username}/`, {
            headers: { Authorization: `Token ${token}` }
          }),
          axios.get(`${API_URL}/movies/genres/`)
        ])
        this.profile = profRes.data
        this.genres = genreRes.data
      } catch (err) {
        console.error('데이터 로딩 실패:', err)
      }
    },

    // 2. 정보 수정 (AI Bio 포함)
    async updateProfile(editData, token, API_URL) {
      try {
        const res = await axios({
          method: 'put',
          url: `${API_URL}/accounts/update/`,
          data: editData,
          headers: { Authorization: `Token ${token}` }
        })
        // 서버 응답으로 스토어의 profile 정보 갱신
        this.profile = { ...this.profile, ...res.data }
        return true
      } catch (err) {
        console.error('수정 실패:', err)
        throw err
      }
    },

    // 3. AI Bio만 즉시 업데이트 (부모-자식 간의 실시간 동기화용)
    setBio(newBio) {
      if (this.profile) {
        this.profile.bio = newBio
      }
    }
  }
})