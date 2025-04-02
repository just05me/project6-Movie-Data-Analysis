import requests

# Функция для получения фильмов c API
def get_movies_from_api(start_date, end_date):
    api_key = "APIkey"
    all_movies = []

    # Датa в формате - "гггг-мм"
    start_year = start_date.split(".")[1]
    end_year = end_date.split(".")[1]
    
    # Проходимся по годам
    for year in range(int(start_year), int(end_year) + 1):

        url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_year={year}"

        # Сохраняет данные
        response = requests.get(url)

        # Преобразуем в Json
        data = response.json()  

        # Фильмы
        movies = data["results"]
        
        # Добавляем фильмы в список
        for movie in movies:
            movie_info = {
                "title": movie["title"],
                "rating": movie["vote_average"],
                "release_date": movie["release_date"]
            }
            all_movies.append(movie_info)

    return all_movies

# Функция фильтрации
def filter_movies(movie_list, start_date, end_date, min_rating):
    # Список для подходящих фильмов
    filtered_movies = []  
    
    # Превращаем даты в числа для сравнения
    start_month = int(start_date.split(".")[0])
    start_year = int(start_date.split(".")[1])

    end_month = int(end_date.split(".")[0])
    end_year = int(end_date.split(".")[1])
    
    # Проходимся по каждому
    for movie in movie_list:

        # дата
        movie_date = movie["release_date"]  
        
        # год
        movie_year = int(movie_date.split("-")[0])  

        # месяц
        movie_month = int(movie_date.split("-")[1])  

        # рейтинг
        movie_rating = movie["rating"]  
        
        # Проверка на условия
        if (movie_year > start_year or (movie_year == start_year and movie_month >= start_month)) and \
           (movie_year < end_year or (movie_year == end_year and movie_month <= end_month)):

            # Проверка рейтинга
            if movie_rating >= min_rating:

                # Прошел все условия - добавляем
                filtered_movies.append(movie)  
    
    return filtered_movies

# Функция для вывода фильмов
def show_movies(movie_list):
    print("Вот фильмы:")

    for movie in movie_list:
        print(f"Название: {movie['title']}, Рейтинг: {movie['rating']}, Дата: {movie['release_date']}")

    # Если ничего нет
    if len(movie_list) == 0:  
        print("Ничего нет!")

# Главная функция
def main():
    # Input от пользователя
    start_date = input("Начало (мм.гггг, например 01.2020): ")
    end_date = input("Конец (мм.гггг, например 12.2022): ")
    min_rating = float(input("Введи минимальный рейтинг: "))
    
    # Берём фильмы из API
    print("Беру фильмы...")
    all_movies = get_movies_from_api(start_date, end_date)
    
    # Фильтруем
    print("Ищу подходящие...")
    good_movies = filter_movies(all_movies, start_date, end_date, min_rating)
    
    # Выводим
    show_movies(good_movies)
    print("Всё готово!")

if __name__ == "__main__":
    main()  