<template>
  <section class="profile-reviews-card">
    <div class="section-header">
      <h3 class="section-title">
        작성한 리뷰 <span class="count">{{ reviews.length }}</span>
      </h3>
    </div>

    <div v-if="paginatedReviews.length > 0" class="review-list">
      <div 
        v-for="review in paginatedReviews" 
        :key="review.id" 
        class="review-item"
        @click="goDetail(review.id)"
      >
        <div class="review-main">
          <div class="review-top">
            <h4 class="movie-title">{{ review.movie_title }}</h4>
            <div class="rating-badge">
              <span class="star">⭐</span>
              <span class="score">{{ review.rating }}</span>
            </div>
          </div>
          <p class="review-content">{{ review.content }}</p>
          <div class="review-footer">
            <span class="date">{{ formatDate(review.created_at) }}</span>
            <span class="like-info" v-if="review.like_count > 0">
              ❤️ {{ review.like_count }}
            </span>
          </div>
        </div>
        <div class="review-action">
          <span class="arrow-icon">›</span>
        </div>
      </div>

      <div class="pagination-wrapper" v-if="totalPages > 1">
        <button 
          class="page-nav-btn" 
          :disabled="currentPage === 1"
          @click="currentPage--"
        >
          이전
        </button>
        
        <div class="page-numbers">
          <button 
            v-for="page in totalPages" 
            :key="page"
            class="page-num-btn"
            :class="{ active: currentPage === page }"
            @click="currentPage = page"
          >
            {{ page }}
          </button>
        </div>

        <button 
          class="page-nav-btn" 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >
          다음
        </button>
      </div>
    </div>

    <div v-else class="empty-reviews">
      <div class="empty-icon">✍️</div>
      <p>아직 작성한 리뷰가 없습니다.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps(['reviews', 'reviewCount'])
const router = useRouter()

// 페이지네이션 상태
const currentPage = ref(1)
const itemsPerPage = 5 // 한 페이지에 보여줄 리뷰 개수

// [로직] 현재 페이지에 해당하는 리뷰들만 계산
const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return props.reviews.slice(start, end)
})

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(props.reviews.length / itemsPerPage)
})

// 리뷰 데이터가 바뀌면(예: 다른 프로필 이동) 1페이지로 초기화
watch(() => props.reviews, () => {
  currentPage.value = 1
})

const goDetail = (reviewId) => {
  router.push({ name: 'ReviewDetailView', params: { reviewId } })
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}
</script>

<style scoped>
/* 기존 스타일 유지 및 페이지네이션 스타일 추가 */
.profile-reviews-card {
  background-color: #FFFFFF;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.section-header {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #F0F0F0;
}

.section-title { font-size: 1.2rem; font-weight: 800; }
.section-title .count { color: #7A6CFA; margin-left: 4px; }

.review-item {
  display: flex;
  align-items: center;
  padding: 1.5rem 0;
  border-bottom: 1px solid #F8F9FA;
  cursor: pointer;
  transition: transform 0.2s;
}

.review-item:hover { transform: translateX(5px); }

.review-main { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.review-top { display: flex; align-items: center; gap: 12px; }
.movie-title { font-size: 1.1rem; font-weight: 700; color: #333; }

.rating-badge {
  display: flex; align-items: center; gap: 3px;
  background-color: #FFF9E6; padding: 2px 8px; border-radius: 12px;
  color: #FFB800; font-size: 0.85rem;
}

.review-content {
  font-size: 0.95rem; color: #666; line-height: 1.5;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  overflow: hidden;
}

.review-footer { display: flex; gap: 12px; font-size: 0.8rem; color: #AAA; }
.arrow-icon { font-size: 1.5rem; color: #DDD; }

/* [추가] 페이지네이션 디자인 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 2rem;
  padding-top: 1rem;
}

.page-numbers {
  display: flex;
  gap: 0.5rem;
}

.page-num-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #888;
  cursor: pointer;
  transition: all 0.2s;
}

.page-num-btn.active {
  background-color: #7A6CFA;
  color: white;
  font-weight: 700;
}

.page-num-btn:hover:not(.active) {
  background-color: #F0F0F0;
  color: #333;
}

.page-nav-btn {
  border: 1px solid #EEE;
  background-color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #666;
  cursor: pointer;
}

.page-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.empty-reviews { text-align: center; padding: 4rem 0; color: #AAA; }
</style>