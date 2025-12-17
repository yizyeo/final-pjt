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

  </div>
  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts'

  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }

</script>

<style scoped>

</style>