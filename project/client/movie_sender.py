import os
import requests
import random
import time
import logging

import pandas as pd


class MovieSender:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.url = os.environ.get("REQUEST_URL", "http://localhost:8080/movies/")
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self.download_csv_from_github()  # Download the csv from GitHub
        self.movies = self.load_movies_from_csv()
        random.shuffle(self.movies)
        self.current_index = 0

    def download_csv_from_github(self):
        github_url = os.environ.get(
            "GITHUB_URL",
            "https://media.githubusercontent.com/media/ehddnr301/MovieRecommend-Csv/master/movies.csv",
        )
        response = requests.get(github_url)
        with open(self.csv_file, "wb") as f:
            f.write(response.content)

    def load_movies_from_csv(self):
        df = pd.read_csv(self.csv_file)
        return df.values.tolist()

    def send_movie_data(self, movie_id, title, genres):
        data = {"genres": genres.split("|"), "movie_id": movie_id, "title": title}
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            if response.status_code == 201:
                logging.info(f"Successfully sent data for movie: {title}")
            else:
                logging.error(
                    f"Failed to send data. Status code: {response.status_code}. Response text: {response.text}"
                )
        except requests.RequestException as e:
            logging.error(f"Error sending data: {e}")

    def pick_random_movie(self):
        movie = self.movies[self.current_index]
        self.current_index += 1
        if self.current_index >= len(self.movies):
            self.current_index = 0
        return movie


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    CSV_FILE = "./movies.csv"
    MOVIE_SEND_INTERVAL = int(os.environ.get("MOVIE_SEND_INTERVAL", 60))
    movie_sender = MovieSender(CSV_FILE)

    while True:
        movie = movie_sender.pick_random_movie()
        movie_sender.send_movie_data(movie[0], movie[1], movie[2])
        time.sleep(MOVIE_SEND_INTERVAL)
