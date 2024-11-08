from project.app.models.artists import (
    Artist,
    ArtistCreate,
    ArtistRead,
    ArtistReadWithAlbums,
    ArtistUpdate,
    ArtistPatch,
)

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession


async def create_artist(session: AsyncSession, artist: ArtistCreate):
    """
    Create a new Artist in the database from the passed in ArtistCreate model.
    Returns the created ArtistRead model.
    """
    db_artist = Artist(name=artist.name)
    session.add(db_artist)
    await session.commit()
    await session.refresh(db_artist)
    return ArtistRead.model_validate(db_artist)


async def read_artist(session: AsyncSession, id: int) -> ArtistRead | None:
    """
    Retrieve an Artist from the database by ID.
    Returns the ArtistRead model if found, None otherwise.
    """
    query = select(Artist).where(Artist.id == id)
    result = await session.execute(query)
    db_artist = result.scalar_one_or_none()
    return ArtistRead.model_validate(db_artist)


async def read_artist_with_albums(
    session: AsyncSession, id: int
) -> ArtistReadWithAlbums | None:
    """
    Retrieve an Artist with its albums from the database.
    Returns an ArtistReadWithAlbums model."""
    query = select(Artist).options(joinedload(Artist.albums)).where(Artist.id == id)
    result = await session.execute(query)
    db_artist = result.unique().scalar_one_or_none()
    if db_artist is None:
        return None
    return ArtistReadWithAlbums.model_validate(db_artist)


async def read_artists(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[ArtistRead]:
    """
    Retrieve all Artists from the database.
    Returns a list of ArtistRead models.
    """
    query = select(Artist).offset(offset).limit(limit)
    result = await session.execute(query)
    db_artists = result.scalars().all()
    return [ArtistRead.model_validate(db_artist) for db_artist in db_artists]


async def update_artist(
    session: AsyncSession, id: int, artist: ArtistUpdate
) -> ArtistRead | None:
    """
    Update an existing Artist in the database using the passed in ArtistUpdate model.
    Returns the updated ArtistRead model if found, None otherwise.
    """
    db_artist = await read_artist(session, id)
    if db_artist is None:
        return None

    for key, value in artist.dict(exclude_unset=True).items():
        setattr(db_artist, key, value)

    await session.commit()
    await session.refresh(db_artist)
    return ArtistRead.model_validate(db_artist)


async def patch_artist(
    session: AsyncSession, id: int, artist: ArtistPatch
) -> ArtistRead | None:
    """
    Partially update an existing Artist in the database using the passed in ArtistPatch model.
    Returns the updated ArtistRead model if found, None otherwise.
    """
    db_artist = await read_artist(session, id)
    if db_artist is None:
        return None

    for key, value in artist.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_artist, key, value)

    await session.commit()
    await session.refresh(db_artist)
    return ArtistRead.model_validate(db_artist)
