import requests

API_url = "https://imdb8.p.rapidapi.com/title"

headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': "891adb0e26msh5ade434062a5e97p19405djsn52e0bda7182a"
    }


def get_movie_id(movie_name = None):
    url = '{}/find'.format(API_url)
    params = {'q' : movie_name}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        return "Error in connection. Status code return is wrong."

    response = response.json()
    if not response:
        return None

    movie_id = response["results"][0]["id"][7:-1]
    return movie_id

def get_cast_list(movie_id):
    cast_list_id = get_cast_id(movie_id)
    url = '{}/get-charname-list'.format(API_url)
    params = {"tconst":movie_id,"id":cast_list_id}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        return "Connection error as status code is not 200."
    response = response.json()
    cast_list = []
    for i in cast_list_id:
        cast_list.append(response[i]["name"]["name"])
    return cast_list
    

def get_cast_id(movie_id):
    url = '{}/get-top-cast'.format(API_url)
    params = {"tconst":movie_id}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        return "Error in connection. Status code returned is wrong."
    response = response.json()
    cast_list_id = []
    for i in range (5):
        cast_list_id.append(response[i][6:-1])
    return cast_list_id

def get_director(movie_id):
    url = '{}/get-top-crew'.format(API_url)
    params = {"tconst" : movie_id}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        return "Status code not 200 error."
    response = response.json()
    if not response:
        return None
    return response["directors"][0]["name"]

def get_plot_year(movie_id):
    url = '{}/get-plots'.format(API_url)
    params = {"tconst" : movie_id}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        return "Status code not 200 error."
    response = response.json()
    if not response:
        return None
    return response["plots"][0]["text"],response["base"]["year"]

def get_ratings_genre(movie_id):
    url = '{}/get-overview-details'.format(API_url)
    params = {"tconst" : movie_id}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        print("Status code not 200 error.")
        return None
    response = response.json()
    if not response:
        return None
    ratings = response["ratings"]["rating"]
    genre_list = response["genres"]
    return ratings, genre_list

def similar_movies_id(movie_id):
    url = "{}/get-more-like-this".format(API_url)
    params = {"tconst":movie_id}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        print("Status code not 200 error")
        return None
    response = response.json()
    if not response:
        return None
    similar_title_ids = [id[7:-1] for id in response[0:5]]
    return similar_title_ids

def similar_movies(movie_id):
    url = "{}/get-meta-data".format(API_url)
    id_list = similar_movies_id(movie_id)
    params = {"ids": id_list}
    response = requests.request("GET",url,headers=headers,params=params)
    if response.status_code != 200:
        print("Status code not 200 error")
        return None
    response = response.json()
    if not response:
        return None
    similar_movie_names = []
    for i in id_list:
        similar_movie_names.append(response[i]["title"]["title"])
    return ', '.join(similar_movie_names)
    
    


if __name__ == '__main__':
    movie_name = input("Enter the movie name : ")
    movie_id = get_movie_id(movie_name)
    list_cast = get_cast_list(movie_id)
    print("Cast : {}".format(', '.join(list_cast)))
    director_name = get_director(movie_id)
    print("Directed by : {}".format(director_name))
    plot, year_of_release = get_plot_year(movie_id)
    print("Release date : {}\nPlot : {}".format(year_of_release, plot))
    rating, genres = get_ratings_genre(movie_id)
    print("Rating : {}/10\nGenres : {}".format(rating,', '.join(genres)))
    print("Movies similar to {} : {}".format(movie_name,similar_movies(movie_id)))