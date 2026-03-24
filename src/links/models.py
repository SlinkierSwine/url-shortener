from sqlalchemy import Column, Integer, String

from db.base import Base
from config import settings


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_id = Column(String(settings.SHORT_ID_LENGTH), unique=True, index=True)
    clicks = Column(Integer, default=0)

    @property
    def short_url(self) -> str:
        return settings.DOMEN + '/' + self.short_id

