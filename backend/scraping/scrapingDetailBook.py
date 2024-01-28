from typing import Optional
from pydantic import HttpUrl
import requests

from bs4 import BeautifulSoup

from model.BookDetailData import BookDetailData

def scrape_detail_book_lpt(detailLink: str) -> Optional[BookDetailData]:
    try:
        return BookDetailData(
            title="asd",
            author="catasdegories",
            image_url= HttpUrl(url="https://example.com"),
            price="categorsadies",
            description="catedasgories",
            category="categdasories",
            isbn="isdasbn"
        )
    except:
        return None

def scrape_detail_book_el_lector(detailLink: str) ->  Optional[BookDetailData]:
    try:
        response = requests.get(detailLink)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select_one('.el-book-title-author h2').text.strip()

        author = soup.select_one('.el-book-title-author h5 a').text.strip()

        image_url = soup.select_one('#productSlider a img')['src']

        price = soup.select_one('.el-pd-price span.precio-actual').text.strip()

        description_element = soup.select_one('.col-12.el-producto-descripcion')
        paragraphs = description_element.find_all('p') if description_element else []
        
        description = '\n'.join(paragraph.text.strip() for paragraph in paragraphs)

        return BookDetailData(
            title=title,
            author=author,
            image_url=image_url,
            price=price,
            description=description,
            category="categories",
            isbn="isbn"
        )
    except:
        return None

def scrape_detail_book_mundo_libros_py(detailLink: str) -> Optional[BookDetailData]:
    try:
        response = requests.get(detailLink)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select_one('.product_name').text.strip()

        author = soup.select_one('.pro_extra_info_brand').text.strip()

        a_tag = soup.find('a', class_='replace-2x')
        imageURL = a_tag.get('href', None)

        price_text = soup.select_one('.price').text.strip().replace('₲','Gs.')
        price_digits = ''.join(char for char in price_text if char.isdigit() or char == '.')
        price = f"Gs. {price_digits}"

        description = soup.select_one('.product-description').text.strip()

        isbn = soup.select_one('.pro_extra_info_content').text.strip()

        return BookDetailData(
            title=title,
            author=author,
            image_url= imageURL,
            price=price,
            description=description,
            category="categdasories",
            isbn=isbn
        )
    except:
        return None