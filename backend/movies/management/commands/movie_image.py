import os
import requests
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from pathlib import Path
from movies.models import Movie

# Load environment variables
load_dotenv(Path(settings.BASE_DIR) / '.env')
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

class Command(BaseCommand):
    help = 'Fetches movie backdrop images from TMDB API and updates the database.'

    def handle(self, *args, **options):
        # Check for API key
        if not TMDB_API_KEY:
            self.stdout.write(self.style.ERROR('TMDB_API_KEY not set in .env file'))
            return
            
        self.stdout.write(self.style.SUCCESS("Starting to fetch movie backdrop images..."))

        # Get movies, ordered by list_type and then by release_date for popular movies
        movies_now_playing = Movie.objects.filter(list_type='now_playing')
        movies_popular = Movie.objects.filter(list_type='popular').order_by('-release_date')
        
        movies_to_update = list(movies_now_playing) + list(movies_popular)

        for movie in movies_to_update:
            # Skip if backdrop_paths is already set
            if movie.backdrop_paths:
                self.stdout.write(self.style.WARNING(f"Backdrop paths for '{movie.title}' already exist. Skipping."))
                continue

            # API URL for movie images
            url = f"https://api.themoviedb.org/3/movie/{movie.tmdb_id}/images?api_key={TMDB_API_KEY}"
            
            try:
                # Fetch movie images
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                # Get backdrop file_paths (up to 5)
                backdrops = data.get('backdrops', [])
                backdrop_paths = [backdrop['file_path'] for backdrop in backdrops[:5]]

                if backdrop_paths:
                    # JSONField는 리스트를 직접 저장
                    movie.backdrop_paths = backdrop_paths
                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully saved backdrop paths for '{movie.title}'."))
                else:
                    self.stdout.write(self.style.WARNING(f"No backdrops found for '{movie.title}'."))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"API error for movie ID {movie.tmdb_id}: {e}"))
            
            # Respect API rate limits
            time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS("Movie backdrop image update process complete."))