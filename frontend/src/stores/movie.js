import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useMovieStore = defineStore('movie', {
  state: () => ({
    movieDetail: null, // 영화 상세 정보
    trailerKey: null, // 예고편 키 (YouTube ID)
    loading: false // 로딩 상태
  }),

  actions: {
    // 1. 영화 상세 정보 가져오기 (GET)
    async fetchMovieDetail(movieId) {
      const accountStore = useAccountStore()
      this.loading = true
      
      try {
        const headers = accountStore.token 
          ? { Authorization: `Token ${accountStore.token}` } 
          : {}

        const res = await axios.get(`${import.meta.env.VITE_API_URL}/movies/movie/${movieId}/detail/`, { headers })
        this.movieDetail = res.data
      } catch (err) {
        console.error('영화 상세 정보 로드 실패:', err)
      } finally {
        this.loading = false
      }
    },

    // 2. 예고편 ID 가져오기 (GET)
    async fetchTrailer(movieId) {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/movies/movie/${movieId}/trailer/`)
        if (res.data.videoId) {
          this.trailerKey = res.data.videoId
        } else {
          this.trailerKey = null
          alert('예고편을 찾을 수 없습니다.')
        }
      } catch (err) {
        console.error('예고편 로드 실패:', err)
        this.trailerKey = null
      }
    },

    // 3. 좋아요 토글 (POST)
    async toggleLike(movieId) {
      const accountStore = useAccountStore()
      if (!accountStore.isLogin) return alert('로그인이 필요합니다.')

      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/movies/movie/${movieId}/like/`,
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        
        if (this.movieDetail && this.movieDetail.tmdb_id === Number(movieId)) {
          this.movieDetail.is_liked = res.data.is_liked
        }
      } catch (err) {
        console.error(err)
      }
    },

    // 4. 볼거에요 토글 (POST)
    async toggleWish(movieId) {
      const accountStore = useAccountStore()
      if (!accountStore.isLogin) return alert('로그인이 필요합니다.')

      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/movies/movie/${movieId}/wish/`,
          headers: { Authorization: `Token ${accountStore.token}` }
        })

        if (this.movieDetail && this.movieDetail.tmdb_id === Number(movieId)) {
          this.movieDetail.is_wished = res.data.is_wished
        }
      } catch (err) {
        console.error(err)
      }
    },

    // 5. 봤어요 토글 (POST)
    async toggleWatched(movieId) {
      const accountStore = useAccountStore()
      if (!accountStore.isLogin) return alert('로그인이 필요합니다.')

      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/movies/movie/${movieId}/watched/`,
          headers: { Authorization: `Token ${accountStore.token}` }
        })

        if (this.movieDetail && this.movieDetail.tmdb_id === Number(movieId)) {
          this.movieDetail.is_watched = res.data.is_watched
        }
      } catch (err) {
        console.error(err)
      }
    }
  }
})