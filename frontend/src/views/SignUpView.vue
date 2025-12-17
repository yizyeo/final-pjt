<template>
    <div>
        <h1>회원가입</h1>
        <form @submit.prevent="signUp">
            <label for="username">id: </label>
            <input type="text" id="username" v-model.trim="username">
            <br>
            <label for="password1">pw: </label>
            <input type="password" id="password1" v-model.trim="password1">
            <br>
            <label for="password2">pw confirmation: </label>
            <input type="password" id="password2" v-model.trim="password2">
            <br>
            <label for="age">age: </label>
            <input type="number" id="age" v-model.trim="age">
            <br>
            <p>선호 장르</p>
            <label v-for="genre in genres" :key="genre.id">
              <input
                type="checkbox"
                :value="genre.id"
                v-model="favorite_genres"
              >
              {{ genre.name }}
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

const API_URL = 'http://127.0.0.1:8000'

const store = useAccountStore()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const age = ref(null)
const favorite_genres = ref([])

const genres = ref([])

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/movies/genres/`)
    genres.value = res.data
  } catch (err) {
    console.error('장르 로딩 실패', err)
  }
})

const signUp = () => {
  if (password1.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다!')
    return
  }
  store.signUp({
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    age: age.value,
    favorite_genres: favorite_genres.value,
  })
}

</script>

<style scoped>

</style>