import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProfileView from '@/views/ProfileView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieListView from '@/views/MovieListView.vue'
import SearchView from '@/views/SearchView.vue'
import WorldcupView from '@/views/WorldcupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },

    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView
    },
    {
      path: '/movies/:movieId',
      name: 'MovieDetailView',
      component: MovieDetailView
    },
    {
      path: '/movies/movielist',
      name: 'MovieListView',
      component: MovieListView
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
    }
  ]
})

router.beforeEach((to, from) => {
  const accountStore = useAccountStore()

  // 게시물 접근 제한
  // if (to.name === 'ArticleView' && !accountStore.isLogin) {
  //   window.alert('로그인이 필요합니다.')
  //   return { name: 'LogInView' }
  // }

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (accountStore.isLogin) ) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'HomeView' }
  }
})

export default router