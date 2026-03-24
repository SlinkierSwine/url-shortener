from sqlalchemy.orm import Session

from links.models import Link


class LinkRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, short_id: str) -> Link | None:
        return self._db.query(Link).filter(Link.short_id == short_id).first()

    def create(self, url: str, short_id: str) -> Link:
        link = Link(
            original_url=url,
            short_id=short_id,
        )
        self._db.add(link)
        self._db.commit()
        self._db.refresh(link)
        return link
    
    def increment_clicks(self, link: Link) -> None:
        link.clicks += 1
        self._db.commit()

