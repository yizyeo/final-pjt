import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from movies.models import Movie
from reviews.models import Review

User = get_user_model()

class Command(BaseCommand):
    help = '영화를 위한 더미 리뷰 데이터를 생성합니다.'

    def handle(self, *args, **kwargs):
        # 1. 리뷰 내용 샘플 (블라인드 테스트에 어울리는 문구들)
        review_samples = [
            "진짜 인생 영화입니다. 초반 10분만 참으면 신세계가 열려요.",
            "배우들의 연기력이 미쳤습니다. 특히 눈빛 연기가 압권이네요.",
            "영상미 하나만으로도 볼 가치가 충분한 영화.",
            "생각없이 봤다가 오열하고 나왔습니다. 휴지 필수.",
            "스토리가 뻔한 것 같은데 연출이 기가 막혀서 시간 가는 줄 몰랐음.",
            "OST가 너무 좋아서 영화 끝나고 계속 찾아 듣는 중.",
            "결말을 보고 나서야 모든 장면이 이해가 가기 시작했다.",
            "호불호가 갈릴 수 있겠지만 저한테는 올해 최고의 영화였습니다.",
            "새벽에 혼자 보기에 딱 좋은 감성.",
            "극장에서 안 본 게 후회될 정도로 압도적인 스케일.",
            "감독의 천재성이 돋보이는 작품.",
            "가볍게 킬링타임용으로 봤는데 의외의 묵직한 메시지가 있네요.",
            "친구랑 같이 봤는데 끝나고 1시간 동안 토론함.",
            "우울할 때 보면 위로가 되는 따뜻한 영화.",
            "긴장감이 장난 아닙니다. 심장 쫄깃해지는 줄."
        ]

        # 2. 유저와 영화 가져오기
        users = User.objects.all()
        movies = Movie.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR('유저가 없습니다. 먼저 유저를 생성해주세요.'))
            return

        if not movies.exists():
            self.stdout.write(self.style.ERROR('영화 데이터가 없습니다. 먼저 영화를 저장해주세요.'))
            return

        # 3. 리뷰 생성 루프
        created_count = 0
        
        # 각 영화마다 1~3개의 리뷰를 랜덤하게 생성
        for movie in movies:
            # 50% 확률로 리뷰 생성 (너무 모든 영화에 있으면 재미없으니)
            if random.choice([True, False]): 
                continue
                
            # 영화당 1~3개 리뷰 생성
            for _ in range(random.randint(1, 3)):
                random_user = random.choice(users)
                random_content = random.choice(review_samples)
                
                # 이미 해당 유저가 이 영화에 리뷰를 썼는지 확인 (중복 방지)
                if Review.objects.filter(user=random_user, movie=movie).exists():
                    continue

                Review.objects.create(
                    user=random_user,
                    movie=movie,
                    content=random_content,
                    rating=random.randint(7, 10), # 추천용이니 높은 점수 위주
                    is_spoiler=False  # [중요] 스포일러 아님 설정
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'총 {created_count}개의 더미 리뷰가 생성되었습니다!'))