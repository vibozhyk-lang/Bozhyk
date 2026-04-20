import requests
from bs4 import BeautifulSoup
import string
from pathlib import Path
from requests.exceptions import RequestException


class NatureScraper:
    def __init__(self, page_limit, article_type):
        self.page_limit = page_limit
        self.article_type = article_type
        self.base_url = "https://www.nature.com/nature/articles"
        self.session = requests.Session()
        # Установка заголовков для имитации браузера
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5"
        })

    def _sanitize_filename(self, title):
        """Превращает заголовок статьи в валидное имя файла."""
        # Убираем пунктуацию и заменяем пробелы на подчеркивания
        translation_table = str.maketrans('', '', string.punctuation.replace('-', '').replace('_', ''))
        clean_title = title.translate(translation_table).replace(' ', '_')
        return f"{clean_title[:100]}.txt"

    def _send_request(self, url, params=None):
        """Обертка для выполнения сетевых запросов с обработкой ошибок."""
        try:
            response = self.session.get(url, params=params, timeout=20)
            response.raise_for_status()
            return response
        except RequestException as exc:
            print(f"[!] Ошибка соединения с {url}: {exc}")
            return None

    def _parse_article_content(self, url):
        """Извлекает текст статьи из найденных HTML-контейнеров."""
        res = self._send_request(url)
        if not res:
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        # Поиск основного блока текста по известным паттернам Nature
        content_selectors = [
            "article.c-article-body",
            "div.main-content",
            "div[itemprop='articleBody']"
        ]

        for selector in content_selectors:
            box = soup.select_one(selector)
            if box:
                paragraphs = box.find_all("p")
                full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
                if full_text.strip():
                    return full_text

        # Если основной блок не найден, пробуем забрать анонс (teaser)
        teaser = soup.find("p", class_="article__teaser")
        return teaser.get_text(strip=True) if teaser else ""

    def _process_single_page(self, page_num):
        """Обрабатывает одну страницу списка статей."""
        print(f"[*] Сканирование страницы {page_num}...")

        payload = {
            "searchType": "journalSearch",
            "sort": "PubDate",
            "year": "2022",  # Можно заменить на актуальный год
            "page": page_num
        }

        resp = self._send_request(self.base_url, params=payload)
        if not resp:
            return

        soup = BeautifulSoup(resp.text, "html.parser")

        # Создаем папку для текущей страницы
        folder = Path(f"Page_{page_num}")
        folder.mkdir(exist_ok=True)

        articles = soup.find_all("article")
        if not articles:
            print(f"[-] На странице {page_num} контент отсутствует.")
            return

        for art in articles:
            # Фильтрация по заданному типу (напр. Research Highlight)
            type_tag = art.find("span", {"data-test": "article.type"})
            if not type_tag or type_tag.text.strip() != self.article_type:
                continue

            anchor = art.find("a", {"data-track-action": "view article"})
            if not anchor:
                continue

            title = anchor.text.strip()
            link = "https://www.nature.com" + anchor.get("href")

            print(f"    + Обработка: {title[:60]}...")

            text_data = self._parse_article_content(link)
            if text_data:
                fname = self._sanitize_filename(title)
                file_path = folder / fname
                try:
                    file_path.write_text(text_data, encoding="utf-8")
                except IOError as e:
                    print(f"[!] Не удалось записать файл {fname}: {e}")

    def run(self):
        """Запуск цикла обхода всех страниц."""
        for n in range(1, self.page_limit + 1):
            self._process_single_page(n)
        print("\n[+] Работа завершена. Проверьте созданные директории.")


def main():
    while True:
        try:
            pages = int(input("Сколько страниц нужно просмотреть?\n> "))
            if pages > 0:
                break
        except ValueError:
            pass
        print("Введите корректное число.")

    category = input("Какую категорию ищем? (напр., Research Highlight):\n> ").strip()

    bot = NatureScraper(pages, category)
    bot.run()


if __name__ == "__main__":
    main()