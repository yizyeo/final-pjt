// export const getTier = (count) => {
//   if (count >= 50) return { label: '시네마 마스터', icon: '/icons/rank_5.png' }
//   if (count >= 30) return { label: '시네필', icon: '/icons/rank_4.png' }
//   if (count >= 15) return { label: '영화 애호가', icon: '/icons/rank_3.png' }
//   if (count >= 3) return { label: '뉴비 평론가', icon: '/icons/rank_2.png' }
  
//   return { label: '관객', icon: '/icons/rank_1.png' }
// }

export const getTier = (count) => {
  if (count >= 50) return { label: '시네마 마스터', icon: '/icons/tier_5.png' }
  if (count >= 30) return { label: '시네필', icon: '/icons/tier_4.png' }
  if (count >= 15) return { label: '영화 애호가', icon: '/icons/tier_3.png' }
  if (count >= 3) return { label: '뉴비 평론가', icon: '/icons/tier_2.png' }
  
  return { label: '관객', icon: '/icons/tier_1.png' }
}