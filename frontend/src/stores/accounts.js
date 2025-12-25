import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const token = ref(null)
  const username = ref(null)
  const router = useRouter()

  const signUp = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: payload
    })
      .then(res => {
        console.log('회원 가입이 완료되었습니다.')
        const loginPayload = {
          username: payload.username,
          password: payload.password1
        }
        logIn(loginPayload)
      })
      .catch(err => {
        if (err.response && err.response.status === 400) {
          const errorData = err.response.data
          // 백엔드에서 보낸 한국어 메시지를 그대로 합쳐서 보여줌
          const messages = Object.values(errorData).flat().join('\n')
          alert(messages)
        }
      })
  }

  const logIn = function (payload) {
    const loginUsername = payload.username
    const loginPassword = payload.password

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username: loginUsername,
        password: loginPassword
      }
    })
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        username.value = loginUsername
        token.value = res.data.key
        
        router.push({ name: 'HomeView' })
      })
      .catch(err => {
        if (err.response && err.response.status === 400) {
          const errorData = err.response.data
          if (errorData.username) {
            alert(`아이디 오류: ${errorData.username[0]}`) 
          } else if (errorData.password) {
            alert(`비밀번호 오류: ${errorData.password[0]}`)
          } else {
            alert('입력 정보를 확인해주세요.')
          }
        } else {
          console.error(err)
        }
      })
  }

  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        token.value = null
        username.value = null
        router.push({ name: 'HomeView' })
      })
      .catch(err => {
        console.log(err)
        token.value = null
        username.value = null
      })
  }
  
  return {
    signUp,
    logIn,
    token,
    username,
    isLogin,
    logOut,
  }
}, { persist: true })