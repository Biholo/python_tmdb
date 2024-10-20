# TMDB Project

## Introduction
This project is a web application built with React for the frontend and Flask for the backend. It allows users to browse and search for movies using the TMDB API.

## Prerequisites
- Node.js
- npm (Node Package Manager)
- Python
- Flask

## Getting Started

### Frontend (React)
1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2. Install the dependencies:
    ```bash
    npm install
    ```
3. Start the React development server:
    ```bash
    npm run start
    ```
4. Open your browser and go to `http://localhost:3000` to see the application running.

### Backend (Flask)
1. Navigate to the backend directory:
    ```bash
    cd backend
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Start the Flask server:
    ```bash
    flask run
    ```
6. The Flask server will be running at `http://localhost:5000`.


### Database Setup

#### Initialize the Database
1. Navigate to the backend directory if you haven't already:
    ```bash
    cd backend
    ```
2. Initialize the database tables:
    ```bash
    flask init-database
    ```
   This command will create the necessary tables in your database.

#### Sync Database with TMDB
1. To populate the database with movie data from TMDB, run the following command:
    ```bash
    flask sync-database-movies
    ```
   This command will fetch movie data from the TMDB API and insert it into your database tables.


## License
This project is licensed under the MIT License.

## Acknowledgements
- [TMDB API](https://www.themoviedb.org/documentation/api)
- [React](https://reactjs.org/)
- [Flask](https://flask.palletsprojects.com/)
