from typing import Optional
from pydantic import HttpUrl
import requests

from bs4 import BeautifulSoup

from model.BookDetailData import BookDetailData

def scrape_detail_book_lpt(detailLink: str) -> Optional[BookDetailData]:
    try:
        response = requests.get(detailLink)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select_one('h2').text.strip()

        image_div = soup.find('div', class_='w-56 xl:w-64 h-76 sm:h-82 xl:h-86 my-6 sm:my-12 xl:my-24 bg-center bg-no-repeat bg-cover')

        if image_div:
            style_attribute = image_div.get('style', '')

            start_index = style_attribute.find('background:url(')
            end_index = style_attribute.find(')')

            if start_index != -1 and end_index != -1:
                image_url = style_attribute[start_index + len('background:url('):end_index].strip()
                

        price_div = soup.find('div', class_='border-b border-grey-dark mb-8')
        price_span = price_div.find('span', class_='font-mtregular text-secondary text-2xl')
        price = price_span.text.strip() if price_span else 'Precio no disponible'

        info_divs = soup.find_all('div', class_='flex pb-2')
        for div in info_divs:
            paragraph = div.find('p', class_='font-mtregular text-secondary')
            
            if paragraph:
                text = paragraph.text.strip()

                if 'Autor:' in text:
                    author = div.find('p', class_='font-mtbold text-v-greenpl-3').text.strip()
                elif 'Código:' in text:
                    isbn = div.find('p', class_='font-mtbold text-v-greenpl-3').text.strip()
                elif 'Categoría:' in text:
                    category = div.find('p', class_='font-mtbold text-v-greenpl-3').text.strip()
                
        return BookDetailData(
            title=title,
            author=author,
            image_url= image_url,
            price=price,
            description="",
            category=[category],
            isbn=isbn
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
            category=["categories"],
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

        price_text = soup.select_one('.price').text.strip().replace('.₲','Gs.')
        price_digits = ''.join(char for char in price_text if char.isdigit() or char == '.')
        price = f"Gs. {price_digits}"

        description = soup.select_one('.product-description').text.strip()

        tags_container = soup.find('div', class_='product-info-tags')
        tags_links = tags_container.find_all('a')
        categories = [tag.get_text(strip=True) for tag in tags_links]

        isbn = ""

        reference_div = soup.find('div', class_='product-reference pro_extra_info flex_container')
        if reference_div:
            reference_label = reference_div.find('span', class_='pro_extra_info_label')

            if reference_label and 'Referencia' in reference_label.text:
                isbn = reference_div.find('div', class_='pro_extra_info_content').text.strip()

        return BookDetailData(
            title=title,
            author=author,
            image_url= imageURL,
            price=price,
            description=description,
            category=categories,
            isbn=isbn
        )
    except:
        return None