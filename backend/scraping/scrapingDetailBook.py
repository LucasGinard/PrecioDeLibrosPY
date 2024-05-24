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
        section = soup.select_one('section.top-section.divider-border-top.single-product.px-2')

        if section:
            title = section.select_one('h1.product_title.entry-title').text.strip()

            author_tag = soup.find('div', class_='product-brand')
            author = author_tag.find('a').text.strip()

            image = soup.find('img',class_='w-100')['src']

            price_element = soup.find('div', class_='price')
            price = price_element.text.strip().replace("₲","Gs. ")

            description = soup.find('p', class_='product-description-text text-justify').get_text(separator='\n',strip=True)

            posted_in = soup.find('span', class_='posted_in')
            categories = posted_in.find_all('a')
            category_names = [category.text for category in categories]

            isbn_tag = soup.find('span', class_='sku')
            isbn = isbn_tag.text.strip()

            return BookDetailData(
                title=title,
                author=author,
                image_url=HttpUrl(url=f"https://ellector.com.py{image}"),
                price=price,
                description=description,
                category=category_names,
                isbn=isbn
            )
        
        return None
    except:
        return None