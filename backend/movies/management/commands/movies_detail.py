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
    help = 'Fetches movie details (runtime) from TMDB API and updates the database.'

    def handle(self, *args, **options):
        # Check for API key
        if not TMDB_API_KEY:
            self.stdout.write(self.style.ERROR('TMDB_API_KEY not set in .env file'))
            return
            
        self.stdout.write(self.style.SUCCESS("Starting to fetch movie runtimes..."))

        # Get movies, ordered by list_type and then by release_date for popular movies
        movies_now_playing = Movie.objects.filter(list_type='now_playing')
        movies_popular = Movie.objects.filter(list_type='popular').order_by('-release_date')
        
        movies_to_update = list(movies_now_playing) + list(movies_popular)

        for movie in movies_to_update:
            # Skip if runtime is already set
            if movie.runtime:
                self.stdout.write(self.style.WARNING(f"Runtime for '{movie.title}' already exists. Skipping."))
                continue

            # API URL for movie details
            url = f"https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={TMDB_API_KEY}&language=ko-KR"
            
            try:
                # Fetch movie details
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()

                # Get runtime from response
                runtime = data.get('runtime')

                if runtime:
                    # Update and save the movie object
                    movie.runtime = runtime
                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully updated runtime for '{movie.title}'."))
                else:
                    self.stdout.write(self.style.WARNING(f"No runtime found for '{movie.title}'."))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"API error for movie ID {movie.tmdb_id}: {e}"))
            
            # Respect API rate limits
            time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS("Movie runtime update process complete."))