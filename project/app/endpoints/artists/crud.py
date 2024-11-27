from typing import List

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.artists import (
    Artist,
    ArtistCreate,
    ArtistRead,
    ArtistReadWithAlbums,
    ArtistUpdate,
    ArtistPatch,
)
from project.app.models.albums import Album


async def create_artist(session: AsyncSession, artist: ArtistCreate) -> ArtistRead:
    """
    Create a new Artist in the database from the passed in ArtistCreate model.
    Returns the created ArtistRead model.
    """
    db_artist = Artist(name=artist.name)
    session.add(db_artist)
    await session.commit()
    await session.refresh(db_artist)
    return ArtistRead.model_validate(db_artist)


async def read_artist(session: AsyncSession, id: int) -> ArtistRead:
    """
    Retrieve an Artist from the database by ID.
    Returns the ArtistRead model if found, None otherwise.
    """
    query = select(Artist).where(Artist.id == id)
    result = await session.execute(query)
    db_artist = result.scalar_one_or_none()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return ArtistRead.model_validate(db_artist)


async def read_artists(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> List[ArtistRead]:
    """
    Retrieve all Artists from the database.
    Returns a list of ArtistRead models.
    """
    query = select(Artist).offset(offset).limit(limit)
    result = await session.execute(query)
    db_artists = result.scalars().all()

    # Query for total count
    count_query = select(func.count()).select_from(Artist)
    total_count = await session.scalar(count_query)

    return [
        ArtistRead.model_validate(db_artist) for db_artist in db_artists
    ], total_count


async def read_artist_with_albums(
    session: AsyncSession, id: int, offset: int = 0, limit: int = 10
) -> [ArtistReadWithAlbums, int]:
    """
    Retrieve an Artist the database with an paginated
    list of associated albums
    """
    query = select(Artist).where(Artist.id == id)

    # Execute the query
    result = await session.execute(query)
    db_artist = result.scalar_one_or_none()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")

    # Fetch albums separately with limit and offset
    albums_query = (
        select(Album)
        .where(Album.artist_id == id)
        .offset(offset)
        .limit(limit)
        .order_by(Album.id)
    )
    albums_result = await session.execute(albums_query)
    albums = list(albums_result.scalars().all())
    db_artist.albums = albums

    # Query for total count of albums
    count_query = select(func.count()).select_from(Album)
    total_count = await session.scalar(count_query)

    return [ArtistReadWithAlbums.model_validate(db_artist), total_count]


async def update_artist(
    session: AsyncSession, id: int, artist: ArtistUpdate
) -> ArtistRead:
    """
    Update an existing Artist in the database using the passed in ArtistUpdate model.
    Returns the updated ArtistRead model if found, None otherwise.
    """
    db_artist = await read_artist(session, id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")

    for key, value in artist.dict(exclude_unset=True).items():
        setattr(db_artist, key, value)

    await session.commit()
    await session.refresh(db_artist)
    return ArtistRead.model_validate(db_artist)


async def patch_artist(
    session: AsyncSession, id: int, artist: ArtistPatch
) -> ArtistRead:
    """
    Partially update an existing Artist in the database using the passed in ArtistPatch model.
    Returns the updated ArtistRead model if found, None otherwise.
    """
    db_artist = await read_artist(session, id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")

    for key, value in artist.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_artist, key, value)

    await session.commit()
    await session.refresh(db_artist)
    return ArtistRead.model_validate(db_artist)
