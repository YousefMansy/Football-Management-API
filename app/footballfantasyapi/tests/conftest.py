import json
import pytest
from typing import Any
from fastapi import FastAPI
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from footballfantasyapi.db.base import Base
from footballfantasyapi.api.deps import get_db
from footballfantasyapi.api.api_v1.api import api_router
from footballfantasyapi.core.auth import authenticate, create_access_token


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def login_data():
    yield {'username': 'test@footballfantasyapi.com', 'password': 'testing'}


@pytest.fixture(scope="function")
def user_data():
    yield {'email': 'test@footballfantasyapi.com', 'password': 'testing'}


@pytest.fixture(scope="function")
def authorized_user(authorized_client):
    yield authorized_client.get('/auth/profile').json()['user']


@pytest.fixture(scope="function")
def authorized_client(db_session: SessionTesting, client, user_data, login_data) -> Generator[TestClient, Any, None]:
    client.post('/auth/signup', json.dumps(user_data))
    client.headers['content-type'] = 'application/x-www-form-urlencoded'
    test_user = authenticate(email=login_data['username'], password=login_data['password'], db=db_session)
    access_token = create_access_token(sub=str(test_user.id))
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}",
    }
    yield client
