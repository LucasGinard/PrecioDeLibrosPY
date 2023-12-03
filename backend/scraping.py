import requests
from model.BookData import BookData, BookLibraryInfo
from bs4 import BeautifulSoup

from typing import List

def scrape_books(search_query: str) -> List[BookData]:
    scraped_data = scrape_lpt(search_query)
    return [scraped_data]


def scrape_lpt(search_query: str) -> List[BookData]:
    url = f"https://lpt.com.py/catalogo?q={search_query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    book_list = []
    for book_div in soup.select('div.card-book'):
        title = book_div.select_one('a.font-futurabold').text.strip()
        author = book_div.select_one('p:contains("Autor:")').find_next('span').text.strip()
        details_url = book_div.select_one('a.font-futurabold')['href']
        image_url = book_div.select_one('img')['src']
        price = book_div.select_one('p.text-complementary-brown').text.strip()

        book = BookData(title=title,
                        author=author, 
                        details_url=details_url, 
                        image_url=image_url, 
                        price=price,
                        library= BookLibraryInfo(name="Libros para todos",website_url="https://lpt.com.py")
                        )
        book_list.append(book)

    return book_list 