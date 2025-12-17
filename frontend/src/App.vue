<template>
  <div>
    <nav>
      <template v-if="!accountStore.isLogin">
        <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> | 
        <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
      </template>

      <template v-else>
        <RouterLink :to="{ name: 'HomeView' }">홈</RouterLink> | 
        <a href="#" @click.prevent="logOut">로그아웃</a>
      </template>
    </nav>

  <div id="app">
    <NavBar />
    <main>
      <RouterView />
    </main>
  </div>

  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'
  import NavBar from './components/NavBar.vue'

  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }
</script>

<style>
/* Global Styles */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #141414;
  color: white;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  padding: 2rem;
}
</style>