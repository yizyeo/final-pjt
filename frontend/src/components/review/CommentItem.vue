<template>
  <div class="comment-item">
    <div class="comment-header">
      <div class="comment-author">
        <img :src="tier.icon" :title="tier.label" class="tier-icon-xs">
        <strong>{{ comment.username }}</strong>
        <span class="date">{{ formatDate(comment.created_at) }}</span>
      </div>
      
      <button 
        v-if="currentUsername === comment.username" 
        @click="$emit('delete-comment', comment.id)"
      >
        삭제
      </button>
    </div>
    <p>{{ comment.content }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { getTier } from '@/utils/tierUtils'

const props = defineProps(['comment', 'currentUsername'])
defineEmits(['delete-comment'])

const tier = computed(() => getTier(props.comment.user_review_count || 0))

const formatDate = (date) => new Date(date).toLocaleString()
</script>

<style scoped>
.comment-item { border-bottom: 1px solid #444; padding: 10px 0; }
.comment-header { display: flex; justify-content: space-between; margin-bottom: 5px; }
.comment-author { display: flex; align-items: center; gap: 5px; }
.tier-icon-xs { width: 20px; height: 20px; object-fit: contain; }
.date { font-size: 0.8rem; color: #888; margin-left: 5px; }
</style>