import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './accounts'

export const useReviewStore = defineStore('review', {
  state: () => ({
    totalReviews: [],      // 전체 리뷰 목록
    movieReviews: [],      // 특정 영화의 리뷰 목록
    currentReview: null,   // 상세 조회를 위한 단일 리뷰
    loading: false
  }),

  actions: {
    // 전체 리뷰
    async fetchTotalReviews(orderBy = 'latest') {
      this.loading = true
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/reviews/`, {
          params: { sort: orderBy }
        })
        this.totalReviews = res.data
      } catch (err) {
        console.error('전체 리뷰 로드 실패:', err)
      } finally {
        this.loading = false
      }
    },

    // 특정 영화의 리뷰 목록
    async fetchMovieReviews(moviePk) {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/reviews/movies/${moviePk}/`)
        this.movieReviews = res.data
      } catch (err) {
        console.error('영화 리뷰 로드 실패:', err)
      }
    },

    // 리뷰 작성
    async createReview(moviePk, payload) {
      const accountStore = useAccountStore()
      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/reviews/movies/${moviePk}/`,
          data: payload,
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        this.movieReviews.unshift(res.data) // 목록 맨 앞에 추가
        return res.data
      } catch (err) {
        console.error('리뷰 작성 실패:', err)
        throw err
      }
    },

    // 리뷰 좋아요
    async likeReview(reviewPk) {
      const accountStore = useAccountStore()
      if (!accountStore.token) return alert('로그인이 필요합니다.')

      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/reviews/${reviewPk}/like/`,
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        
        // 스토어 내의 리뷰 데이터 실시간 업데이트 (좋아요 수/상태)
        const updateLike = (review) => {
          if (review.id === reviewPk) {
            review.like_count = res.data.like_count
            review.is_liked = res.data.is_liked
          }
        }
        this.totalReviews.forEach(updateLike)
        this.movieReviews.forEach(updateLike)
      } catch (err) {
        console.error('좋아요 실패:', err)
      }
    }
  }
})