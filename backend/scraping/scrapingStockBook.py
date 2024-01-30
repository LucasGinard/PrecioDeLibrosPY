from typing import Optional
import requests

from bs4 import BeautifulSoup

def scrape_stock_book_lpt(detailLink: str) -> Optional[str]:
    try:
        response = requests.get(detailLink)
        soup = BeautifulSoup(response.text, 'html.parser')

        info_divs = soup.find_all('div', class_='flex pb-2')
        for div in info_divs:
            paragraph = div.find('p', class_='font-mtregular text-secondary')
            
            if paragraph:
                text = paragraph.text.strip()

                if 'Disponibilidad:' in text:
                    stock = div.find('p', class_='font-mtbold text-v-greenpl-3').text.strip()
        return stock
    except:
        return None