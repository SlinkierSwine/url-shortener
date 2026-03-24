from collections.abc import Iterator
from unittest.mock import Mock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from links.exceptions import LinkIntegrityError
from links.services import LinkService


@pytest.fixture
def m_repo() -> Iterator[Mock]:
    with patch('links.services.LinkRepository') as m:
        yield m


def test_shorten_retry_on_integrity_error(m_repo: Mock) -> None:
    m_repo.create.side_effect = [
        IntegrityError('', None, Exception()),
        None
    ]
    
    service = LinkService(m_repo)
    service.shorten('test')
    

def test_shorten_fail_after_max_attempt(m_repo: Mock) -> None:
    m_repo.create.side_effect = IntegrityError('', None, Exception())
    
    service = LinkService(m_repo)
    with pytest.raises(LinkIntegrityError):
        service.shorten('test')
    
