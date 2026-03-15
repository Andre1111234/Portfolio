from movielens_analysis import Ratings, Tags, Links, Tests

def main():
    ratings = Ratings("ratings.csv", "movies.csv")
    movies = ratings.movies
    tags = Tags("tags.csv")
    links = Links("links.csv")

    tests = Tests(
        movies=movies,
        ratings=ratings,
        tags=tags,
        links=links
    )

    print(tests.run_all())

if __name__ == "__main__":
    main()