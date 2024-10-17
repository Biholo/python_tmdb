// ApiService.ts
class ApiService {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    // Récupérer les films tendance
    async getTrendingMovies(): Promise<any> {
        try {
            const response = await fetch(`${this.baseUrl}/api/trending`);
            if (!response.ok) {
                throw new Error(`Erreur: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération des films tendance:', error);
            throw error;
        }
    }

    // Rechercher des films
    async searchMovies(query: string): Promise<any> {
        if (!query) {
            throw new Error("La requête de recherche ne peut pas être vide");
        }
        try {
            const response = await fetch(`${this.baseUrl}/api/search?query=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error(`Erreur: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la recherche de films:', error);
            throw error;
        }
    }

    // Obtenir les détails d'un film par ID
    async getMovieDetails(movieId: number): Promise<any> {
        try {
            const response = await fetch(`${this.baseUrl}/api/movie/${movieId}`);
            if (!response.ok) {
                throw new Error(`Erreur: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Erreur lors de la récupération des détails du film avec ID ${movieId}:`, error);
            throw error;
        }
    }

    // Récupérer les meilleurs films
    async getBestMovies(limit: number = 10, offset: number = 1): Promise<any> {
        try {
            const response = await fetch(`${this.baseUrl}/api/best`);
            if (!response.ok) {
                throw new Error(`Erreur: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération des meilleurs films:', error);
            throw error;
        }
    }

    // Récupérer les mauvais films
    async getBadMovies(limit: number = 10, offset: number = 0): Promise<any> {
        try {
            const response = await fetch(`${this.baseUrl}/api/bad`);
            if (!response.ok) {
                throw new Error(`Erreur: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Erreur lors de la récupération des mauvais films:', error);
            throw error;
        }
    }
}

// Exemple d'utilisation
const apiService = new ApiService('http://localhost:5000'); // Remplace par l'URL de ton backend

export default apiService;