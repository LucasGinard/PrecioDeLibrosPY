import requests

from model.BookData import BookData, BookLibraryInfo

from bs4 import BeautifulSoup

from typing import List

def scrape_book(search_query: str) -> List[BookData]:
    return scrape_lpt(search_query) + scrape_el_lector(search_query) + scrape_mundo_libros_py(search_query)


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

        if title == "ELENA DE AVALOR" and search_query != "ELENA DE AVALOR":
            return book_list
        
        book = BookData(title=title,
                        author=author, 
                        details_url=details_url, 
                        image_url=image_url, 
                        price=price,
                        library= BookLibraryInfo(name="Libros para todos",
                                                 website_url="https://lpt.com.py",
                                                 icon_url="https://lpt.com.py/images/logo/logo-simple-or.png"
                                                 )
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
        author_element = book_div.select_one('.book-author a')
        author = author_element.text.strip() if author_element else ""
        image_url = book_div.select_one('.book-image-bg')['style'].split('url(')[1].split(')')[0].strip("'")
        price = book_div.select_one('.book-price').text.strip().replace('₲','Gs.')
        details_url = book_div.select_one('.book-image-bg')['href']

        book = BookData(title=title, author=author, 
                        image_url=image_url, 
                        price=price, 
                        details_url=details_url,
                        library= BookLibraryInfo(name="El Lector",
                                                 website_url="https://ellector.com.py",
                                                 icon_url="https://ellector.com.py/assets/images/logo.png"
                                                 )
                        )
        book_list.append(book)

    return book_list


def scrape_mundo_libros_py(search_query: str) -> List[BookData]:
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
                        library= BookLibraryInfo(name="Mundo Libros",
                                                 website_url="https://www.mundolibrospy.com",
                                                 icon_url= "http://www.mundolibrospy.com/img/cms/Mundo%20Libros.png"
                                                 )
                        )
        book_list.append(book)

    return book_list