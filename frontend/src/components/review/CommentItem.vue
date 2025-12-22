<template>
  <div class="comment-item border-bottom border-secondary py-3">
    <div class="d-flex justify-content-between align-items-center">
      <div>
        <strong class="text-white">{{ comment.username }}</strong>
        <span class="text-secondary small ms-3">{{ formatDate(comment.created_at) }}</span>
      </div>
      
      <button 
        v-if="currentUsername === comment.username" 
        @click="$emit('delete-comment', comment.id)" 
        class="btn btn-sm text-danger"
      >
        삭제
      </button>
    </div>
    <p class="text-white mt-2 mb-0">{{ comment.content }}</p>
  </div>
</template>

<script setup>
defineProps(['comment', 'currentUsername'])
defineEmits(['delete-comment'])

const formatDate = (date) => new Date(date).toLocaleString()
</script>