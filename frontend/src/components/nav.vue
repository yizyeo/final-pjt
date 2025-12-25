<template>
  <router-link :to="{ name: 'HomeView' }" class="navbar-logo">
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 24 24" 
      width="32" 
      height="32" 
      fill="currentColor"
      class="ghost-icon"
    >
      <path d="M12 2C7.58172 2 4 5.58172 4 10V22H6L8 20L10 22L12 20L14 22L16 20L18 22H20V10C20 5.58172 16.4183 2 12 2ZM10 11C10 10.4477 9.55228 10 9 10C8.44772 10 8 10.4477 8 11C8 11.5523 8.44772 12 9 12C9.55228 12 10 11.5523 10 11ZM16 11C16 10.4477 15.5523 10 15 10C14.4477 10 14 10.4477 14 11C14 11.5523 14.4477 12 15 12C15.5523 12 16 11.5523 16 11Z"/>
    </svg>
    <span class="logo-text">MovieGhost</span> </router-link>
</template>

<style scoped>
.navbar-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #333; /* 기본 텍스트 색상 */
}

.ghost-icon {
  color: #7A6CFA; /* 아이콘 테마 색상 */
  transition: transform 0.2s ease;
}

.logo-text {
  font-weight: 800;
  font-size: 1.2rem;
  letter-spacing: -0.5px;
}

/* 호버 효과 */
.navbar-logo:hover .ghost-icon {
  transform: translateY(-2px); /* 살짝 떠오르는 효과 */
}
</style>