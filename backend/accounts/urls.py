from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')), # dj_rest_auth.urls에 login, logout, user path 정의되어 있음
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('profile/<str:username>/', views.profile_detail),
    path('update/', views.user_update),
    path('generate-bio/', views.generate_ai_bio),
]
