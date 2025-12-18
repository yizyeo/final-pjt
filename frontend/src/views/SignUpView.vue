<template>
    <div>
        <h1>회원가입</h1>
        <form @submit.prevent="signUp">
            <label for="username">username: </label>
            <input type="text" id="username" v-model.trim="username">
            <br>
            <label for="password1">pw: </label>
            <input type="password" id="password1" v-model.trim="password1">
            <p v-if="password1.length > 0 && password1.length < 8" style="color: red; font-size: 0.8rem;">
              비밀번호는 8자 이상이어야 합니다.
            </p>
            <br>
            <label for="password2">pw confirmation: </label>
            <input type="password" id="password2" v-model.trim="password2">
            <br>
            <label for="email">email: </label>
            <input type="email" id="email" v-model.trim="email">
            <br>
            <label for="age">age: </label>
            <input type="number" id="age" v-model.trim="age">
            <br>
            <p>성별</p>
            <label>
              <input type="radio" name="gender" value="M" v-model="gender">남성
            </label>
            <label>
              <input type="radio" name="gender" value="F" v-model="gender">여성
            </label>
            <br>
            <p>선호 장르</p>
            <label v-for="genre in genres" :key="genre.genre_id">
              <input
                type="checkbox"
                :value="genre.genre_id"
                v-model="favorite_genres"
              >
                {{ genre.name_kr }}
            </label>
            <br><br>
            <input type="submit" value="signup">

        </form>

    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const API_URL = import.meta.env.VITE_API_URL

const store = useAccountStore()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const email = ref('')
const gender = ref('')
const age = ref(null)
const favorite_genres = ref([])

const genres = ref([]) // 장르 선택지를 보여주는 용도

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/movies/genres/`)
    console.log(res.data) 
    genres.value = res.data
  } catch (err) {
    console.error('영화 장르 리스트 로딩 실패', err)
  }
})

const signUp = () => {
  if (!username.value || !email.value || !age.value || !gender.value) {
    alert('모든 필수 정보를 입력해주세요.')
    return
  }

  if (password1.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  if (favorite_genres.value.length === 0) {
    alert('선호 장르를 최소 1개 선택해주세요.')
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    alert('유효한 이메일 형식이 아닙니다.')
    return
  }

  const password = password1.value
  if (password.length < 8) {
    alert('비밀번호는 최소 8자 이상이어야 합니다.')
    return
  }

  store.signUp({
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    age: age.value,
    gender: gender.value,
    favorite_genres: favorite_genres.value,
  })
}

</script>

<style scoped>

</style>