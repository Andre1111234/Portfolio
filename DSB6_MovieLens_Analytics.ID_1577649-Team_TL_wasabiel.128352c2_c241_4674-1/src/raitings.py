import csv
from collections import defaultdict


class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path_to_the_file):
        self.file_path = path_to_the_file
        self.data = []

    def read_data(self):
        """
        Reads ratings.csv (first 1000 rows)
        """
        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 1000:
                    break

                self.data.append({
                    "userId": int(row["userId"]),
                    "movieId": int(row["movieId"]),
                    "rating": float(row["rating"]),
                    "timestamp": int(row["timestamp"])
                })

    # --------------------------------------------------
    # Base analytics (Ratings only)
    # --------------------------------------------------

    def dist_by_rating(self):
        """
        Distribution of ratings.
        {rating: count}
        """
        dist = defaultdict(int)
        for r in self.data:
            dist[r["rating"]] += 1

        return dict(sorted(dist.items()))

    def dist_by_user(self):
        """
        Distribution by users.
        {userId: number of ratings}
        """
        dist = defaultdict(int)
        for r in self.data:
            dist[r["userId"]] += 1

        return dict(sorted(dist.items(), key=lambda x: x[1], reverse=True))

    def average_by_movie(self):
        """
        Average rating for each movie.
        {movieId: average rating}
        """
        sums = defaultdict(float)
        counts = defaultdict(int)

        for r in self.data:
            mid = r["movieId"]
            sums[mid] += r["rating"]
            counts[mid] += 1

        return {
            mid: sums[mid] / counts[mid]
            for mid in sums
        }

    # --------------------------------------------------
    # Ratings + Movies (join by movieId)
    # --------------------------------------------------

    def top_movies(self, movies, n):
        """
        Top-n movies by average rating.
        {movie title: average rating}
        """
        if not isinstance(n, int) or n <= 0:
            return {}

        averages = self.average_by_movie()

        sorted_movies = sorted(
            averages.items(),
            key=lambda x: x[1],
            reverse=True
        )

        result = {}
        for movie_id, avg in sorted_movies[:n]:
            title = movies.get_title(movie_id)
            if title:
                result[title] = round(avg, 2)

        return result

    def most_rated_movies(self, movies, n):
        """
        Top-n movies by number of ratings.
        {movie title: number of ratings}
        """
        if not isinstance(n, int) or n <= 0:
            return {}

        counts = defaultdict(int)
        for r in self.data:
            counts[r["movieId"]] += 1

        sorted_movies = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        result = {}
        for movie_id, count in sorted_movies[:n]:
            title = movies.get_title(movie_id)
            if title:
                result[title] = count

        return result
    
if __name__ == "__main__":
    from movies import Movies   # или из этого же файла, если объединено

    movies = Movies("movies.csv")
    movies.read_data()

    ratings = Ratings("ratings.csv")
    ratings.read_data()

    print(ratings.top_movies(movies, 10))
    print(ratings.most_rated_movies(movies, 10))