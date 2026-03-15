import csv
import requests
from bs4 import BeautifulSoup

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
    
if __name__ == "__main__":
    links = Links("links.csv")

    # Проверяем, что файл прочитан
    print(len(links.data))

    # Проверяем САМЫЙ минимальный IMDb-вызов
    print(links.get_imdb(
        [1],
        ["title-boxoffice-budget"]
    ))