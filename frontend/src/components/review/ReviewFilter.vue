<template>
  <div>
    <button 
      v-for="mode in ['popular', 'latest']" 
      :key="mode"
      @click="$emit('change-sort', mode)" 
      :class="{ active: currentSort === mode }"
    >
      {{ mode === 'latest' ? '최신순' : '인기순' }}
    </button>
  </div>
</template>

<script setup>
defineProps(['currentSort'])
defineEmits(['change-sort'])
</script>