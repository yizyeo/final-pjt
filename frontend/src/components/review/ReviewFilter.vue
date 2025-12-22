<template>
  <div class="btn-group">
    <button 
      v-for="mode in ['latest', 'popular']" 
      :key="mode"
      @click="$emit('change-sort', mode)" 
      class="btn btn-outline-light text-capitalize" 
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