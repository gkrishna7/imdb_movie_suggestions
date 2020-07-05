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
    

if __name__ == '__main__':
    movie_name = input("Enter the movie name : ")
    movie_id = get_movie_id(movie_name)
    print("{} is the movie id.".format(movie_id))