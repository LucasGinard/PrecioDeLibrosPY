import requests
from model.BookData import BookData, BookLibraryInfo
from bs4 import BeautifulSoup

from typing import List

def scrape_books(search_query: str) -> List[BookData]:
    scraped_data_lpt = scrape_lpt(search_query)
    scraped_data_el_lector = scrape_el_lector(search_query)
    return scraped_data_lpt + scraped_data_el_lector


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

def scrape_el_lector(search_query: str) -> List[BookData]:
    url = f"https://ellector.com.py/shop?filters%5Bname%5D={search_query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    book_list = []
    for book_div in soup.select('.el-product-grid-item'):
        if book_div.select_one('.badge-light') and "Sin Stock" in book_div.select_one('.badge-light').text:
            continue
        title = book_div.select_one('.book-title').text.strip()
        author = book_div.select_one('.book-author a').text.strip()
        image_url = book_div.select_one('.book-image-bg')['style'].split('url(')[1].split(')')[0].strip("'")
        price = book_div.select_one('.book-price').text.strip()
        details_url = book_div.select_one('.book-image-bg')['href']

        book = BookData(title=title, author=author, image_url=image_url, price=price, details_url=details_url,library= BookLibraryInfo(name="El Lector",website_url="https://ellector.com.py"))
        book_list.append(book)

    return book_list