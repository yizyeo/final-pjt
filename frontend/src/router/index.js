import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProfileView from '@/views/ProfileView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieListView from '@/views/MovieListView.vue'
import ReviewListView from '@/views/ReviewListView.vue'
import ReviewDetailView from '@/views/ReviewDetailView.vue'
import SearchView from '@/views/SearchView.vue'
import WorldcupView from '@/views/WorldcupView.vue'
import RecommendKeywordView from '@/views/RecommendKeywordView.vue'
import BlindReviewView from '@/views/BlindReviewView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 메인 페이지 (기본 페이지)
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },
    // 회원가입 페이지
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    // 로그인 페이지
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    // 사용자 개인 페이지 (마이페이지)
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView
    },
    // 영화 상세 페이지
    {
      path: '/movies/:movieId',
      name: 'MovieDetailView',
      component: MovieDetailView
    },
    // 전체 영화 페이지
    {
      path: '/movies/movielist',
      name: 'MovieListView',
      component: MovieListView
    },
    // 전체 리뷰 페이지
    {
      path: '/reviews',
      name: 'ReviewListView',
      component: ReviewListView
    },
    // 리뷰 상세 페이지
    {
      path: '/reviews/:reviewId',
      name: 'ReviewDetailView',
      component: ReviewDetailView
    },
    {
      path: '/search',
      name: 'SearchView',
      component: SearchView
    },
    {
      path: '/worldcup',
      name: 'WorldcupView',
      component: WorldcupView
    },
    {
      path: '/recommend-keyword',
      name: 'RecommendKeywordView',
      component: RecommendKeywordView
    },
    {
      path: '/blind-review',
      name: 'BlindReviewView',
      component: BlindReviewView
    },

  ]
})

router.beforeEach((to, from) => {
  const accountStore = useAccountStore()

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (accountStore.isLogin) ) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'HomeView' }
  }
})

export default router