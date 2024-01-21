import requests

from bs4 import BeautifulSoup

from model.BookDetailData import BookDetailData

def scrape_detail_book_lpt(detailLink: str) -> BookDetailData:
    
    return BookDetailData()

def scrape_detail_book_el_lector(detailLink: str) -> BookDetailData:
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


def scrape_detail_book_mundo_libros_py(detailLink: str) -> BookDetailData:
    

    return detailLink