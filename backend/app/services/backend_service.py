from ..services.database import Base
import json

class DatabaseService:
    def __init__(self, database):
        self.database = database  # Instance de Database

    def get_movie_by_id(self, movie_id):
        """ Récupérer un film par son ID depuis la base de données """
        query = "SELECT * FROM movie WHERE id = :movie_id"
        result = self.database.fetch_all(query, {'movie_id': movie_id})
        return [dict(row) for row in result] if result else None  # Convertir en liste de dictionnaires

    def get_all_movies(self):
        """ Récupérer tous les films depuis la base de données """
        query = "SELECT * FROM movie"
        result = self.database.fetch_all(query)
        return [dict(row) for row in result]  # Convertir en liste de dictionnaires
    
    def search_movies(self, term):
        """ Rechercher des films par titre """
        query = "SELECT * FROM movie WHERE original_title LIKE :term"
        result = self.database.fetch_all(query, {'term': f'%{term}%'})
        print(result)
        # Convertir les résultats en liste de dictionnaires
        result = [dict(id=row[0], original_title=row[1], popularity=row[2], adult=row[3], video=row[4]) for row in result]
        return result
    
    def get_best_movies(self, limit=10, offset=0):
        """ Récupérer les films les mieux notés avec pagination """
        query = "SELECT * FROM movie ORDER BY popularity DESC LIMIT :limit OFFSET :offset"
        result = self.database.fetch_all(query, {'limit': limit, 'offset': offset})
        result = [dict(id=row[0], original_title=row[1], popularity=row[2], adult=row[3], video=row[4]) for row in result]
        return result
    
    def get_bad_movies(self, limit=10, offset=0):
        """ Récupérer les films les moins bien notés avec pagination """
        query = "SELECT * FROM movie ORDER BY popularity ASC LIMIT :limit OFFSET :offset"
        result = self.database.fetch_all(query, {'limit': limit, 'offset': offset})
        result = [dict(id=row[0], original_title=row[1], popularity=row[2], adult=row[3], video=row[4]) for row in result]
        return result