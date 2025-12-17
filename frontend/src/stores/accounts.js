import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)

  const router = useRouter()

  const signUp = function (payload) {
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2
    const age = payload.age
    const favorite_genres = payload.favorite_genres
    // const { username, password1, password2, age } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, age, favorite_genres
      }
    })
      .then(res => {
        console.log('회원 가입이 완료되었습니다.')
        const password = password1
        logIn({ username, password })
      })
      .catch(err => {
        // 400 에러 시 서버가 보내준 상세 메시지 출력
        if (err.response && err.response.status === 400) {
          console.table(err.response.data)
          alert('회원가입 실패: ' + JSON.stringify(err.response.data))
        }
      })
  }


  const logIn = function (payload) {
    const username = payload.username
    const password = payload.password
    // const { username, password } = payload
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        console.log(res.data)
        token.value = res.data.key
        router.push({ name: 'HomeView' })
      })
      .catch(err => console.log(err))
  }


  const isLogin = computed(() => {
    return token.value ? true : false
  })


  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}` // 토큰을 함께 보내야 안전하게 로그아웃됨
      }
    })
      .then(res => {
        token.value = null
        router.push({ name: 'LogInView' })
      })
      .catch(err => console.log(err))
  }

  return {
    signUp,
    logIn,
    token,
    isLogin,
    logOut,
  }
}, { persist: true })