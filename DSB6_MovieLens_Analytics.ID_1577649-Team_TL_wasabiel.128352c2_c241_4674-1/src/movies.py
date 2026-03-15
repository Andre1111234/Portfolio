import csv
from collections import Counter


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        self.file_path = path_to_the_file
        self.movie_data = []
        self.movies_by_id = {}

    def read_data(self):
        """
        Reads movies.csv (first 1000 rows)
        """
        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 1000:
                    break

                movie_id = int(row["movieId"])
                self.movie_data.append(row)
                self.movies_by_id[movie_id] = {
                    "title": row["title"],
                    "genres": row["genres"]
                }

    # --------------------------------------------------
    # Analytics
    # --------------------------------------------------

    def dist_by_release(self):
        """
        Distribution of movies by release year.
        {year: count}
        """
        years = []

        for movie in self.movie_data:
            title = movie["title"]
            if "(" in title and title.endswith(")"):
                year = title[-5:-1]
                if year.isdigit():
                    years.append(year)

        counter = Counter(years)
        return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

    def dist_by_genres(self):
        """
        Distribution of movies by genres.
        {genre: count}
        """
        genres = []

        for movie in self.movie_data:
            genres.extend(movie["genres"].split("|"))

        counter = Counter(genres)
        return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

    def most_genres(self, n):
        """
        Top-n movies with the largest number of genres.
        {movie title: number of genres}
        """
        if not isinstance(n, int) or n <= 0:
            return {}

        movies = []

        for movie in self.movie_data:
            title = movie["title"]
            count_genres = len(movie["genres"].split("|"))
            movies.append((title, count_genres))

        return dict(sorted(movies, key=lambda x: x[1], reverse=True)[:n])

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def get_title(self, movie_id):
        """
        Returns movie title by movieId
        """
        movie = self.movies_by_id.get(movie_id)
        return movie["title"] if movie else None