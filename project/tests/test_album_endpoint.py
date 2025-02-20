from typing import AsyncGenerator
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models.albums import Album, AlbumCreate, AlbumRead
from app.models.artists import Artist

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for tests
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Test data
test_artist = {
    "id": 1,
    "name": "Test Artist"
}

test_album = {
    "title": "Test Album",
    "artist_id": 1
}

expected_album_response = {
    "id": 1,
    "title": "Test Album",
    "artist_id": 1
}

@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Album.metadata.create_all)
        await conn.run_sync(Artist.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        # Clean up after test
        async with engine.begin() as conn:
            await conn.run_sync(Album.metadata.drop_all)
            await conn.run_sync(Artist.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def async_client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async client with the test database session."""
    async def override_get_db():
        try:
            yield async_session
        finally:
            await async_session.close()

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="function")
async def test_artist_fixture(async_session: AsyncSession) -> Artist:
    """Create a test artist in the database."""
    artist = Artist(**test_artist)
    async_session.add(artist)
    await async_session.commit()
    return artist

@pytest.mark.asyncio
async def test_create_album(async_client: AsyncClient, test_artist_fixture: Artist):
    """Test creating a new album."""
    response = await async_client.post("/api/v1/albums/", json=test_album)
    
    assert response.status_code == 201
    data = response.json()
    assert "response" in data
    album_data = data["response"]
    assert album_data["title"] == test_album["title"]
    assert album_data["artist_id"] == test_album["artist_id"]
    assert "id" in album_data

@pytest.mark.asyncio
async def test_read_album(
    async_client: AsyncClient, 
    async_session: AsyncSession,
    test_artist_fixture: Artist
):
    """Test reading an album by ID."""
    # Create test album first
    album = Album(**test_album)
    async_session.add(album)
    await async_session.commit()
    await async_session.refresh(album)

    response = await async_client.get(f"/api/v1/albums/{album.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    album_data = data["response"]
    assert album_data["title"] == test_album["title"]
    assert album_data["artist_id"] == test_album["artist_id"]

@pytest.mark.asyncio
async def test_read_albums(
    async_client: AsyncClient, 
    async_session: AsyncSession,
    test_artist_fixture: Artist
):
    """Test reading all albums."""
    # Create test album first
    album = Album(**test_album)
    async_session.add(album)
    await async_session.commit()

    response = await async_client.get("/api/v1/albums/")
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    albums = data["response"]
    assert len(albums) >= 1
    assert any(a["title"] == test_album["title"] for a in albums)

@pytest.mark.asyncio
async def test_update_album(
    async_client: AsyncClient, 
    async_session: AsyncSession,
    test_artist_fixture: Artist
):
    """Test updating an album."""
    # Create test album first
    album = Album(**test_album)
    async_session.add(album)
    await async_session.commit()
    await async_session.refresh(album)

    update_data = {
        "title": "Updated Album Title",
        "artist_id": test_artist_fixture.id
    }

    response = await async_client.put(
        f"/api/v1/albums/{album.id}",
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    album_data = data["response"]
    assert album_data["title"] == update_data["title"]
    assert album_data["artist_id"] == update_data["artist_id"]

@pytest.mark.asyncio
async def test_patch_album(
    async_client: AsyncClient, 
    async_session: AsyncSession,
    test_artist_fixture: Artist
):
    """Test partially updating an album."""
    # Create test album first
    album = Album(**test_album)
    async_session.add(album)
    await async_session.commit()
    await async_session.refresh(album)

    patch_data = {
        "title": "Patched Album Title"
    }

    response = await async_client.patch(
        f"/api/v1/albums/{album.id}",
        json=patch_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    album_data = data["response"]
    assert album_data["title"] == patch_data["title"]
    assert album_data["artist_id"] == test_album["artist_id"]  # Should remain unchanged

@pytest.mark.asyncio
async def test_album_not_found(async_client: AsyncClient):
    """Test getting a non-existent album."""
    response = await async_client.get("/api/v1/albums/999999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

@pytest.mark.asyncio
async def test_create_album_invalid_artist(async_client: AsyncClient):
    """Test creating an album with non-existent artist."""
    invalid_album = {
        "title": "Test Album",
        "artist_id": 999999  # Non-existent artist ID
    }
    
    response = await async_client.post("/api/v1/albums/", json=invalid_album)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data 