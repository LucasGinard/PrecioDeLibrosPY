import requests

from bs4 import BeautifulSoup

from model.BookDetailData import BookDetailData

def scrape_detail_book_lpt(detailLink: str) -> BookDetailData:
    
    return BookDetailData()

def scrape_detail_book_el_lector(detailLink: str) -> BookDetailData:
    response = requests.get(detailLink)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Obtener el título del libro
    title = soup.select_one('.el-book-title-author h2').text.strip()

    # Obtener el autor del libro
    author = soup.select_one('.el-book-title-author h5 a').text.strip()

    # Obtener la URL de la imagen del libro
    image_url = soup.select_one('#productSlider a img')['src']

    # Obtener el precio del libro
    price = soup.select_one('.el-pd-price span.precio-actual').text.strip()

    # Obtener la descripción del libro
    description = soup.select_one('.el-producto-descripcion p').text.strip()


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