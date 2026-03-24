import logging

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from links.models import Link
from links.repositories import LinkRepository
from links.utils import generate_short_id
from db import get_db
from links.exceptions import LinkIntegrityError

logger = logging.getLogger(__name__)


class LinkService:
    MAX_INTEGRITY_ERROR_RETRIES = 5

    def __init__(self, repo: LinkRepository) -> None:
        self._repo = repo

    def get_link(self, short_id: str) -> Link | None:
        return self._repo.get(short_id)

    def get_original_url(self, short_id: str) -> str | None:
        link = self._repo.get(short_id)

        if not link:
            return

        self._repo.increment_clicks(link)
        return link.original_url

    def shorten(self, url: str) -> Link:
        short_id = generate_short_id()

        for _ in range(self.MAX_INTEGRITY_ERROR_RETRIES):
            try:
                return self._repo.create(url, short_id)
            except IntegrityError:
                continue

        logger.error(
            f'Failed to generate unique short_id after'
            f' {self.MAX_INTEGRITY_ERROR_RETRIES} attempts',
        )
        raise LinkIntegrityError(
            'Failed to generate unique short_id, try again later'
        )


def get_link_service(db: Session = Depends(get_db)) -> LinkService:
    repo = LinkRepository(db)
    return LinkService(repo)

