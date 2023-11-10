import os
import requests
import random
import time
import logging
import json
import pandas as pd

SOURCE_MOVIE_CSV_URL = (
    "https://media.githubusercontent.com/media/ehddnr301/MovieRecommend-Csv/master/"
)
SOURCE_MOVIE_CSV_URL = os.environ.get("SOURCE_MOVIE_CSV_URL", SOURCE_MOVIE_CSV_URL)


# trigger Airflow Dag
def trigger_airflow_dag(dag_id: str = "train_rec_model"):
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "conf": {},
    }
    url = f"http://airflow-webserver-service:8080/api/v1/dags/{dag_id}/dagRuns"
    response = requests.post(
        url, headers=headers, data=json.dumps(payload), auth=("admin", "admin")
    )
    logging.info(response.status_code, response.text)


# fmt: off
GROUP_B = [1,   2,   3,   4,   5,   6,   7,  10,  15,  16,  17,  18,  19,
        20,  21,  23,  24,  25,  26,  27,  28,  29,  30,  33,  34,  35,
        36,  41,  42,  43,  46,  47,  48,  49,  50,  52,  57,  62,  63,
        64,  66,  67,  68,  72,  73,  74,  75,  76,  78,  79,  80,  81,
        82,  84,  89,  90,  91,  92,  93,  94,  95,  96,  97,  98, 103,
       104, 105, 106, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
       120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
       133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 154, 155,
       156, 166, 167, 168, 169, 170, 171, 172, 174, 175, 176, 177, 178,
       182, 183, 184, 185, 186, 187, 188, 189, 190, 198, 199, 201, 202,
       203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215,
       216, 217, 219, 220, 221, 222, 223, 226, 227, 228, 229, 230, 231,
       232, 233, 234, 235, 236, 237, 245, 246, 249, 250, 251, 252, 253,
       254, 255, 256, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267,
       268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280,
       281, 282, 283, 284, 288, 290, 291, 292, 293, 294, 295, 296, 297,
       298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310,
       311, 312, 313, 314, 315, 316, 317, 318, 322, 323, 324, 325, 326,
       327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 344,
       345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 357, 358, 359,
       360, 361, 362, 365, 366, 367, 368, 372, 373, 374, 375, 376, 377,
       378, 379, 380, 381, 382, 383, 384, 385, 387, 388, 389, 390, 391,
       392, 393, 395, 396, 397, 398, 399, 400, 401, 402, 405, 406, 407,
       408, 409]
# fmt: on


class ClientSender:
    def __init__(self, base_csv_file: str = "ratings.csv"):
        self.base_csv_file = base_csv_file
        self.last_movie_url = "http://fastapi-service:8080/movies/last"
        self.recommend_url_v1 = f"http://fastapi-service:8080/recommend/v1"
        self.recommend_url_v2 = f"http://fastapi-service:8080/recommend/v2"
        self.feedback_url = "http://fastapi-service:8080/feedback"
        self.rating_url = "http://fastapi-service:8080/ratings"
        self.movie_url = "http://fastapi-service:8080/movies/"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self._rating_dataframe: pd.DataFrame = None
        self._movie_dataframe: pd.DataFrame = None
        self._tag_dataframe = None
        self._current_index = 0

    @property
    def rating_dataframe(self):
        if self._rating_dataframe is None:
            self._rating_dataframe = pd.read_csv(self.base_csv_file)
        return self._rating_dataframe

    @property
    def movie_dataframe(self):
        if self._movie_dataframe is None:
            self._movie_dataframe = pd.read_csv("movies.csv")
        return self._movie_dataframe

    def increase_current_index(self):
        self._current_index += 1

    def download_csv_from_github(self, csv_name=None):
        csv_name = csv_name or self.base_csv_file
        response = requests.get(SOURCE_MOVIE_CSV_URL + csv_name)
        with open(csv_name, "wb") as f:
            f.write(response.content)

    def find_user_list_from_ratings(self, movie_id):
        user_list = self.rating_dataframe[self.rating_dataframe["movieId"] == movie_id][
            "userId"
        ].tolist()
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

    def _get_movie_recommend(self, user_id, action_cycle):
        url = (
            self.recommend_url_v2 + f"?user_id={user_id}"
            if user_id in GROUP_B and action_cycle != 0
            else self.recommend_url_v1 + f"?user_id={user_id}"
        )
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logging.error(f"Error: {response.status_code}")

        return response.json()

    def _create_feedback_request(
        self, user_id, recommended_movie_list, movie_id, user_type, action_cycle
    ):
        data = {
            "user_id": user_id,
            "recommended_movie_id_list": recommended_movie_list,
            "selected_movie_id": movie_id,
            "user_type": user_type,
            "action_cycle": action_cycle,
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

    def send_user_reaction(self, client_wait_time, user_list, movie_id):
        max_interval = max(
            client_wait_time // (len(user_list) if len(user_list) != 0 else 1), 1
        )
        action_cycle = (self._current_index // 2000) % 2
        for user_id in user_list:
            time.sleep(0.25)
            user_type = "A" if user_id not in GROUP_B else "B"
            recommended_movie_list = self._get_movie_recommend(user_id, action_cycle)

            self._create_feedback_request(
                user_id, recommended_movie_list, movie_id, user_type, action_cycle
            )

            rating = self._find_rating_from_ratings(user_id, movie_id)
            self._create_rating_request(user_id, movie_id, rating)

    def send_movie_data(self, movie_id, title, genres):
        data = {"genres": genres, "movie_id": movie_id, "title": title}
        try:
            response = requests.post(self.movie_url, headers=self.headers, json=data)
            if response.status_code == 201:
                logging.info(
                    f"Successfully sent data for movie: {title} | self._current_index: {self._current_index}"
                )
            else:
                logging.error(
                    f"Failed to send data. Status code: {response.status_code}. Response text: {response.text}"
                )
        except requests.RequestException as e:
            logging.error(f"Error sending data: {e}")

    def pick_random_movie(self):
        movies = self.movie_dataframe.values.tolist()
        random.shuffle(movies)
        movie = movies[self._current_index]
        if self._current_index % 500 == 0 and self._current_index != 0:
            trigger_airflow_dag("train_rec_model")
        if self._current_index >= len(self.movie_dataframe):
            self._current_index = 0
        self.increase_current_index()
        return movie


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    CLIENT_WAIT_TIME = int(os.environ.get("CLIENT_WAIT_TIME", 0))
    VERSION = os.environ.get("VERSION", "v1")

    client_sender = ClientSender()
    client_sender.download_csv_from_github()
    client_sender.download_csv_from_github("movies.csv")
    # trigger_airflow_dag("init_data")
    time.sleep(10)
    while True:
        movie = client_sender.pick_random_movie()
        client_sender.send_movie_data(movie[0], movie[1], movie[2])
        movie_id = movie[0]
        users = client_sender.find_user_list_from_ratings(movie_id)
        client_sender.send_user_reaction(CLIENT_WAIT_TIME, users, movie_id)
        time.sleep(CLIENT_WAIT_TIME)
