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
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('DB에 유저가 한 명도 없습니다. 먼저 유저를 생성해주세요.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'현재 등록된 {users.count()}명의 유저를 활용하여 리뷰를 작성합니다.'))

        movies = Movie.objects.all()
        if not movies.exists():
            self.stdout.write(self.style.ERROR('DB에 영화 데이터가 없습니다.'))
            return

        try:
            client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY, 
                base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'OpenAI Client 설정 실패: {e}'))
            return

        # 리뷰 생성 루프
        target_movies = movies.order_by('-popularity')[:150]
        
        created_count = 0

        for movie in target_movies:
            # 이미 리뷰가 있는 영화는 건너뛰기
            if Review.objects.filter(movie=movie).exists():
                self.stdout.write(f"Pass: {movie.title} (이미 리뷰 존재)")
                continue

            try:
                self.stdout.write(f"Generating review for: {movie.title}...")

                # 프롬프트
                system_message = "당신은 왓챠피디아 스타일의 한줄 영화 리뷰를 쓰는 평론가입니다. 과장 없이, 감상 포인트를 짚는 위트 있는 문장을 씁니다."
                user_prompt = f"""
                영화 제목: {movie.title}
                
                아래 예시와 같은 톤의 한줄 리뷰를 작성하세요.

                [리뷰 스타일 예시]
                - 벌써부터 사랑에 빠진 듯한 느낌
                - 부국제 평이 왜 좋았지?
                - 숨막힐 듯한 미장센과, 처절한 연기에 경의를 표하며
                - 여행은 좀 고독해도 좋다
                - 시작부터 끝까지 속도감 있게 몰아붙인다
                - 한걸음 한걸음 내려가는 자에 대한 연민과 위로

                [작성 규칙]
                1. 반드시 한 문장, 공백 포함 25~55자 이내
                2. 영화 제목, 배우 이름, 줄거리, 결말, 장르 직접 언급 금지
                3. 추천/비추천 표현 사용 금지 (재밌다, 꼭 봐라 등)
                4. 생각·해석보다 ‘보는 동안의 상태나 반응’ 위주로 작성
                5. 감탄사·이모지·따옴표 사용 금지
                6. 결과는 문장만 출력
                7. 반드시 긍정일 필요는 없으며, 의문·거리감·냉소적 시선도 허용
                8. 같은 문장 패턴 반복 금지 (예: “~하지만”, “~인데” 남용 금지)
                9. 어려운 추상어 사용 금지 (사유, 본질, 아이러니, 메타, 서사, 상징 등)
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
                content = content.replace('"', '').replace("'", "")

                # DB 저장 (작성자는 랜덤 선택)
                Review.objects.create(
                    user=random.choice(users),
                    movie=movie,
                    content=content,
                    rating=random.randint(5, 9),
                    is_spoiler=False
                )
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Success: {content}"))
                
                time.sleep(0.5)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error generating review for {movie.title}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'작업 완료! 총 {created_count}개의 리뷰가 생성되었습니다.'))