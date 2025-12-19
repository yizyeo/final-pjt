import openai
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserUpdateSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail(request, username):
    person = get_object_or_404(User, username=username)
    serializer = ProfileSerializer(person)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_bio(request):
    import os
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"현재 로드된 API KEY 앞부분: {api_key[:10] if api_key else 'None'}")

    user = request.user
    
    favorite_genres = ", ".join([g.name_kr for g in user.favorite_genres.all()])
    # 좋아요 한 영화 (제목만 최대 10개)
    liked_movies = ", ".join([m.title for m in user.like_movies.all()[:10]])
    # 작성한 리뷰 (최근 10개)
    reviews = user.reviews.all()[:10]
    review_list = []
    for r in reviews:
        review_list.append(f"[{r.movie.title}] 평점:{r.rating}점 - {r.content[:100]}")
    review_contents = "\n".join(review_list)
    
    # 데이터 부재 시 처리
    favorite_genres = favorite_genres or "미설정"
    liked_movies = liked_movies or "아직 없음"
    review_contents = review_contents or "아직 작성한 리뷰가 없습니다."

    # GMS 전용 클라이언트 설정
    client = openai.OpenAI(
        api_key=settings.OPENAI_API_KEY, 
        base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
    )

    # 2. 프롬프트 설계
    system_message = "당신은 사용자의 영화 취향과 리뷰 톤을 분석해 위트 있고 독창적인 프로필 문구를 만드는 카피라이터입니다."
    user_prompt = f"""
    이 사용자의 영화 선호도와 리뷰 데이터를 분석해서 프로필 한 줄 소개를 작성해줘.
    
    [사용자 활동 데이터]
    - 선호 장르: {favorite_genres}
    - 좋아요 한 영화: {liked_movies}
    - 작성한 리뷰 및 평점: {review_contents}
    
    [작성 규칙]
    1. 반드시 한국어로 작성하고, 공백 포함 20자 이내일 것.
    2. 취향을 단순 나열하지 말고, 이 유저의 영화적 정체성을 닉네임처럼 표현할 수 있는 하나의 문장으로 정의할 것.
       (예: 'B급 감성을 사랑하는 냉철한 분석가', '로맨스 영화에 진심인 눈물 많은 관객' 등)
    3. 활동 데이터가 부족하다면, 선호 장르를 고려해서 이제 막 영화 여행을 시작하려는 설렘이나 취향을 찾아가는 중이라는 컨셉으로 멋지게 써줘.
    4. 리뷰의 말투(냉소적, 열정적, 간결함 등)가 있다면 소개 문구에도 그 분위기를 반영할 것.
    5. 예시는 참고용일 뿐 출력에 포함하지 말 것.
    6. 따옴표, 이모지나 불필요한 설명 없이 문장만 출력할 것.
    """

    try:
        # 3. OpenAI API 호출 (gpt-4o-mini 모델 사용)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7, # 창의성 조절 (0.0~1.0)
            max_tokens=50
        )
        
        ai_bio = response.choices[0].message.content.strip()
        
        user.bio = ai_bio
        user.save()
        
        return Response({'bio': ai_bio})

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return Response({'error': 'AI 문구 생성 중 오류가 발생했습니다.'}, status=500)