import random
import time
import openai
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from movies.models import Movie
from reviews.models import Review

User = get_user_model()

class Command(BaseCommand):
    help = '기존 유저를 활용하여 OpenAI(gpt-4o-mini)로 리뷰 데이터를 생성합니다.'

    def handle(self, *args, **kwargs):
        # 1. 유저 확인 (직접 만드신 유저들이 있는지 체크)
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('DB에 유저가 한 명도 없습니다. 먼저 유저를 생성해주세요!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'현재 등록된 {users.count()}명의 유저를 활용하여 리뷰를 작성합니다.'))

        # 2. 영화 데이터 확인
        movies = Movie.objects.all()
        if not movies.exists():
            self.stdout.write(self.style.ERROR('DB에 영화 데이터가 없습니다.'))
            return

        # 3. GMS 전용 OpenAI 클라이언트 설정
        try:
            client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY, 
                base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'OpenAI Client 설정 실패: {e}'))
            return

        # 4. 리뷰 생성 루프 (테스트용 상위 30개)
        target_movies = movies.order_by('-popularity')[:30]
        
        created_count = 0

        for movie in target_movies:
            # 이미 리뷰가 있는 영화는 건너뛰기
            if Review.objects.filter(movie=movie).exists():
                self.stdout.write(f"Pass: {movie.title} (이미 리뷰 존재)")
                continue

            try:
                self.stdout.write(f"Generating review for: {movie.title}...")

                # 프롬프트
                system_message = "당신은 영화를 사랑하는 열정적인 블로거입니다."
                user_prompt = f"""
                영화 제목: {movie.title}
                
                미션: 이 영화를 친구에게 강력 추천하는 짧은 리뷰를 1개 작성해줘.
                조건:
                1. 절대 영화 제목, 출연 배우, 줄거리, 결말 등 스포일러를 포함하지 말 것.
                2. 영화의 분위기, 배우의 연기, 연출 스타일 위주로 묘사할 것.
                3. 공백 포함 80자 이내로 짧고 임팩트 있게 작성할 것.
                4. 한국어 구어체(해요체)로 자연스럽게 쓸 것.
                5. "이 영화는..." 같은 지루한 시작 금지. 따옴표 없이 문장만 출력해.
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=120
                )

                content = response.choices[0].message.content.strip()
                content = content.replace('"', '').replace("'", "") # 따옴표 제거

                # DB 저장 (작성자는 랜덤 선택)
                Review.objects.create(
                    user=random.choice(users),
                    movie=movie,
                    content=content,
                    rating=random.randint(8, 10),
                    is_spoiler=False
                )
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Success: {content}"))
                
                time.sleep(0.5) # 속도 조절

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error generating review for {movie.title}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'작업 완료! 총 {created_count}개의 리뷰가 생성되었습니다.'))