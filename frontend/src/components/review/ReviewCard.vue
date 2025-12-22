<template>
  <div class="card bg-dark text-white h-100 border-secondary review-card shadow-sm">
    <div class="row g-0 h-100">
      <div class="col-4 movie-poster-wrapper" @click="$emit('go-movie', review.movie)">
        <img :src="getImageUrl(review.movie_poster)" class="img-fluid rounded-start h-100" alt="poster">
      </div>
      
      <div class="col-8 d-flex flex-column">
        <div class="card-body d-flex flex-column h-100">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <h5 class="card-title text-truncate mb-0 clickable" @click="$emit('go-movie', review.movie)">
              {{ review.movie_title }}
            </h5>
            <div class="star-rating flex-shrink-0 ms-2">
              <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= review.rating / 2 }">★</span>
            </div>
          </div>

          <p class="card-text flex-grow-1 review-content clickable" @click="$emit('go-detail', review.id)">
            {{ review.content }}
          </p>

          <div class="d-flex justify-content-between align-items-center mt-auto pt-3">
            <span class="text-secondary small">by {{ review.username }}</span>
            <div class="d-flex align-items-center gap-2">
              <button @click="$emit('like', review.id)" class="btn-like">
                <span :class="{ 'liked': review.is_liked }">{{ review.is_liked ? '❤️' : '🤍' }}</span>
                <span class="ms-1">{{ review.like_count }}</span>
              </button>
              <button @click="$emit('go-detail', review.id)" class="btn btn-sm btn-outline-secondary py-0 px-2">댓글</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['review'])
defineEmits(['go-movie', 'go-detail', 'like'])

const getImageUrl = (path) => path ? `https://image.tmdb.org/t/p/w200${path}` : '/no-image.png'
</script>

<style scoped>
.review-card { transition: transform 0.2s; }
.review-card:hover { transform: translateY(-5px); border-color: #ffc107 !important; }
.movie-poster-wrapper { cursor: pointer; overflow: hidden; }
.movie-poster-wrapper img { object-fit: cover; width: 100%; height: 100%; }
.star-rating { color: #444; font-size: 0.8rem; }
.star.filled { color: #ffc107; }
.clickable { cursor: pointer; }
.review-content {
  font-size: 0.9rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.btn-like { background: none; border: none; color: white; display: flex; align-items: center; padding: 0; }
.liked { transform: scale(1.1); display: inline-block; }
</style>