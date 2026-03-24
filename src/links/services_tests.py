from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from links.exceptions import LinkIntegrityError
from links.services import LinkService


@pytest.fixture
def m_repo() -> Mock:
    return Mock()


@pytest.fixture
def m_link() -> Mock:
    return Mock(original_url='url', short_url='shorturl')


def test_shorten_retry_on_integrity_error(
    m_repo: Mock,
    m_link: Mock,
) -> None:
    m_repo.create.side_effect = [
        IntegrityError('', None, Exception()),
        m_link,
    ]
    
    service = LinkService(m_repo)
    shorten_link = service.shorten('test')

    assert shorten_link == m_link.short_url
    assert m_repo.create.call_count == 2
    

def test_shorten_fail_after_max_attempt(m_repo: Mock) -> None:
    m_repo.create.side_effect = IntegrityError('', None, Exception())
    
    service = LinkService(m_repo)
    with pytest.raises(LinkIntegrityError):
        service.shorten('test')

    assert m_repo.create.call_count == LinkService.MAX_INTEGRITY_ERROR_RETRIES
    

def test_get_original_url_should_increment_clicks(
    m_repo: Mock,
    m_link: Mock,
) -> None:
    m_repo.get.return_value = m_link

    service = LinkService(m_repo)
    url = service.get_original_url('test')
    assert url == m_link.original_url

    m_repo.increment_clicks.assert_called_once_with(m_link)


def test_get_original_url_not_found(m_repo: Mock) -> None:
    m_repo.get.return_value = None

    service = LinkService(m_repo)
    url = service.get_original_url('test')
    assert url is None

    m_repo.increment_clicks.assert_not_called()

