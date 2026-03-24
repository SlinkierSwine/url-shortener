from collections.abc import Iterator
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.base import Base
from main import app
from db import get_db
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # to use one connection for all queries
)

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def f_db() -> Iterator[Session]:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        # recreate tables on each test
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def f_client(f_db: Session) -> Iterator[TestClient]:
    # to use sqlite instead of postgres
    def override_get_db() -> Iterator[Session]:
        yield f_db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

