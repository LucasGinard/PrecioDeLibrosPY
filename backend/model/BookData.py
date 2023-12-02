from pydantic import BaseModel, HttpUrl

class BookData(BaseModel):
    title: str
    image_url: HttpUrl
    price: str
    details_url: HttpUrl