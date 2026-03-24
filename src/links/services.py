from fastapi import Depends
from sqlalchemy.orm import Session
from links.models import Link
from links.repositories import LinkRepository
from links.utils import generate_short_id
from db import get_db


class LinkService:
    def __init__(self, repo: LinkRepository) -> None:
        self._repo = repo

    def get_link(self, short_id: str) -> Link | None:
        return self._repo.get(short_id)

    def shorten(self, url: str) -> Link:
        short_id = generate_short_id()
        return self._repo.create(url, short_id)

    def increment_clicks(self, link: Link) -> None:
        self._repo.increment_clicks(link)


def get_link_service(db: Session = Depends(get_db)) -> LinkService:
    repo = LinkRepository(db)
    return LinkService(repo)

