import os
import re
import requests
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(settings.BASE_DIR) / '.env')

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

from movies.models import Movie, Genre  # Genre 추가


class Command(BaseCommand):
    help = 'TMDB API saved first movie data to DB.'

    def _contains_korean(self, text):
        """한글이 포함되어 있는지 확인"""
        if not text:
            return False
        return bool(re.search(r'[가-힣]', text))

    def _save_basic_movie_info(self, data, current_list_type):
        tmdb_id = data.get('id')
        title = data.get('title')
        
        if not tmdb_id:
            return False

        # 한국어 제목이 아니면 스킵
        if not self._contains_korean(title):
            return False

        genre_ids = data.get('genre_ids', [])  # 장르 ID 가져오기

        movie, created = Movie.objects.update_or_create(
            tmdb_id=tmdb_id,
            defaults={
                'title': title,
                'poster_path': data.get('poster_path'), 
                'release_date': data.get('release_date') or None, 
                'vote_average': data.get('vote_average'),
                'overview': data.get('overview'),
                'popularity': data.get('popularity'),
                'list_type': current_list_type,
            }
        )
        
        # ManyToMany 장르 설정
        if genre_ids:
            genres = Genre.objects.filter(genre_id__in=genre_ids)
            movie.genres.set(genres)
        
        return True

    def handle(self, *args, **options):
        if not TMDB_API_KEY:
            self.stdout.write(self.style.ERROR('TMDB_API_KEY .env file not setted'))
            return
            
        self.stdout.write(f"API key load okey, seeding start...")

        API_LISTS = ['now_playing', 'popular']
        MAX_PAGES = 300

        for list_type in API_LISTS:
            self.stdout.write(f"--- {list_type} list seeding start ---")
            saved_count = 0
            skipped_count = 0
            
            for page in range(2, MAX_PAGES + 1):
                url = f"https://api.themoviedb.org/3/movie/{list_type}?api_key={TMDB_API_KEY}&page={page}&language=ko-KR"
                
                try:
                    response = requests.get(url).json()
                except requests.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"API error: {e}"))
                    break

                if not response.get('results'):
                    break
                
                for movie_data in response.get('results', []):
                    if self._save_basic_movie_info(movie_data, list_type):
                        saved_count += 1
                    else:
                        skipped_count += 1
                    
                time.sleep(0.5)
                self.stdout.write(f"page {page} ok. (saved: {saved_count}, skipped: {skipped_count})")

        self.stdout.write(self.style.SUCCESS(f"first data seeding complete. total saved: {saved_count}, skipped: {skipped_count}"))