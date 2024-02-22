from pydantic import HttpUrl

import requests

from model.LibraryEnum import LibraryInfo

from model.BookData import BookData

from bs4 import BeautifulSoup

from typing import List

def scrape_book(search_query: str) -> List[BookData]:
    return scrape_lpt(search_query) + scrape_el_lector(search_query) + scrape_mundo_libros_py(search_query)


def scrape_lpt(search_query: str) -> List[BookData]:
    try:
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

            if title == "ELENA DE AVALOR" and search_query != "ELENA DE AVALOR":
                return book_list
            
            book = BookData(title=title,
                            author=author, 
                            details_url=details_url, 
                            image_url=image_url, 
                            price=price,
                            library= LibraryInfo(name="Libros para todos",
                                                    website_url="https://lpt.com.py",
                                                    icon_url="https://lpt.com.py/images/logo/logo-simple-or.png"
                                                    )
                            )
            book_list.append(book)

        return book_list
    except:
        return []

def scrape_el_lector(search_query: str) -> List[BookData]:
    try:
        url = f"https://ellector.com.py/productos/buscar.html?buscando={search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        book_list = []

        books_container = soup.find('div', class_='row evende-products-overflow no-border-last-line')

        if books_container:
            for book_div in books_container.find_all('div', class_='card'):
                title = book_div.select_one('.card-title a').text.strip()
                author = book_div.select_one('.product-author a').text.strip()
                price = book_div.select_one('.product-price .price-amount').text.strip().replace('₲', 'Gs.')
                image_relative_url = book_div.select_one('.card-img-top')['src']
                image_url = f"https://ellector.com.py{image_relative_url}"
                details_relative_url = book_div.select_one('.card-title a')['href']
                details_url = f"https://ellector.com.py{details_relative_url}"

                book = BookData(title=title, author=author, 
                                image_url=HttpUrl(url=image_url), 
                                price=price, 
                                details_url=HttpUrl(url=details_url),
                                library= LibraryInfo(name="El Lector", 
                                                     website_url="https://ellector.com.py", 
                                                     icon_url="https://ellector.com.py/assets/img/logo_ellector_v2.svg", 
                                                     library_path="lector")
                                                     )
                book_list.append(book)

        return book_list
    except Exception as e:
        print(f"Error: {e}")
        return []

def scrape_mundo_libros_py(search_query: str) -> List[BookData]:
    try:
        url = f"https://www.mundolibrospy.com/busqueda?controller=search&s={search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        book_list = []
        for product_item in soup.select('.product_list_item'):
            
            title = product_item.select_one('h1.s_title_block a')['title']
            author_tag = product_item.select_one('.pro_extra_info_brand')
            author = author_tag.select_one('meta[itemprop="name"]')['content'] if author_tag else ''
            image_url = product_item.select_one('.front-image')['data-src']

            price_text = product_item.select_one('.price').text.strip().replace('₲', '')
            price_digits = ''.join(char for char in price_text if char.isdigit() or char == '.')
            price = f"Gs. {price_digits}"

            details_url = product_item.select_one('h1.s_title_block a')['href']

            book = BookData(title=title, 
                            author=author, 
                            image_url=image_url, 
                            price=price, 
                            details_url=details_url,
                            library= LibraryInfo(name="Mundo Libros", 
                                                 website_url="https://www.mundolibrospy.com", 
                                                 icon_url="http://www.mundolibrospy.com/img/cms/Mundo%20Libros.png", 
                                                 library_path="mundo")
                            )
            book_list.append(book)

        return book_list
    except:
        return []