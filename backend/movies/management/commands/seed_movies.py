
import os
import requests
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(settings.BASE_DIR) / '.env')

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

from movies.models import Movie 


class Command(BaseCommand):
    help = 'TMDB API saved first movie data to DB.'

    def _save_basic_movie_info(self, data, current_list_type):
        tmdb_id = data.get('id')
        if not tmdb_id:
            return

        Movie.objects.update_or_create(
            tmdb_id=tmdb_id,
            defaults={
                'title': data.get('title'),
                'poster_path': data.get('poster_path'), 
                'release_date': data.get('release_date') or None, 
                'vote_average': data.get('vote_average'),
                'overview': data.get('overview'), 
                'genres': data.get('genre_ids'),
                'list_type': current_list_type,
            }
        )

    def handle(self, *args, **options):
        if not TMDB_API_KEY:
            self.stdout.write(self.style.ERROR('TMDB_API_KEY .env file not setted'))
            return
            
        self.stdout.write(f"API key load okey, seeding start...")

        API_LISTS = ['now_playing', 'popular'] 
        MAX_PAGES = 100

        for list_type in API_LISTS:
            self.stdout.write(f"--- {list_type} list seeding start ---")
            
            for page in range(1, MAX_PAGES + 1):
                url = f"https://api.themoviedb.org/3/movie/{list_type}?api_key={TMDB_API_KEY}&page={page}&language=ko-KR"
                
                try:
                    response = requests.get(url).json()
                except requests.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"API error: {e}"))
                    break

                if not response.get('results'):
                    break
                
                for movie_data in response.get('results', []):
                    self._save_basic_movie_info(movie_data, list_type) 
                    
                time.sleep(0.5)
                self.stdout.write(f"page {page} ok. (total {list_type} {page*20} saved)")

        self.stdout.write(self.style.SUCCESS("first data seeding complete."))
