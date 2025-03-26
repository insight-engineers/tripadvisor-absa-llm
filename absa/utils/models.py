from typing import Literal

from pydantic import BaseModel


class AspectRating(BaseModel):
    general: Literal["positive", "neutral", "negative", "not_given"]
    food: Literal["positive", "neutral", "negative", "not_given"]
    price: Literal["positive", "neutral", "negative", "not_given"]
    ambience: Literal["positive", "neutral", "negative", "not_given"]
    service: Literal["positive", "neutral", "negative", "not_given"]
    location: Literal["positive", "neutral", "negative", "not_given"]
