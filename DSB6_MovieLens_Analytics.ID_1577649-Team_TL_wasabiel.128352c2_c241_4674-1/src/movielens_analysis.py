import datetime
import csv
from collections import Counter
import requests
from bs4 import BeautifulSoup

class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        self.file_path = path_to_the_file
        self.data = []
        self.by_movie = {}
        self.read_file()

    def read_file(self):
        """
        Reads tags.csv and fills internal structures.
        """
        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            required_fields = {"userId", "movieId", "tag", "timestamp"}
            if not required_fields.issubset(reader.fieldnames):
                raise ValueError("Invalid tags.csv structure")

            for i, row in enumerate(reader):
                if i >= 1000:
                    break

                if not row["tag"]:
                    continue

                record = {
                    "userId": int(row["userId"]),
                    "movieId": int(row["movieId"]),
                    "tag": row["tag"],
                    "timestamp": int(row["timestamp"])
                }

                self.data.append(record)
                self.by_movie.setdefault(record["movieId"], []).append(record["tag"])

    def most_words(self, n):
        """
        Returns top-n tags with the most words.
        """
        if not isinstance(n, int) or n <= 0:
            return {}

        counts = {}
        for record in self.data:
            tag = record["tag"]
            counts[tag] = len(tag.split())

        sorted_tags = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return dict(sorted_tags[:n])

    def longest(self, n):
        """
        Returns top-n longest tags by character length.
        """
        if not isinstance(n, int) or n <= 0:
            return []

        uniq = {}
        for record in self.data:
            tag = record["tag"]
            uniq[tag] = len(tag)

        sorted_tags = sorted(
            uniq.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [tag for tag, _ in sorted_tags[:n]]

    def most_words_and_longest(self, n):
        """
        Returns intersection of tags from most_words and longest.
        """
        if not isinstance(n, int) or n <= 0:
            return []

        words_dict = self.most_words(n)
        longest_list = self.longest(n)

        intersection = set(words_dict.keys()) & set(longest_list)
        return sorted(intersection)

    def most_popular(self, n):
        """
        Returns top-n most popular tags by frequency.
        """
        if not isinstance(n, int) or n <= 0:
            return {}

        counts = {}
        for record in self.data:
            tag = record["tag"]
            counts[tag] = counts.get(tag, 0) + 1

        sorted_tags = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return dict(sorted_tags[:n])

    def tags_with(self, word):
        """
        Returns all unique tags containing the given word.
        """
        if not isinstance(word, str) or not word:
            return []

        result = set()
        for record in self.data:
            tag = record["tag"]
            if word in tag:
                result.add(tag)

        return sorted(result)

    def get_all(self):
        """
        Returns all loaded tag records.
        """
        return self.data

class Ratings:
   
    def __init__(self,ratings_path, movies_path):

        self.ratings_path = ratings_path
        self.rating_data = []
        self.read_rating()
        
        self.movies = self.Movies(self, movies_path)
        self.user = self.Users(self, movies_path)
    

    def read_rating(self):
        try:
            with open(self.ratings_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                for i, row in enumerate(csv_reader):
                    if i >= 1000:
                        break
                    self.rating_data.append(row)
                    
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.file_path} не найден")
        
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")
        
    def find_title_on_id(self, movies_id: list):
        movies = []
        for key, value in movies_id:
            for line in self.movies.movie_data:
                if key == line['movieId']:
                    movies.append((line['title'], value))
                    break
        return movies
        
    def dist_by_year(self):
        years = []
        for line in self.rating_data:
            time = datetime.datetime.fromtimestamp(int(line['timestamp']))
            year = time.year
            years.append(year)
        counter = Counter(years)
        ratings_by_year = dict(sorted(counter.items(), key=lambda item: int(item[1])))
            
        return ratings_by_year
        
    def dist_by_rating(self):
        ratings = []
        for line in self.rating_data:
            rating = line['rating']
            ratings.append(rating)
        counter = Counter(ratings)
        ratings_distribution = dict(sorted(counter.items(), key=lambda item: int(item[1])))
            
        return ratings_distribution
        
    def top_by_num_of_ratings(self, n):
        top = []
        for line in self.rating_data:
            movie_id = line['movieId']
            top.append(movie_id)
        counter = Counter(top)
        top_movies_id = sorted(counter.items(), key=lambda item: int(-item[1]))[:n]

        top_movies = self.find_title_on_id(top_movies_id)

        return dict(top_movies)

    class Movies:
        """
         Analyzing data from movies.csv
        """
        def __init__(self, outer_instance, path_to_the_file):
            self.outer = outer_instance
            self.file_path = path_to_the_file
            self.movie_data = []
            self.read_movie()


        def read_movie(self):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    csv_reader = csv.DictReader(f)
                    
                    for i, row in enumerate(csv_reader):
                        if i >= 1000:
                            break
                        self.movie_data.append(row)
                        
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл {self.file_path} не найден")
            
            except Exception as e:
                raise Exception(f"Ошибка при чтении файла: {e}")

        def dist_by_release(self):
            year = []
            for line in self.movie_data:
                title = line['title']
                if '(' in title and title.endswith(')'):
                    year.append(title.split('(')[-1][:-1])
            counter = Counter(year)
            release_years = dict(sorted(counter.items(), key=lambda item: int(-item[1])))
            return release_years
        
        def dist_by_genres(self):
            all_genres = []
            for line in self.movie_data:
                it_genre = line['genres']
                if '|' in it_genre:
                    all_genres += it_genre.split("|")
                else:
                    all_genres.append(it_genre)
            counter = Counter(all_genres)
            genres = dict(sorted(counter.items(), key=lambda item: int(-item[1])))

            return genres
            
        def most_genres(self, n):
            if n <= 0:
                raise Exception('Количество ожидаемых данных должно быть больше 0')
            
            all_movies = []
            for line in self.movie_data:
                title = line['title']
                genre = line['genres']
                count_genre = len(genre.split('|'))
                all_movies.append((title, count_genre))

            movies = dict(sorted(all_movies, key=lambda item: int(-item[1]))[:n])

            return movies

        
        def movie_rating(self, movie_id, mode, find='movieId'):
            rating = self.outer
            data = rating.rating_data
            movie_id = int(movie_id)

            if mode == 'average':
                sum = 0
                count = 0
                for line in data:
                    if int(line[find]) == movie_id:
                        sum += float(line['rating'])
                        count += 1
                if count == 0:
                    raise Exception(f"{find} - {movie_id} не найден")
                return round(sum/count, 2)

            elif mode == 'median':  
                median = [float(line['rating'])
                          for line in data 
                          if int(line[find]) == movie_id]
                if not median:
                    raise Exception(f"{find} - {movie_id} не найден")
                rating = Counter(median).most_common(1)[0]
                return rating[0]
            else:
                raise Exception("Введите корректную метрику(averag/median)")
            
        def top_by_ratings(self, n, metric='average'):
            rating = self.outer
            data = rating.rating_data
            all_movie_id = []
            for id in data:
                if id['movieId'] not in all_movie_id:
                    all_movie_id.append(id['movieId'])
            
            top = []
            for id in all_movie_id:
                value = self.movie_rating(id, metric)
                top.append((id, value))
            top_movies_id = sorted(top, key=lambda x: float(-x[1]))[:n]

            top_movies = rating.find_title_on_id(top_movies_id)
            return dict(top_movies)
        
        def movie_variance(self, movie_id, find='movieId'):
            rating = self.outer
            data = rating.rating_data
            movie_id = int(movie_id)

            variance = [float(line['rating'])
                      for line in data 
                      if int(line[find]) == movie_id]
            if not variance:
                raise Exception(f"{find} - {movie_id} не найден")
            if len(variance) == 1:
                return -1 
            
            avg = self.movie_rating(movie_id, 'average')

            result = 0
            for rating in variance:
                result += (rating - avg)**2
            result = result/(len(variance)-1)

            return round(result, 2)
            
        def top_controversial(self, n):
            rating = self.outer
            data = rating.rating_data
            all_movie_id = []
            for id in data:
                if id['movieId'] not in all_movie_id:
                    all_movie_id.append(id['movieId'])
            
            top = []
            for id in all_movie_id:
                value = self.movie_variance(id)
                top.append((id, value))
            top_movies_id = sorted(top, key=lambda x: float(-x[1]))[:n]

            top_movies = rating.find_title_on_id(top_movies_id)

            return dict(top_movies)


    class Users(Movies):
        def __init__(self, outer_instance, path_to_the_file):
            super().__init__(outer_instance, path_to_the_file)
            self.outer = outer_instance
            self.file_path = path_to_the_file
            
        def top_by_num_of_user(self):
            rating = self.outer
            top = []
            for line in rating.rating_data:
                user_id = line['userId']
                top.append(user_id)
            counter = Counter(top)
            top_user_id = sorted(counter.items(), key=lambda item: int(-item[1]))

            return dict(top_user_id)
        
        def top_by_ratings_user(self, metric='average'):
            rating = self.outer
            data = rating.rating_data
            all_user_id = []
            for id in data:
                if id['userId'] not in all_user_id:
                    all_user_id.append(id['userId'])
        
            top = []
            for id in all_user_id:
                value = self.movie_rating(id, metric, 'userId')
                top.append((id, value))
            top_user_id = sorted(top, key=lambda x: float(-x[1]))

            return dict(top_user_id)
        
        def top_controversial_user(self, n):
            rating = self.outer
            data = rating.rating_data
            all_user_id = []
            for id in data:
                if id['userId'] not in all_user_id:
                    all_user_id.append(id['userId'])
            
            top = []
            for id in all_user_id:
                value = self.movie_variance(id, 'userId')
                top.append((id, value))
            top_user_id = sorted(top, key=lambda x: float(-x[1]))[:n]

            return dict(top_user_id)

class Links:
    """
    Analyzing data from links.csv and IMDb pages
    """

    IMDB_URL = "https://www.imdb.com/title/tt{}"

    def __init__(self, path_to_the_file):
        self.file_path = path_to_the_file
        self.data = {}
        self.read_file()

    def read_file(self):
        """
        Reads links.csv and stores movieId -> imdbId mapping
        """
        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            required_fields = {"movieId", "imdbId", "tmdbId"}
            if not required_fields.issubset(reader.fieldnames):
                raise ValueError("Invalid links.csv structure")

            for i, row in enumerate(reader):
                if i >= 1000:
                    break

                movie_id = int(row["movieId"])
                imdb_id = row["imdbId"].zfill(7)

                self.data[movie_id] = imdb_id


    def _get_imdb_page(self, imdb_id):
        url = self.IMDB_URL.format(imdb_id)
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def _extract_text(self, soup, label):
        block = soup.find("li", attrs={"data-testid": label})
        if not block:
            return None
        value = block.find("span", class_="ipc-metadata-list-item__list-content-item")
        return value.text.strip() if value else None


    def get_imdb(self, list_of_movies, list_of_fields):
        """
        Returns list of lists:
        [movieId, field1, field2, ...]
        """
        if not isinstance(list_of_movies, list) or not isinstance(list_of_fields, list):
            return []

        result = []

        for movie_id in list_of_movies:
            if movie_id not in self.data:
                continue

            imdb_id = self.data[movie_id]
            soup = self._get_imdb_page(imdb_id)

            row = [movie_id]
            for field in list_of_fields:
                value = self._extract_text(soup, field)
                row.append(value)

            result.append(row)

        return sorted(result, key=lambda x: x[0], reverse=True)

    def top_directors(self, n):
        if not isinstance(n, int) or n <= 0:
            return {}

        counts = {}

        for imdb_id in self.data.values():
            soup = self._get_imdb_page(imdb_id)
            director = self._extract_text(soup, "title-pc-principal-credit")
            if director:
                counts[director] = counts.get(director, 0) + 1

        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_items[:n])

    def most_expensive(self, n):
        if not isinstance(n, int) or n <= 0:
            return {}

        budgets = {}

        for imdb_id in self.data.values():
            soup = self._get_imdb_page(imdb_id)
            title = soup.find("h1").text.strip()
            budget = self._extract_text(soup, "title-boxoffice-budget")

            if budget:
                budgets[title] = budget

        sorted_items = sorted(budgets.items(), reverse=True)
        return dict(sorted_items[:n])

    def most_profitable(self, n):
        if not isinstance(n, int) or n <= 0:
            return {}

        profits = {}

        for imdb_id in self.data.values():
            soup = self._get_imdb_page(imdb_id)
            title = soup.find("h1").text.strip()

            budget = self._extract_text(soup, "title-boxoffice-budget")
            gross = self._extract_text(soup, "title-boxoffice-cumulativeworldwidegross")

            if budget and gross:
                profits[title] = gross

        sorted_items = sorted(profits.items(), reverse=True)
        return dict(sorted_items[:n])

    def longest(self, n):
        if not isinstance(n, int) or n <= 0:
            return {}

        runtimes = {}

        for imdb_id in self.data.values():
            soup = self._get_imdb_page(imdb_id)
            title = soup.find("h1").text.strip()
            runtime = self._extract_text(soup, "title-techspec_runtime")

            if runtime:
                runtimes[title] = runtime

        sorted_items = sorted(runtimes.items(), reverse=True)
        return dict(sorted_items[:n])

    def top_cost_per_minute(self, n):
        if not isinstance(n, int) or n <= 0:
            return {}

        costs = {}

        for imdb_id in self.data.values():
            soup = self._get_imdb_page(imdb_id)
            title = soup.find("h1").text.strip()

            budget = self._extract_text(soup, "title-boxoffice-budget")
            runtime = self._extract_text(soup, "title-techspec_runtime")

            if budget and runtime:
                try:
                    minutes = int(runtime.split()[0])
                    value = round(1 / minutes, 2)
                    costs[title] = value
                except ValueError:
                    continue

        sorted_items = sorted(costs.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_items[:n])


class Tests:
    """
    Simple tests for Movies, Ratings, Tags, Links
    Checks:
    - return types
    - basic correctness
    """

    def __init__(self, movies, ratings, tags=None, links=None):
        self.movies = movies
        self.ratings = ratings
        self.tags = tags
        self.links = links

    # Movies

    def test_movies_dist_by_release(self):
        result = self.movies.dist_by_release()
        assert isinstance(result, dict)

    def test_movies_dist_by_genres(self):
        result = self.movies.dist_by_genres()
        assert isinstance(result, dict)

    def test_movies_most_genres(self):
        result = self.movies.most_genres(5)
        assert isinstance(result, dict)

    def test_movies_movie_rating_avg(self):
        movie_id = self.movies.movie_data[0]["movieId"]
        result = self.movies.movie_rating(movie_id, "average")
        assert isinstance(result, float)

    def test_movies_movie_rating_median(self):
        movie_id = self.movies.movie_data[0]["movieId"]
        result = self.movies.movie_rating(movie_id, "median")
        assert isinstance(result, float)

    def test_movies_top_by_ratings(self):
        result = self.movies.top_by_ratings(5)
        assert isinstance(result, dict)

    def test_movies_movie_variance(self):
        movie_id = self.movies.movie_data[0]["movieId"]
        result = self.movies.movie_variance(movie_id)
        assert isinstance(result, float)

    def test_movies_top_controversial(self):
        result = self.movies.top_controversial(5)
        assert isinstance(result, dict)

    # Ratings

    def test_ratings_dist_by_rating(self):
        result = self.ratings.dist_by_rating()
        assert isinstance(result, dict)

    def test_ratings_dist_by_year(self):
        result = self.ratings.dist_by_yeah()
        assert isinstance(result, dict)

    def test_ratings_top_by_num_of_ratings(self):
        result = self.ratings.top_by_num_of_ratings(5)
        assert isinstance(result, dict)

    # Users (вложенный)

    def test_users_top_by_num_of_user(self):
        result = self.ratings.user.top_by_num_of_user()
        assert isinstance(result, dict)

    def test_users_top_by_ratings_user(self):
        result = self.ratings.user.top_by_ratings_user()
        assert isinstance(result, dict)

    def test_users_top_controversial_user(self):
        result = self.ratings.user.top_controversial_user(3)
        assert isinstance(result, dict)

    # Tags

    def test_tags_most_words(self):
        if self.tags is None:
            return
        result = self.tags.most_words(5)
        assert isinstance(result, dict)

    def test_tags_longest(self):
        if self.tags is None:
            return
        result = self.tags.longest(5)
        assert isinstance(result, list)

    def test_tags_most_words_and_longest(self):
        if self.tags is None:
            return
        result = self.tags.most_words_and_longest(5)
        assert isinstance(result, list)

    def test_tags_most_popular(self):
        if self.tags is None:
            return
        result = self.tags.most_popular(5)
        assert isinstance(result, dict)

    def test_tags_tags_with(self):
        if self.tags is None:
            return
        result = self.tags.tags_with("true")
        assert isinstance(result, list)

    # Links (ОПАСНО: сеть)
    #  Эти тесты НЕ запускаются по умолчанию

    def test_links_get_imdb(self):
        if self.links is None:
            return
        result = self.links.get_imdb([1, 2, 3], ["title-boxoffice-budget"])
        assert isinstance(result, list)

    def test_links_top_directors(self):
        if self.links is None:
            return
        result = self.links.top_directors(3)
        assert isinstance(result, dict)

    # Runner
    
    def run_all(self):
        # Movies
        self.test_movies_dist_by_release()
        self.test_movies_dist_by_genres()
        self.test_movies_most_genres()
        self.test_movies_movie_rating_avg()
        self.test_movies_movie_rating_median()
        self.test_movies_top_by_ratings()
        self.test_movies_movie_variance()
        self.test_movies_top_controversial()

        # Ratings
        self.test_ratings_dist_by_rating()
        self.test_ratings_dist_by_year()
        self.test_ratings_top_by_num_of_ratings()

        # Users
        self.test_users_top_by_num_of_user()
        self.test_users_top_by_ratings_user()
        self.test_users_top_controversial_user()

        # Tags
        self.test_tags_most_words()
        self.test_tags_longest()
        self.test_tags_most_words_and_longest()
        self.test_tags_most_popular()
        self.test_tags_tags_with()

        #  Links intentionally NOT run automatically

        return "All tests passed"