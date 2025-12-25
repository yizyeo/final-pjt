<template>
  <div class="review-detail-page">
    
    <div class="nav-header">
      <button @click="router.back()" class="back-btn" title="뒤로가기">
        <span class="icon">←</span>
      </button>
    </div>

    <div v-if="!reviewStore.currentReview" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else class="content-container">
      
      <header class="review-header">
        <div class="movie-thumbnail" @click="goMovie(reviewStore.currentReview.movie)">
          <img :src="getImageUrl(reviewStore.currentReview.movie_poster)" alt="poster">
        </div>

        <div class="header-text">
          <span class="category-label">Movie Review</span>
          
          <h1 class="movie-title" @click="goMovie(reviewStore.currentReview.movie)">
            {{ reviewStore.currentReview.movie_title }}
            <span class="go-icon">›</span>
          </h1>
          
          <div class="meta-row">
            <div 
              class="author-profile" 
              @click="goProfile(reviewStore.currentReview.username)"
            >
              <div class="tier-badge" :title="userTier.label">
                <img :src="userTier.icon" :alt="userTier.label" class="tier-img">
              </div>
              <div class="author-info">
                <span class="username">{{ reviewStore.currentReview.username }}</span>
                <span class="date">{{ formatDate(reviewStore.currentReview.created_at) }}</span>
              </div>
            </div>
            
            <div class="rating-badge">
              <span class="star">⭐</span>
              <span class="score">{{ reviewStore.currentReview.rating }}</span>
            </div>
          </div>
        </div>

        <div v-if="accountStore.username === reviewStore.currentReview.username && !isEditing" class="owner-actions">
          <button @click="toggleEdit" class="text-btn">수정</button>
          <span class="divider">|</span>
          <button @click="handleDelete" class="text-btn delete">삭제</button>
        </div>
      </header>

      <main class="review-body">
        
        <div v-if="isEditing" class="edit-form-card">
          <h3 class="edit-title">리뷰 수정</h3>
          
          <div class="form-group">
            <label>평점</label>
            <div class="star-rating-input" @mouseleave="hoverRating = 0">
              <div class="stars">
                <div 
                  v-for="n in 5" 
                  :key="n" 
                  class="star-wrapper"
                >
                  <div class="star-visual" :class="getStarState(n)">
                    ★
                  </div>

                  <div 
                    class="click-area left"
                    @mouseover="hoverRating = (n * 2) - 1"
                    @click="setRating((n * 2) - 1)"
                  ></div>
                  
                  <div 
                    class="click-area right"
                    @mouseover="hoverRating = n * 2"
                    @click="setRating(n * 2)"
                  ></div>
                </div>
              </div>
              
              <span class="rating-text">
                {{ hoverRating || editData.rating }}점
              </span>
            </div>
          </div>
          
          <div class="form-group">
            <label>내용</label>
            <textarea 
              v-model="editData.content" 
              rows="8" 
              class="custom-textarea"
              placeholder="영화에 대한 감상을 자유롭게 남겨주세요."
            ></textarea>
          </div>
          
          <div class="edit-actions">
            <button @click="toggleEdit" class="btn-cancel">취소</button>
            <button @click="handleUpdate" class="btn-save">수정 완료</button>
          </div>
        </div>

        <div v-else class="view-mode">
          <div v-if="reviewStore.currentReview.is_spoiler && !showSpoilerDetail" class="spoiler-warning">
            <p>⚠️ 스포일러가 포함된 리뷰입니다.</p>
            <button @click="showSpoilerDetail = true" class="spoiler-btn">내용 보기</button>
          </div>
          <div v-else class="review-text">
            {{ reviewStore.currentReview.content }}
          </div>
        </div>
      </main>

      <section class="action-section">
        <button 
          @click="reviewStore.likeReview(reviewStore.currentReview.id)" 
          class="like-btn"
          :class="{ active: reviewStore.currentReview.is_liked }"
        >
          <span class="icon">{{ reviewStore.currentReview.is_liked ? '❤️' : '🤍' }}</span>
          <span class="label">좋아요</span>
          <span class="count">{{ reviewStore.currentReview.like_count }}</span>
        </button>
      </section>

      <hr class="section-divider">

      <section class="comment-section">
        <h3 class="section-title">
          댓글 <span class="count">{{ reviewStore.currentReview.comments?.length || 0 }}</span>
        </h3>
        
        <div class="comment-form-wrapper">
          <CommentForm @submit-comment="submitComment" />
        </div>

        <div class="comment-list">
          <div v-if="!reviewStore.currentReview.comments?.length" class="empty-comment">
            <p>아직 댓글이 없습니다. 첫 번째 댓글을 남겨보세요!</p>
          </div>
          
          <CommentItem 
            v-for="comment in reviewStore.currentReview.comments" 
            :key="comment.id" 
            :comment="comment"
            :currentUsername="accountStore.username"
            @delete-comment="deleteComment"
          />
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReviewStore } from '@/stores/review'
import { useAccountStore } from '@/stores/accounts'
import { getTier } from '@/utils/tierUtils'
import CommentForm from '@/components/review/CommentForm.vue'
import CommentItem from '@/components/review/CommentItem.vue'

const route = useRoute()
const router = useRouter()
const reviewStore = useReviewStore()
const accountStore = useAccountStore()

const isEditing = ref(false)
const showSpoilerDetail = ref(false)
const editData = ref({ content: '', rating: 0 })

const hoverRating = ref(0)

onMounted(async () => {
  await reviewStore.getReviewDetail(route.params.reviewId)
  
  if (reviewStore.currentReview) {
    editData.value.content = reviewStore.currentReview.content
    editData.value.rating = reviewStore.currentReview.rating
  }
})

const userTier = computed(() => {
  if (!reviewStore.currentReview) return getTier(0)
  return getTier(reviewStore.currentReview.user_review_count || 0)
})

const getImageUrl = (path) => path ? `https://image.tmdb.org/t/p/w200${path}` : '/no-image.png'

const goMovie = (movie) => {
  const movieId = (typeof movie === 'object') ? (movie.tmdb_id || movie.id) : movie
  router.push({ name: 'MovieDetailView', params: { movieId: movieId } })
}

const goProfile = (username) => {
  router.push({ name: 'ProfileView', params: { username: username } })
}

const toggleEdit = () => {
  isEditing.value = !isEditing.value
  if (isEditing.value && reviewStore.currentReview) {
    editData.value.content = reviewStore.currentReview.content
    editData.value.rating = reviewStore.currentReview.rating
  }
}

const getStarState = (index) => {
  const targetScore = hoverRating.value || editData.value.rating
  const starScore = index * 2

  if (targetScore >= starScore) {
    return 'full'
  } else if (targetScore >= starScore - 1) {
    return 'half'
  } else {
    return 'empty'
  }
}

const setRating = (score) => {
  editData.value.rating = score
}

const handleUpdate = async () => {
  try {
    await reviewStore.updateReview(route.params.reviewId, editData.value)
    isEditing.value = false
    alert('수정되었습니다.')
  } catch (err) {
    alert('수정 실패')
  }
}

const handleDelete = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await reviewStore.deleteReview(route.params.reviewId)
    alert('삭제되었습니다.')
    router.push({ name: 'ReviewListView' })
  } catch (err) {
    alert('삭제 실패')
  }
}

const submitComment = async (content) => {
  try {
    await reviewStore.createComment(route.params.reviewId, content)
  } catch (err) {
    alert('댓글 등록 실패')
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  try {
    await reviewStore.deleteComment(route.params.reviewId, commentId)
  } catch (err) {
    alert('댓글 삭제 실패')
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ko-KR', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}
</script>

<style scoped>
.review-detail-page {
  width: 100%;
  min-height: 100vh;
  background-color: #FFFFFF;
  padding-bottom: 4rem;
}

/* 네비게이션 헤더 */
.nav-header {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem 1.5rem 0.5rem;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid #EEEEEE;
  background-color: #FFFFFF;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.back-btn:hover {
  background-color: #F5F5F5;
  transform: translateX(-2px);
}

.back-btn .icon {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 2px;
}

/* 컨텐츠 컨테이너 */
.content-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* 리뷰 헤더 */
.review-header {
  margin-top: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #F0F0F0;
  padding-bottom: 2rem;
  display: flex; 
  gap: 1.5rem;
  position: relative;
}

.movie-thumbnail {
  width: 80px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.movie-thumbnail:hover {
  transform: scale(1.05);
}

.movie-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.category-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #7A6CFA;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.movie-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #111111;
  margin-bottom: 0.8rem;
  line-height: 1.2;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}

.movie-title:hover {
  text-decoration: underline;
}

.go-icon {
  font-size: 1.2rem;
  color: #CCCCCC;
  font-weight: 400;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.author-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  /* [추가] 클릭 가능 스타일 */
  cursor: pointer;
  transition: opacity 0.2s;
}

/* [추가] 호버 효과 */
.author-profile:hover {
  opacity: 0.7;
}

.tier-badge {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #F5F5F5;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.tier-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 700;
  color: #333333;
  font-size: 0.9rem;
}

.date {
  font-size: 0.8rem;
  color: #999999;
}

.rating-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: #FFF9E6;
  padding: 4px 10px;
  border-radius: 20px;
  color: #FFB800;
}

.rating-badge .score {
  font-weight: 800;
  font-size: 1rem;
  color: #333333;
}

.owner-actions {
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  gap: 8px;
  font-size: 0.8rem;
}

.text-btn {
  background: none;
  border: none;
  color: #999999;
  cursor: pointer;
  padding: 4px;
}

.text-btn:hover {
  color: #333333;
  text-decoration: underline;
}

.text-btn.delete:hover {
  color: #FF4444;
}

.divider {
  color: #E0E0E0;
}

/* 본문 영역 */
.review-body {
  margin-bottom: 3rem;
  min-height: 120px;
}

.review-text {
  font-size: 1.05rem;
  line-height: 1.8;
  color: #333333;
  white-space: pre-wrap;
}

/* 스포일러 경고 */
.spoiler-warning {
  background-color: #F9F9F9;
  border-radius: 12px;
  padding: 2.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.spoiler-btn {
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.spoiler-btn:hover {
  background-color: #F0F0F0;
}

/* 수정 폼 스타일 개선 */
.edit-form-card {
  background-color: #FFFFFF;
  border: 1px solid #EEEEEE;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  padding: 2rem;
  border-radius: 16px;
}

.edit-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: #111111;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #333333;
}

/* 커스텀 셀렉트 박스 */
.custom-select-wrapper {
  position: relative;
  width: 150px;
}

.custom-select {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #DDDDDD;
  background-color: #FFFFFF;
  appearance: none;
  font-family: inherit;
  font-size: 0.95rem;
  cursor: pointer;
  transition: border-color 0.2s;
}

.custom-select:focus {
  border-color: #7A6CFA;
  outline: none;
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.8rem;
  color: #888;
  pointer-events: none;
}

/* 커스텀 텍스트에어리어 */
.custom-textarea {
  width: 100%;
  padding: 14px;
  border: 1px solid #DDDDDD;
  border-radius: 12px;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.6;
  resize: vertical;
  background-color: #FAFAFA;
  transition: all 0.2s;
}

.custom-textarea:focus {
  background-color: #FFFFFF;
  border-color: #7A6CFA;
  box-shadow: 0 0 0 3px rgba(122, 108, 250, 0.1);
  outline: none;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 2rem;
}

.btn-save {
  background-color: #7A6CFA;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background-color 0.2s;
}

.btn-save:hover {
  background-color: #6656E0;
}

.btn-cancel {
  background-color: white;
  border: 1px solid #DDDDDD;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.95rem;
  color: #555555;
}

.btn-cancel:hover {
  background-color: #F5F5F5;
}

/* 별점 입력 컨테이너 */
.star-rating-input {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stars {
  display: flex;
  gap: 2px;
}

/* 개별 별 래퍼 (상대 위치 기준점) */
.star-wrapper {
  position: relative;
  width: 32px;
  height: 32px;
  cursor: pointer;
}

/* 시각적 별 아이콘 */
.star-visual {
  font-size: 2rem;
  line-height: 1;
  color: #E0E0E0;
  transition: all 0.1s;
}

/* 꽉 찬 별 */
.star-visual.full {
  color: #FFB800;
}

/* 반 개 별 */
.star-visual.half {
  background: linear-gradient(to right, #FFB800 50%, #E0E0E0 50%);
  -webkit-background-clip: text;
  color: transparent;
}

/* 클릭 영역 */
.click-area {
  position: absolute;
  top: 0;
  height: 100%;
  width: 50%;
  z-index: 10;
}

.click-area.left {
  left: 0;
}

.click-area.right {
  right: 0;
}

.star-wrapper:active {
  transform: scale(0.9);
}

.rating-text {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333333;
  min-width: 40px;
}

/* 액션 (좋아요) */
.action-section {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.8rem 2.5rem;
  border-radius: 50px;
  border: 1px solid #E0E0E0; 
  background-color: white;
  color: #555555;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.like-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

.like-btn.active {
  border-color: #FF4444;
  background-color: #FFF0F0; 
  color: #FF4444; 
  font-weight: 600;
}

.like-btn .count {
  font-weight: 700;
  margin-left: 4px;
}

.section-divider {
  border: none;
  border-top: 1px solid #EEEEEE;
  margin-bottom: 3rem;
}

/* 댓글 섹션 */
.comment-section {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
}

.section-title .count {
  color: #7A6CFA;
  margin-left: 4px;
}

.comment-form-wrapper {
  margin-bottom: 2rem;
}

.empty-comment {
  text-align: center;
  padding: 3rem;
  color: #888888;
  background-color: #FAFAFA;
  border-radius: 12px;
}

/* 로딩 스피너 */
.loading-state {
  display: flex;
  justify-content: center;
  padding-top: 5rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #F3F3F3;
  border-top: 4px solid #7A6CFA;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .review-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .movie-thumbnail {
    width: 60px;
    height: 90px;
  }
  
  .owner-actions {
    position: relative;
    margin-top: 0.5rem;
    justify-content: flex-start;
  }
  
  .movie-title {
    font-size: 1.4rem;
  }
}
</style>