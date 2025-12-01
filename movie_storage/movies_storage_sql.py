from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import requests

load_dotenv()
OMDB_KEY = os.getenv('OMDB_API_KEY')
DB_URL = 'sqlite:///data/movies.db/'

engine = create_engine(DB_URL, echo=False)

with engine.connect() as connection:
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL
        )
    '''))
    connection.commit()

def get_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT title, year, rating "
            "FROM movies")
        )
        movies = result.fetchall()
        #print(movies)

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}

def get_generation_data():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT title, year, rating, poster "
            "FROM movies")
        )
        movies = result.fetchall()

    return movies

def add_movie(title):
    """Add a new movie to the database.

    Fetches movie data from OMDB API and adds it to the database.
    Checks for duplicates before inserting.

    Args:
        title (str): Movie title to search and add.

    Returns:
        dict: Status dictionary with success flag and details.
              Format: {"success": bool, "reason": str, "data": dict}
    """

    url = f'http://www.omdbapi.com/?apikey={OMDB_KEY}&t={title}'
    res = requests.get(url)
    parsed = res.json()

    if res.status_code != 200:
        return {"success": False, "reason": "api_connection", "title": title}

    if parsed["Response"] == 'False':
        return {"success": False, "reason": "not_found", "title": title}

    existing_movies = get_movies()
    if parsed["Title"] in existing_movies:
        return {"success": False, "reason": "duplicate", "title": parsed["Title"]}

    with engine.connect() as connection:
        try:
            connection.execute(text(
                "INSERT INTO movies (title, year, rating, poster) "
                "VALUES (:title, :year, :rating, :poster)"
            ), {"title": parsed["Title"], "year": parsed["Year"], "rating": parsed["imdbRating"], "poster": parsed["Poster"]})
            connection.commit()
            return {
                "success": True,
                "reason": "added",
                "title": parsed["Title"],
                "year": parsed["Year"],
                "rating": parsed["imdbRating"],
                "poser_image_url": parsed["Poster"]
            }
        except Exception as e:
            return {"success": False, "reason": "database_error", "error": str(e)}

def delete_movie(title):
    """Delete a movie from the database."""

    with engine.connect() as connection:
        try:
            connection.execute(text(
                "DELETE "
                "FROM movies "
                "WHERE title = :title"),
                {"title": title}
            )
            connection.commit()
            return True

        except Exception as e:
            return False

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text(
                "UPDATE movies "
                "SET rating = :rating "
                "WHERE title = :title"),
                {"title": title, "rating": rating}
            )
            connection.commit()
            return True

        except Exception as e:
            return False
