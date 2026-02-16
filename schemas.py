from pydantic import BaseModel

class DestinationCreate(BaseModel):
    id: int
    name: str
    city: str
    category: str
    rating: float
