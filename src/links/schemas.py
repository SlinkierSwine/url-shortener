from pydantic import BaseModel, HttpUrl


class LinkResponse(BaseModel):
    short_id: str
    original_url: str
    clicks: int


class ShortIdResponse(BaseModel):
    short_url: HttpUrl


class LinkCreate(BaseModel):
    url: HttpUrl
