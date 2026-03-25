MENU_PROMPT = "\n Enter 'a' to add movie, 'l' to see your movies, 'f' to find a movie by title, or 'q' to quit: "

movies = []


def add_movie():
    title = input("enter the movie title")
    director = input("enter the movie director")
    year = input("enter the movie release year")

    movies.append({
        'title': title,
        'director': director,
        'year': year
    })


def show_movies():
    for movie in movies:
        print_movie(movie) #create to avoid duplication


def print_movie(movie):
    print(f"Title: {movie['title']}")
    print(f"Director: {movie['director']}")
    print(f"Release year: {movie['year']}")


def find_movies():
    search_title = input("enter movie title your looking for: ")
    for movie in movies:
        if movie['title'] == search_title:
            print_movie(movie)
        else:
            print(f"{search_title} is not in the movie list please try again")
            search_title = input("enter movie title your looking for: ")



user_options ={
    "a": add_movie,
    "l": show_movies,
    "f": find_movies
}
def menu():
    selection = input(MENU_PROMPT)
    while selection != 'q':
        if selection in user_options:       
            selected_function = user_options[selection]
            selected_function()
        else:
            print("unknown command. please try aigain")
        selection = input(MENU_PROMPT)
                                                                           
menu()
                                                                                                                                                                               
