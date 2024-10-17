from flask import Blueprint, jsonify, request
from ..services.tmdb_service import TMDBService
from ..services.backend_service import DatabaseService
from ..services.database import database
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Créer un Blueprint
main = Blueprint('main', __name__)

executor = ThreadPoolExecutor()


tmdb_service = TMDBService()
backend_service = DatabaseService(database)

def fetch_movie_details(results):
    detailed_movies = []
    loop = asyncio.get_event_loop()
    
    print("Fetching movie details...")
    for movie in results:
        if isinstance(movie, dict) and 'id' in movie:
            # Exécutez la fonction synchrone get_movie_details dans le même pool
            movie_details = loop.run_in_executor(executor, tmdb_service.get_movie_details, movie['id'])
            movie_details = asyncio.run(movie_details)  # Attendre le résultat de la future
            # Déboguer le contenu de movie_details
            print("Movie details:", movie_details)
            
            if movie_details:  # Vérifiez si les détails ne sont pas None ou vides
                detailed_movies.append(movie_details)
            else:
                print(f"Aucun détail trouvé pour le film ID: {movie['id']}")
        else:
            print("Invalid movie format:", movie)
    
    return detailed_movies

async def fetch_movie_details(movie):
    return await tmdb_service.get_movie_details(movie['id'])

async def run_async_tasks(tasks):
    print("running async tasks", tasks)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(asyncio.gather(*tasks))
    print('results', results)
    loop.close()
    return results

@main.route('/api/trending', methods=['GET'])
def trending_movies():
    try:
        movies = tmdb_service.get_trending_movies()
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "La requête de recherche ne peut pas être vide"}), 400 
    try:
        results = backend_service.search_movies(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#get movie detail vy id
@main.route('/api/movie/<int:movie_id>', methods=['GET'])
def movie_detail(movie_id):
    try:
        movie = tmdb_service.get_movie_details(movie_id)
        return jsonify(movie)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route('/api/best', methods=['GET'])
async def best_movies():
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)

    try:
        # Utiliser le pool d'exécution pour exécuter l'appel synchrone
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(executor, backend_service.get_best_movies, limit, offset)


        if not isinstance(results, list):
            raise ValueError("Expected results to be a list.")

        detailed_movies = []

        print("Fetching movie details...")
        for movie in results:
            if isinstance(movie, dict) and 'id' in movie:
                # Exécutez la fonction synchrone get_movie_details dans le même pool
                movie_details = await loop.run_in_executor(executor, tmdb_service.get_movie_details, movie['id'])
                
                # Déboguer le contenu de movie_details
                print("Movie details:", movie_details)
                
                if movie_details:  # Vérifiez si les détails ne sont pas None ou vides
                    detailed_movies.append(movie_details)
                else:
                    print(f"Aucun détail trouvé pour le film ID: {movie['id']}")
            else:
                print("Invalid movie format:", movie)

        return jsonify(detailed_movies)

    except Exception as e:
        print(f"Erreur dans best_movies : {str(e)}")  # Ajouter un print pour déboguer les exceptions
        return jsonify({"error": str(e)}), 500

@main.route('/api/bad', methods=['GET'])
async def bad_movies():
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)

    try:
        # Utiliser le pool d'exécution pour exécuter l'appel synchrone
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(executor, backend_service.get_bad_movies, limit, offset)

        if not isinstance(results, list):
            raise ValueError("Expected results to be a list.")

        detailed_movies = []

        print("Fetching movie details for bad movies...")
        for movie in results:
            if isinstance(movie, dict) and 'id' in movie:
                # Exécutez la fonction synchrone get_movie_details dans le même pool
                movie_details = await loop.run_in_executor(executor, tmdb_service.get_movie_details, movie['id'])
                
                # Déboguer le contenu de movie_details
                print("Movie details for bad movie:", movie_details)
                
                if movie_details:  # Vérifiez si les détails ne sont pas None ou vides
                    detailed_movies.append(movie_details)
                else:
                    print(f"Aucun détail trouvé pour le film ID: {movie['id']}")
            else:
                print("Invalid movie format:", movie)

        return jsonify(detailed_movies)

    except Exception as e:
        print(f"Erreur dans bad_movies : {str(e)}")  # Ajouter un print pour déboguer les exceptions
        return jsonify({"error": str(e)}), 500