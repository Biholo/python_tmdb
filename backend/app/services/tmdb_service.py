import requests
import time
from requests.exceptions import HTTPError
from tenacity import retry, wait_exponential, stop_after_attempt
from flask import current_app
from cachetools import TTLCache

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, app=None):
        self.cache = TTLCache(maxsize=100, ttl=3600)
        if app is not None:
            # self.api_key = app.config['TMDB_API_KEY']  # Ancien modèle avec clé API
            self.bearer_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MDZjOThhMDI5N2RlZGJkMTU2NzgzODljOTExNjgwOCIsIm5iZiI6MTcyOTE0OTI0NS4zNTE1NjYsInN1YiI6IjY2MDk1MzM5YTg5NGQ2MDE0OTYyZmYyYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.bGzxBmc6TWfGU1flKJuzaFgjLyE3Mb6UtEkI-m9rWOM'

    def create_headers(self):
        return {
            "accept": "application/json",
            # "Authorization": f"Bearer {self.bearer_token}"
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MDZjOThhMDI5N2RlZGJkMTU2NzgzODljOTExNjgwOCIsIm5iZiI6MTcyOTE0OTI0NS4zNTE1NjYsInN1YiI6IjY2MDk1MzM5YTg5NGQ2MDE0OTYyZmYyYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.bGzxBmc6TWfGU1flKJuzaFgjLyE3Mb6UtEkI-m9rWOM"
        }

    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def api_request(self, endpoint, params=None):
        if params is None:
            params = {}

        print(f"Appel API vers {endpoint} avec les paramètres {params}")

        # Construire l'URL complète
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Clé unique pour le cache
        cache_key = (url, tuple(params.items()))
        print(f"Clé de cache : {cache_key}")

        # Faire l'appel API
        try:
            print(f"Appel API vers {url}")
            response = requests.get(url, headers=self.create_headers(), params=params)
            response.raise_for_status()
            print('Response:', response)

            result = response.json()

            # Stocker le résultat dans le cache
            self.cache[cache_key] = result
            print('Response.json:', response.json())

            return result

        except HTTPError as http_err:
            status_code = http_err.response.status_code
            if status_code == 429:
                print(f"Trop de requêtes. Attente de {http_err.response.headers.get('Retry-After', 1)} secondes.")
                time.sleep(int(http_err.response.headers.get('Retry-After', 1)))
            elif status_code in [500, 503]:
                print(f"Erreur serveur {status_code}, nouvelle tentative en cours...")
            elif status_code == 401:
                print("Erreur 401 : Token manquant ou invalide.")
            elif status_code == 403:
                print("Erreur 403 : Accès interdit.")
            elif status_code == 404:
                print("Erreur 404 : Ressource non trouvée.")
            else:
                print(f"Erreur HTTP {status_code} : {http_err}")
            raise
        except Exception as err:
            print(f"Erreur inattendue : {err}")
            raise

    # def api_request(self, endpoint, params=None):
    #     if params is None:
    #         params = {}

    #     # Construire l'URL complète
    #     url = f"{self.BASE_URL}/{endpoint}"

    #     print(f"Appel API vers {url} avec les paramètres {params}")

    #     # Ajouter les headers avec le token Bearer
    #     headers = {
    #         "accept": "application/json",
    #         "Authorization": f"Bearer {self.bearer_token}"
    #     }
    #     print(headers)
    #     # Faire l'appel API
    #     response = requests.get(url, headers=headers, params=params)
    #     response.raise_for_status()  # Cela lèvera une exception pour les erreurs HTTP

    #     return response.json()  # Retourne les données JSON directemen

    # Méthode pour obtenir les films tendances
    def get_trending_movies(self):
        return self.api_request("movie/popular", params={})

    def get_movie_details(self, movie_id):
        return self.api_request(f"movie/{movie_id}", params={})