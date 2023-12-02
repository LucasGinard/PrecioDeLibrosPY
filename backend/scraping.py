from model.BookData import BookData
from typing import List

def scrape_books(search_query: str) -> List[BookData]:
    scraped_data = [
        {
            "title": f"{search_query} Book 1",
            "image_url": "http://example.com/image1.jpg",
            "price": "19.99",
            "details_url": "http://example.com/book1",
        },
        {
            "title": f"{search_query} Book 2",
            "image_url": "http://example.com/image2.jpg",
            "price": "29.99",
            "details_url": "http://example.com/book2",
        },
    ]
    return [BookData(**data) for data in scraped_data]


