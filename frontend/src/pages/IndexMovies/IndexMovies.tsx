import { useState, useEffect } from 'react'
// import { Search } from 'lucide-react'
import apiService from '@/api/backendApi'

type Movie = {
  id: number
  title: string
  poster_path: string | null
  vote_average: number
  popularity: number
  overview: string
  release_date: string
}

type MovieRowProps = {
  title: string
  movies: Movie[]
  onMovieClick: (movie: Movie) => void
}

const MovieRow = ({ title, movies, onMovieClick }: MovieRowProps) => (
  <div className="mb-8">
    <h2 className="text-2xl font-bold mb-4">{title}</h2>
    <div className="flex overflow-x-auto space-x-4 pb-4">
      {movies.map((movie) => (
        <div key={movie.id} className="flex-none w-48 cursor-pointer" onClick={() => onMovieClick(movie)}>
          <div className="relative h-72 w-48 mb-2">
            <img
              src={movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : '/placeholder.svg'}
              alt={movie.title}
              className="w-full h-full object-cover rounded-lg"
            />
            <div className="absolute top-2 right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded-full text-sm">
              {movie.vote_average.toFixed(1)}
            </div>
          </div>
          <h3 className="text-sm font-semibold truncate">{movie.title}</h3>
        </div>
      ))}
    </div>
  </div>
)

export default function IndexMovies() {
  const [searchTerm, setSearchTerm] = useState('')
  const [searchResults, setSearchResults] = useState<Movie[]>([])
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const [trendingMovies, setTrendingMovies] = useState<Movie[]>([])
  const [topRatedMovies, setTopRatedMovies] = useState<Movie[]>([])
  const [lowestRatedMovies, setLowestRatedMovies] = useState<Movie[]>([])
  useEffect(() => {
    apiService.getBestMovies().then((movies) => {
      setTopRatedMovies(movies)
      console.log('Meilleurs films:', movies)
    }).catch((error) => {
      console.error('Erreur lors de la récupération des meilleurs films:', error)
    })

    apiService.getBadMovies().then((movies) => {
      setLowestRatedMovies(movies)
      console.log('Mauvais films:', movies)
    }).catch((error) => {
      console.error('Erreur lors de la récupération des mauvais films:', error)
    })

    apiService.getTrendingMovies().then((movies) => {
      setTrendingMovies(movies.results)
      console.log('Films tendances:', movies)
    }).catch((error) => {
      console.error('Erreur lors de la récupération des films tendances:', error)
    })
  }, [])

  useEffect(() => {
    console.log(trendingMovies)
  }, [trendingMovies])

  useEffect(() => {
    if (searchTerm) {
      if (searchTerm.length > 3) {

        apiService.searchMovies(searchTerm).then((movies) => {

            setSearchResults(movies)
          
        }).catch((error) => {
          console.error('Erreur lors de la recherche de films:', error)
        }
        )
      }
    } else {
      if (searchResults.length > 0) {
        setSearchResults([])
      }
    }
  }, [searchTerm])

  useEffect(() => {
    console.log('result',searchResults)
  }, [searchResults])

  const handleMovieClick = (movie: Movie) => {
    setSelectedMovie(movie)
    setIsModalOpen(true)
  }

  const loadDetailMovie = (movie: Movie) => {
    apiService.getMovieDetails(movie.id).then((movie) => {
      setSelectedMovie(movie)
      setIsModalOpen(true)
      setSearchResults([])
    })
  }

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <div className="mb-8">
        <div className="relative">
          <input
            type="text"
            placeholder="Rechercher un film..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-gray-800 text-white"
          />
          {/* <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" /> */}
        </div>
        {searchResults.length > 0 && (
          <div className="absolute z-10 mt-2 w-full bg-gray-800 rounded-lg shadow-lg">
            {searchResults.slice(0, 10).map(movie => (
              <div
                key={movie.id}
                className="px-4 py-2 hover:bg-gray-700 cursor-pointer"
                onClick={() => loadDetailMovie(movie)}
              >
                {movie.original_title}
              </div>
            ))}
          </div>
        )}
      </div>

      <MovieRow title="Films tendances" movies={trendingMovies} onMovieClick={handleMovieClick} />
      <MovieRow title="Meilleurs films" movies={topRatedMovies} onMovieClick={handleMovieClick} />
      <MovieRow title="Films les moins bien notés" movies={lowestRatedMovies} onMovieClick={handleMovieClick} />

      {isModalOpen && selectedMovie && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-gray-800 p-6 rounded-lg max-w-2xl w-full">
            <h2 className="text-2xl font-bold mb-4">{selectedMovie.title}</h2>
            <div className="grid gap-4">
              {selectedMovie.poster_path && (
                <img
                  src={`https://image.tmdb.org/t/p/w500${selectedMovie.poster_path}`}
                  alt={selectedMovie.title}
                  className="w-full max-w-sm mx-auto rounded-lg"
                />
              )}
              <div>
                <p><strong>Note :</strong> {selectedMovie.vote_average.toFixed(1)}/10</p>
                <p><strong>Date de sortie :</strong> {selectedMovie.release_date}</p>
                <p><strong>Synopsis :</strong> {selectedMovie.overview}</p>
              </div>
            </div>
            <button
              onClick={() => setIsModalOpen(false)}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Fermer
            </button>
          </div>
        </div>
      )}
    </div>
  )
}