<template>
  <div id="app">
    <NavBar />
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
import { RouterView } from 'vue-router';
</script>

<style>
/* 1. Pretendard 폰트 불러오기 */
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

/* 2. 전역 스타일 리셋 및 배경 설정 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  /* 배경을 완전한 흰색으로 변경 */
  background-color: #FFFFFF; 
  
  /* 폰트 적용 */
  font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
  
  /* 글자 색상 (기본) */
  color: #0F172A;
  -webkit-font-smoothing: antialiased;
}

a {
  text-decoration: none;
  color: inherit;
}

ul {
  list-style: none;
}

input, textarea, select, button {
  font-family: inherit;
}
</style>