import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database, database_exists

from main import app
from database import get_db
from models import Base

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:159357@localhost:5433/test_video_catalog"

# Create a new test database if it doesn't exist
if not database_exists(TEST_DATABASE_URL):
    create_database(TEST_DATABASE_URL)

# Create all tables in the test database
engine = create_engine(TEST_DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Create a test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency with the test session
app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)


@pytest.fixture(scope="module")
def test_database():
    # Code that runs before the tests
    yield  # Yield the test database
    # Code that runs after the tests
    drop_database(TEST_DATABASE_URL)


def test_create_video(test_database):
    # Test create video endpoint
    video_data = {"title": "Test Video", "description": "Test Description", "duration": 60}
    response = client.post("/videos/", json=video_data)

    assert response.status_code == 200
    assert response.json()["title"] == video_data["title"]
    assert response.json()["description"] == video_data["description"]
    assert response.json()["duration"] == video_data["duration"]
    assert "id" in response.json()


def test_get_video(test_database):
    # Test get video endpoint
    video_data = {"title": "Test Video", "description": "Test Description", "duration": 60}
    response_create = client.post("/videos/", json=video_data)
    video_id = response_create.json()["id"]

    response_get = client.get(f"/videos/{video_id}")

    assert response_get.status_code == 200
    assert response_get.json()["title"] == video_data["title"]
    assert response_get.json()["description"] == video_data["description"]
    assert response_get.json()["duration"] == video_data["duration"]
    assert response_get.json()["id"] == video_id


def test_update_video(test_database):
    # Test update video endpoint
    video_data = {"title": "Test Video", "description": "Test Description", "duration": 60}
    response_create = client.post("/videos/", json=video_data)
    video_id = response_create.json()["id"]

    updated_video_data = {"title": "Updated Video", "description": "Updated Description", "duration": 120}
    response_update = client.put(f"/videos/{video_id}", json=updated_video_data)

    assert response_update.status_code == 200
    assert response_update.json()["title"] == updated_video_data["title"]
    assert response_update.json()["description"] == updated_video_data["description"]
    assert response_update.json()["duration"] == updated_video_data["duration"]
    assert response_update.json()["id"] == video_id


def test_delete_video(test_database):
    # Test delete video endpoint
    video_data = {"title": "Test Video", "description": "Test Description", "duration": 60}
    response_create = client.post("/videos/", json=video_data)
    video_id = response_create.json()["id"]

    response_delete = client.delete(f"/videos/{video_id}")

    assert response_delete.status_code == 200
    assert response_delete.json() == {"message": "Video deleted"}





