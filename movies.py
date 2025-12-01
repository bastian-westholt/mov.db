"""Movie Database Management Application.

This module provides a command-line interface for managing a movie database.
Users can add, delete, update, search, and sort movies, as well as view
statistics and get random movie recommendations.

The application uses an external storage module (movies_storage) to persist
movie data and provides a menu-driven interface for user interaction.
"""
import os.path

import movies_storage_sql as ms
import json
import sys
import random as rand


def exit_application():
    """Exit the application gracefully."""
    print('Bye!')
    return sys.exit()


def list_up_movies():
    """List all movies with their year and rating.

    Returns:
        list: Formatted strings containing movie title, year, and rating.
              Returns error message if database is empty.
    """
    movies = ms.get_movies()
    movies_lst = []
    for title, infos in movies.items():
        movies_lst.append(f'{title} ({infos['year']}): {infos['rating']}')
    if not movies_lst:
        return [f'Database is empty, add movies to database.']
    else:
        return movies_lst


def add_movie_to_dict():
    """Add a new movie to the database via user input.

    Prompts the user for movie title and fetches data from OMDB API.
    User can enter 'b' to return to the main menu.

    Returns:
        list: Success message or error message as list of strings.
    """
    while True:
        try:
            title = input('("b" = back to menu)\nEnter new movie name: ')
            if title == "b":
                break

            result = ms.add_movie(title)

            if result["success"]:
                return [f'\nMovie "{result["title"]}" ({result["year"]}) added successfully with rating {result["rating"]}.']
            elif result["reason"] == "not_found":
                return [f'\nError: Movie "{result["title"]}" not found in database.']
            elif result["reason"] == "duplicate":
                return [f'\nError: Movie "{result["title"]}" already exists in database.']
            elif result["reason"] == "database_error":
                return [f'\nDatabase error: {result["error"]}']
            elif result["reason"] == "api_connection":
                return [f'\nError: OMDb-API connection problem.']
            else:
                return [f'\nUnexpected error occurred.']

        except Exception as e:
            return [f'\nUnexpected error: {str(e)}']


def remove_movie_from_dict():
    """Delete a movie from the database via user input.

    Prompts the user for the movie title to delete.
    User can enter 'b' to return to the main menu.

    Returns:
        list: Success message if movie was deleted, error message otherwise.

    Raises:
        FileNotFoundError: If database file doesn't exist.
        JSONDecodeError: If database file is corrupted.
        PermissionError: If no permission to access database.
    """
    while True:
        try:
            movies = ms.get_movies()
            title = input('("b" = back to menu)\nEnter movie name to delete: ')
            if title == "b":
                break
            elif title in movies:
                ms.delete_movie(title)
                return [f'\nMovie "{title}" deleted successfully.']
            elif not movies:
                return [f'Database is empty, add movies to database.']
            else:
                return [f'Movie don´t exist!']

        except Exception as e:
            return [f'Unexpected error: {str(e)}']


def update_movie_from_dict():
    """Update the rating of an existing movie via user input.

    Prompts the user for the movie title and new rating.
    User can enter 'b' to return to the main menu.

    Returns:
        list: Success message if movie was updated, error message otherwise.

    Raises:
        FileNotFoundError: If database file doesn't exist.
        JSONDecodeError: If database file is corrupted.
        PermissionError: If no permission to access database.
    """
    while True:
        try:
            movies = ms.get_movies()
            title = input('("b" = back to menu)\nEnter movie name: ')
            if title == "b":
                break
            rating = movies[title]['rating']
            if title in movies:
                ms.update_movie(title, rating)
                return [f'\nMovie "{title}" updated successfully.']
            elif not movies:
                return [f'Database is empty, add movies to database.']
            else:
                return [f'Movie don´t exist!']
        except FileNotFoundError:
            return [f'Database file not found!']
        except json.JSONDecodeError:
            return [f'Database file is corrupted!']
        except PermissionError:
            return [f'No permission to access database!']
        except Exception as e:
            return [f'Unexpected error: {str(e)}']


def calc_stats_for_all_movies():
    """Calculate and return comprehensive statistics for all movies.

    Calculates average rating, median rating, best rated movie(s),
    and worst rated movie(s) from the database.

    Returns:
        tuple: Four strings containing average, median, best, and worst movie info.
               Returns error message list if database is empty or inaccessible.

    Raises:
        ZeroDivisionError: If database is empty.
        FileNotFoundError: If database file doesn't exist.
        JSONDecodeError: If database file is corrupted.
        PermissionError: If no permission to access database.
    """
    try:
        def calc_rating_average():
            """Calculate the average of all movie ratings.

            Returns:
                str: Formatted string with average rating rounded to 1 decimal.
            """
            movies = ms.get_movies()
            sum_ratings = 0
            for movie, infos in movies.items():
                sum_ratings += float(infos['rating'])
            average_rating = sum_ratings / len(movies)
            return f'Average rating: {round(average_rating, 1)}'

        def calc_rating_median():
            """Calculate the median of all movie ratings.

            Returns:
                str: Formatted string with median rating.
            """
            movies = ms.get_movies()
            rating_lst = [infos['rating'] for movie, infos in movies.items()]
            sorted_rating_lst = sorted(rating_lst)
            media_index = len(sorted_rating_lst) // 2
            return f'Median rating: {sorted_rating_lst[media_index]}'

        def return_best_movie():
            """Find the movie(s) with the highest rating.

            Returns:
                str: Formatted string with best rated movie(s).
            """
            movies = ms.get_movies()
            best_movie_rating = max(infos['rating'] for movie, infos in movies.items())
            best_movies_lst = [f'{movie} ({infos['year']}), {infos['rating']}' for movie, infos in movies.items() if infos['rating'] == best_movie_rating]
            best_movies_str = ', '.join(best_movies_lst)
            return f'Best movie: {best_movies_str}'

        def return_worst_movie():
            """Find the movie(s) with the lowest rating.

            Returns:
                str: Formatted string with worst rated movie(s).
            """
            movies = ms.get_movies()
            worst_movie_rating = min(infos['rating'] for movie, infos in movies.items())
            worst_movies_lst = [f'{movie} ({infos['year']}), {infos['rating']}' for movie, infos in movies.items() if infos['rating'] == worst_movie_rating]
            worst_movies_str = ', '.join(worst_movies_lst)
            return f'Worst movie: {worst_movies_str}'

        average = calc_rating_average()
        median = calc_rating_median()
        best_movie = return_best_movie()
        worst_movie = return_worst_movie()

        return average, median, best_movie, worst_movie
    except ZeroDivisionError:
        return [f'Database is empty, add movies to database.']
    except FileNotFoundError:
        return [f'Database file not found!']
    except json.JSONDecodeError:
        return [f'Database file is corrupted!']
    except PermissionError:
        return [f'No permission to access database!']
    except Exception as e:
        return [f'Unexpected error: {str(e)}']


def return_random_movie():
    """Select and return a random movie from the database.

    Returns:
        list: Formatted string with random movie title and rating,
              or error message if database is empty.

    Raises:
        ValueError: If database is empty.
        FileNotFoundError: If database file doesn't exist.
        JSONDecodeError: If database file is corrupted.
        PermissionError: If no permission to access database.
    """
    try:
        movies = ms.get_movies()
        if not movies:
            return ["Database is empty, add movies to database."]
        movies_lst = list(movies)
        movies_lst_len = len(movies_lst)
        random_movie = movies_lst[rand.randrange(movies_lst_len)]
        return [f'Your movie for tonight: {random_movie} with a rating of {movies[random_movie]['rating']}']
    except ValueError:
        return [f'[1mDatabase is empty, add movies to database.']
    except FileNotFoundError:
        return [f'Database file not found!']
    except json.JSONDecodeError:
        return [f'Database file is corrupted!']
    except PermissionError:
        return [f'No permission to access database!']
    except Exception as e:
        return [f'Unexpected error: {str(e)}']


def search_for_movie_in_dict():
    """Search for movies by partial title match (case-insensitive).

    Prompts the user for a search string and returns all movies
    whose titles contain that string.

    Returns:
        list: Formatted strings with matching movies, or error message
              if no matches found or database error occurs.

    Raises:
        ValueError: If database is empty.
        FileNotFoundError: If database file doesn't exist.
        JSONDecodeError: If database file is corrupted.
        PermissionError: If no permission to access database.
    """
    try:
        movies = ms.get_movies()
        search_request = input('Enter part of movie name: ')
        search_request_lower = search_request.lower()
        search_result = []
        for movie, infos in movies.items():
            if search_request_lower in movie.lower():
                search_result.append(f'\n{movie} ({infos['year']}): {infos['rating']}')
        if not search_result:
            return [f"\nCouldn't found movies with '{search_request}'"]
        return search_result
    except ValueError:
        return [f'[1mDatabase is empty, add movies to database.']
    except FileNotFoundError:
        return [f'Database file not found!']
    except json.JSONDecodeError:
        return [f'Database file is corrupted!']
    except PermissionError:
        return [f'No permission to access database!']
    except Exception as e:
        return [f'Unexpected error: {str(e)}']


def sort_movies_by_rating():
    """Sort movies by rating in descending order using manual sort algorithm.

    Implements a custom sorting algorithm without using built-in sort functions.

    Returns:
        list: Formatted strings with movies sorted by rating (highest first),
              or error message if database is empty or inaccessible.

    Raises:
        ValueError: If database is empty.
        FileNotFoundError: If database file doesn't exist.
        JSONDecodeError: If database file is corrupted.
        PermissionError: If no permission to access database.
    """
    try:
        movies = ms.get_movies()
        if not movies:
            return [f"Database is empty, add movies to database."]

        rating_lst = [(movie, infos['year'], infos['rating']) for movie, infos in movies.items()]
        sorted_lst = []

        while rating_lst:
            best_rating = 0.0
            best_movie = None

            for movie in rating_lst:
                current_rating = movie[2]
                if current_rating > best_rating:
                    best_rating = current_rating
                    best_movie = movie

            if best_movie:
                sorted_lst.append(best_movie)
                rating_lst.remove(best_movie)

        result_lst = [f'\n{movie} ({year}): {rating}' for movie, year, rating in sorted_lst]
        return result_lst
    except ValueError:
        return [f'Database is empty, add movies to database.']
    except FileNotFoundError:
        return [f'Database file not found!']
    except json.JSONDecodeError:
        return [f'Database file is corrupted!']
    except PermissionError:
        return [f'No permission to access database!']
    except Exception as e:
        return [f'Unexpected error: {str(e)}']


def sort_movies_by_year():
    """Sort movies by release year using manual sort algorithm.

    Implements a custom sorting algorithm without using built-in sort functions.
    Prompts user to choose between oldest first or youngest first.

    Returns:
        list: Formatted strings with movies sorted by year according to user choice,
              empty list if user cancels, or error message if database error occurs.

    Raises:
        ValueError: If database is empty.
        FileNotFoundError: If database file doesn't exist.
        JSONDecodeError: If database file is corrupted.
        PermissionError: If no permission to access database.
    """
    try:
        movies = ms.get_movies()
        if not movies:
            return [f"Database is empty, add movies to database."]

        year_lst = [(movie, infos['year'], infos['rating']) for movie, infos in movies.items()]
        sorted_lst = []

        while year_lst:
            youngest_year = 0
            youngest_movie = None

            for movie in year_lst:
                current_year = movie[1]
                if current_year > youngest_year:
                    youngest_year = current_year
                    youngest_movie = movie

            if youngest_movie:
                sorted_lst.append(youngest_movie)
                year_lst.remove(youngest_movie)

        while True:
            user_input = input("'b' = back to menu\n'old' = oldest movies first\n'young' = youngest movies first\nEnter your choice: ")
            if user_input == 'b':
                return []
            elif user_input == 'old':
                result_lst = [f'\n{movie} ({year}): {rating}' for movie, year, rating in reversed(sorted_lst)]
                return result_lst
            elif user_input == 'young':
                result_lst = [f'\n{movie} ({year}): {rating}' for movie, year, rating in sorted_lst]
                return result_lst
            else:
                print(f"Input invalid, only 'old' or 'new' are allowed.")

    except ValueError:
        return [f'Database is empty, add movies to database.']
    except FileNotFoundError:
        return [f'Database file not found!']
    except json.JSONDecodeError:
        return [f'Database file is corrupted!']
    except PermissionError:
        return [f'No permission to access database!']
    except Exception as e:
        return [f'Unexpected error: {str(e)}']


def generate_landing_page():

    def serialize_output(movies):
        output = ''
        print(movies)
        for movie in movies:
            output += f'    <li class="movie">\n'
            output += f'        <img class="movie-poster" src="{movie[3]}">\n'
            output += f'        <p class="movie-title">{movie[0]}</p>\n'
            output += f'        <p class="movie-year">{movie[1]}</p>\n'
            output += f'    </li>\n'
        return output


    def replace_template_with_output(output):
        with open(os.path.join('_static', 'index_template.html'), 'r') as Reader:
            template_content = Reader.readlines()

        html_content = []
        for line in template_content:
            if '__TEMPLATE_TITLE__' in line:
                line = line.strip().replace('__TEMPLATE_TITLE__', 'MOVIE-DB')
            elif '__TEMPLATE_MOVIE_GRID__' in line:
                line = line.strip().replace('__TEMPLATE_MOVIE_GRID__', output)
            html_content.append(line)

        with open(os.path.join('_static', 'index.html'), 'w') as Writer:
            Writer.writelines(html_content)


   # with open(os.path.join('_static', 'index.html'), 'w') as writer:
   #    writer.write(output)
    movies = ms.get_generation_data()
    html_output = serialize_output(movies)
    replace_template_with_output(html_output)


def main():
    """Run the main application loop with menu-driven interface.

    Displays a menu with options for managing the movie database and
    processes user selections in a continuous loop until exit is chosen.
    """
    menu_dict = {
        0: exit_application,
        1: list_up_movies,
        2: add_movie_to_dict,
        3: remove_movie_from_dict,
        4: update_movie_from_dict,
        5: calc_stats_for_all_movies,
        6: return_random_movie,
        7: search_for_movie_in_dict,
        8: sort_movies_by_rating,
        9: sort_movies_by_year,
        10: generate_landing_page
    }

    def enter_menu_tag():
        """Display the main menu and get user's menu choice.

        Returns:
            int: User's menu selection (0-9).
        """
        print()
        print(f'********** My Movies Database *********')
        print()
        print(f'0. Exit')
        print(f'1. List movies')
        print(f'2. Add movie')
        print(f'3. Delete movie')
        print(f'4. Update movie')
        print(f'5. Stats')
        print(f'6. Random movie')
        print(f'7. Search movie')
        print(f'8. Movies sorted by rating')
        print(f'9. Movies sorted by year')
        print(f'10. Generate Landing-Page')
        print()
        while True:
            try:
                user_entry = int(input('Enter choice (0-10):'))
                if user_entry < 0 or user_entry > 10:
                    print(f'\nInvalid number, only numbers between 0 and 8 allowed, try again.\n')
                    continue
                return user_entry
            except ValueError:
                print(f'\nEntered value invalid, only numbers allowed!\n')

    def enter_to_continue():
        """Pause execution until user presses Enter, then return to menu."""
        while True:
            input('Press Enter to continue')
            break
        execute_menu()

    def function_execution(user_entry):
        """Execute the selected menu function and display results.

        Args:
            user_entry (int): The menu option selected by the user.
        """
        try:
            if user_entry in menu_dict:
                print()
                for line in menu_dict[user_entry]():
                    print(line)
                print()
                enter_to_continue()
        except TypeError:
            execute_menu()

    def execute_menu():
        """Execute the main menu loop."""
        menu_input = enter_menu_tag()
        function_execution(menu_input)

    execute_menu()


if __name__ == "__main__":
    main()
