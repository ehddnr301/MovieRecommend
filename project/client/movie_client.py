import os
import requests
import random
import time
import logging
import pandas as pd

SOURCE_MOVIE_CSV_URL = (
    "https://media.githubusercontent.com/media/ehddnr301/MovieRecommend-Csv/master/"
)
SOURCE_MOVIE_CSV_URL = os.environ.get("SOURCE_MOVIE_CSV_URL", SOURCE_MOVIE_CSV_URL)


class ClientSender:
    def __init__(self, base_csv_file: str = "ratings.csv", version: str = "v1"):
        self.base_csv_file = base_csv_file
        self.last_movie_url = "http://fastapi-service:8080/movies/last"
        self.recommend_url = f"http://fastapi-service:8080/recommend/{version}"
        self.feedback_url = f"http://fastapi-service:8080/feedback"
        self.rating_url = f"http://fastapi-service:8080/ratings"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self._rating_dataframe: pd.DataFrame = None
        self._tag_dataframe = None

    @property
    def rating_dataframe(self):
        if self._rating_dataframe is None:
            self._rating_dataframe = pd.read_csv(self.base_csv_file)
        return self._rating_dataframe

    def download_csv_from_github(self, csv_name=None):
        csv_name = csv_name or self.base_csv_file
        response = requests.get(SOURCE_MOVIE_CSV_URL + csv_name)
        with open(csv_name, "wb") as f:
            f.write(response.content)

    def find_user_list_from_ratings(self, movie_id):
        user_list = self.rating_dataframe[self.rating_dataframe["movieId"] == movie_id][
            "userId"
        ].tolist()
        print(user_list)
        return user_list

    def _find_rating_from_ratings(self, user_id, movie_id):
        rating = self.rating_dataframe[
            (self.rating_dataframe["userId"] == user_id)
            & (self.rating_dataframe["movieId"] == movie_id)
        ]["rating"].tolist()[0]
        return rating

    def get_last_movie_id(self):
        response = requests.get(self.last_movie_url, headers=self.headers)
        return response.json()

    def _get_movie_recommend(self, user_id):
        url = self.recommend_url + f"?user_id={user_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logging.error(f"Error: {response.status_code}")

        return response.json()

    def _create_feedback_request(self, user_id, recommended_movie_list, movie_id):
        data = {
            "user_id": user_id,
            "recommended_movie_id_list": recommended_movie_list,
            "selected_movie_id": movie_id,
        }
        response = requests.post(self.feedback_url, headers=self.headers, json=data)
        if response.status_code != 201:
            logging.error(f"Error: {response.status_code}")

    def _create_rating_request(self, user_id, movie_id, rating):
        data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": rating,
        }
        response = requests.post(self.rating_url, headers=self.headers, json=data)
        if response.status_code != 201:
            logging.error(f"Error: {response.status_code}")

    def send_requests_within_time_limit(self, client_wait_time, user_list, movie_id):
        max_interval = max(client_wait_time // (len(user_list) if len(user_list) != 0 else 1), 2)
        for user_id in user_list:
            time.sleep(random.randint(1, max_interval))
            recommended_movie_list = self._get_movie_recommend(user_id)

            # feedback with user_id and recommended_movie_list and movie_id
            self._create_feedback_request(user_id, recommended_movie_list, movie_id)

            rating = self._find_rating_from_ratings(user_id, movie_id)
            print(rating)
            self._create_rating_request(user_id, movie_id, rating)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    CLIENT_WAIT_TIME = int(os.environ.get("CLIENT_WAIT_TIME", 30))
    VERSION = os.environ.get("VERSION", "v1")

    client_sender = ClientSender()
    client_sender.download_csv_from_github()

    previous_movie_id = None
    while True:
        movie_id = client_sender.get_last_movie_id()

        if movie_id == previous_movie_id:
            time.sleep(CLIENT_WAIT_TIME)
            continue

        users = client_sender.find_user_list_from_ratings(movie_id)
        client_sender.send_requests_within_time_limit(CLIENT_WAIT_TIME, users, movie_id)
        previous_movie_id = movie_id
