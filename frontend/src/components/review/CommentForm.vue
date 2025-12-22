<template>
  <div class="comment-form mb-4">
    <div class="input-group">
      <input 
        v-model.trim="content" 
        type="text" 
        class="form-control bg-secondary text-white border-0" 
        placeholder="댓글을 남겨보세요..."
        @keyup.enter="handleSubmit"
      >
      <button @click="handleSubmit" class="btn btn-primary">등록</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['submit-comment'])
const content = ref('')

const handleSubmit = () => {
  if (!content.value) return
  emit('submit-comment', content.value)
  content.value = ''
}
</script>