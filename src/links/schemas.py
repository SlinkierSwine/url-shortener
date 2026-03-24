from pydantic import BaseModel


class LinkResponse(BaseModel):
    short_id: str
    original_url: str
    clicks: int


class ShortIdResponse(BaseModel):
    short_id: str

