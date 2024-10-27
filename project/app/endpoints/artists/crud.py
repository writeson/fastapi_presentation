from project.app.models.artists import (
    Artist,
    ArtistCreate,
    ArtistRead,
    ArtistUpdate,
    ArtistPatch,
)

from sqlalchemy import select
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
    return db_artist


async def read_artist(session: AsyncSession, id: int) -> ArtistRead | None:
    """
    Retrieve an Artist from the database by ID.
    Returns the ArtistRead model if found, None otherwise.
    """
    query = select(Artist).where(Artist.id == id)
    result = await session.execute(query)
    db_artist = result.scalar_one_or_none()
    return db_artist

async def read_artists(session: AsyncSession, offset: int=0, limit: int=10) -> list[ArtistRead]:
    """
    Retrieve all Artists from the database.
    Returns a list of ArtistRead models.
    """
    query = select(Artist).offset(offset).limit(limit)
    result = await session.execute(query)
    db_artists = result.scalars().all()
    return db_artists


async def update_artist(session: AsyncSession, id: int, artist: ArtistUpdate) -> ArtistRead | None:
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
    return db_artist


async def patch_artist(session: AsyncSession, id: int, artist: ArtistPatch) -> ArtistRead | None:
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
    return db_artist