from urllib.parse import urlparse
from collections.abc import Iterator
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
import pytest


def _extract_short_id(short_url: str) -> str:
    return urlparse(short_url).path.strip("/")


@pytest.fixture
def f_short_id() -> str:
    return 'shrtid'


@pytest.fixture
def m_generate_short_id(f_short_id: str) -> Iterator[Mock]:
    with patch('links.services.generate_short_id') as m:
        m.return_value = f_short_id
        yield m


@pytest.fixture
def f_generated_short_id(f_client: TestClient) -> str:
    res = f_client.post("/shorten", json={"url": "https://example.com"})
    short_url = res.json()["short_url"]
    return _extract_short_id(short_url)


@pytest.mark.usefixtures('m_generate_short_id')
def test_shorten(f_client: TestClient, f_short_id: str) -> None:
    res = f_client.post("/shorten", json={"url": "https://example.com"})
    assert res.status_code == 200

    short_url = res.json()["short_url"]
    short_id = _extract_short_id(short_url)

    assert short_id == f_short_id


def test_redirect(f_client: TestClient, f_generated_short_id: str) -> None:
    res = f_client.get(f"/{f_generated_short_id}", follow_redirects=False)
    assert res.status_code in (302, 307)
    assert res.headers["location"].rstrip('/') == "https://example.com"


def test_stats(f_client: TestClient, f_generated_short_id: str) -> None:
    stats = f_client.get(f"/stats/{f_generated_short_id}")

    assert stats.status_code == 200
    assert stats.json()["clicks"] == 0


def test_stats_not_found(f_client: TestClient):
    res = f_client.get("/stats/unknown")
    assert res.status_code == 404


def test_redirect_and_stats(f_client: TestClient, f_generated_short_id: str) -> None:
    f_client.get(f"/{f_generated_short_id}", follow_redirects=False)
    stats = f_client.get(f"/stats/{f_generated_short_id}")

    assert stats.status_code == 200
    assert stats.json()["clicks"] == 1


def test_not_found(f_client: TestClient) -> None:
    res = f_client.get("/unknown")
    assert res.status_code == 404

