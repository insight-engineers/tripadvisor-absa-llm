from pydantic import BaseModel


class AspectRating(BaseModel):
    food: str
    price: str
    ambience: str
    service: str
