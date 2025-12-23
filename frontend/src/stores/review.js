import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './accounts'

export const useReviewStore = defineStore('review', {
  state: () => ({
    totalReviews: [],      // 전체 리뷰 목록
    movieReviews: [],      // 특정 영화의 리뷰 목록
    currentReview: null,   // 상세 페이지에서 보여줄 단일 리뷰 데이터
    hotReviews: [],        // 홈 화면용 인기 리뷰 저장소
    loading: false
  }),

  actions: {
    // 1. 전체 리뷰 목록 조회
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

    // 2. 특정 영화 리뷰 목록 조회
    async fetchMovieReviews(moviePk) {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/reviews/movies/${moviePk}/`)
        this.movieReviews = res.data
      } catch (err) {
        console.error('영화 리뷰 로드 실패:', err)
      }
    },

    // 3. 리뷰 상세 조회 (View 진입 시 호출)
    async getReviewDetail(reviewId) {
      this.loading = true
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/reviews/${reviewId}/`)
        this.currentReview = res.data
      } catch (err) {
        console.error('상세 리뷰 조회 실패:', err)
      } finally {
        this.loading = false
      }
    },

    // 4. 리뷰 작성
    async createReview(moviePk, payload) {
      const accountStore = useAccountStore()
      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/reviews/movies/${moviePk}/`,
          data: payload,
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        this.movieReviews.unshift(res.data)
        return res.data
      } catch (err) {
        throw err
      }
    },

    // 5. 리뷰 수정
    async updateReview(reviewId, payload) {
      const accountStore = useAccountStore()
      try {
        const res = await axios({
          method: 'put',
          url: `${import.meta.env.VITE_API_URL}/reviews/${reviewId}/`,
          data: payload,
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        
        // 상세 데이터 갱신
        this.currentReview = res.data
        
        // 목록 데이터도 동기화 (새로고침 없이 반영되도록)
        const updateList = (list) => {
          const idx = list.findIndex(r => r.id === reviewId)
          if (idx !== -1) list[idx] = res.data
        }
        updateList(this.totalReviews)
        updateList(this.movieReviews)
      } catch (err) {
        throw err
      }
    },

    // 6. 리뷰 삭제
    async deleteReview(reviewId) {
      const accountStore = useAccountStore()
      try {
        await axios({
          method: 'delete',
          url: `${import.meta.env.VITE_API_URL}/reviews/${reviewId}/`,
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        
        this.currentReview = null
        // 목록에서 제거
        this.totalReviews = this.totalReviews.filter(r => r.id !== reviewId)
        this.movieReviews = this.movieReviews.filter(r => r.id !== reviewId)
      } catch (err) {
        throw err
      }
    },

    // 7. 좋아요 토글
    async likeReview(reviewId) {
      const accountStore = useAccountStore()
      if (!accountStore.token) return alert('로그인이 필요합니다.')

      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/reviews/${reviewId}/like/`,
          headers: { Authorization: `Token ${accountStore.token}` }
        })

        // 상세 데이터 갱신
        if (this.currentReview && this.currentReview.id === reviewId) {
          this.currentReview.is_liked = res.data.is_liked
          this.currentReview.like_count = res.data.like_count
        }

        // 목록 데이터 갱신
        const updateLike = (r) => {
          if (r.id === reviewId) {
            r.is_liked = res.data.is_liked
            r.like_count = res.data.like_count
          }
        }
        this.totalReviews.forEach(updateLike)
        this.movieReviews.forEach(updateLike)
      } catch (err) {
        console.error('좋아요 실패:', err)
      }
    },

    // 8. 댓글 작성
    async createComment(reviewId, content) {
      const accountStore = useAccountStore()
      try {
        const res = await axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/reviews/${reviewId}/comments/`,
          data: { content },
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        // 현재 보고 있는 리뷰에 댓글 즉시 추가
        if (this.currentReview) {
          this.currentReview.comments.push(res.data)
        }
      } catch (err) {
        throw err
      }
    },

    // 9. 댓글 삭제
    async deleteComment(reviewId, commentId) {
      const accountStore = useAccountStore()
      try {
        await axios({
          method: 'delete',
          url: `${import.meta.env.VITE_API_URL}/reviews/${reviewId}/comments/${commentId}/`,
          headers: { Authorization: `Token ${accountStore.token}` }
        })
        // 현재 보고 있는 리뷰에서 댓글 즉시 제거
        if (this.currentReview) {
          this.currentReview.comments = this.currentReview.comments.filter(c => c.id !== commentId)
        }
      } catch (err) {
        throw err
      }
    },

    // 10. 홈 화면용 인기 리뷰 5개
    async fetchHotReviews() {
      try {
        // 백엔드에 'likes' 정렬로 요청
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/reviews/`, {
          params: { sort: 'popular' } 
        })
        this.hotReviews = res.data.slice(0, 5)
      } catch (err) {
        console.error('인기 리뷰 로드 실패:', err)
      }
    },
  }
})