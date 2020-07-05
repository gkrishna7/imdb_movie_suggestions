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
    params = {"tconst":movie_id,"id":[]}
    for i in cast_list_id:
        params["id"].append(i)
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

if __name__ == '__main__':
    movie_name = input("Enter the movie name : ")
    movie_id = get_movie_id(movie_name)
    print("{} is the movie id.".format(movie_id))
    list_cast = get_cast_list(movie_id)
    print("Cast : {}".format(', '.join(list_cast)))