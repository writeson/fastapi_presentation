from typing import List

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.albums import (
    Album,
    AlbumCreate,
    AlbumRead,
    AlbumReadWithTracks,
    AlbumUpdate,
    AlbumPatch,
)


async def create_album(session: AsyncSession, album: AlbumCreate):
    """
    Create a new Album in the database from the passed in AlbumCreate model.
    Returns the created AlbumRead model.
    """
    db_album = Album(title=album.title)
    session.add(db_album)
    await session.commit()
    await session.refresh(db_album)
    return AlbumRead.model_validate(db_album)


async def read_album(session: AsyncSession, id: int) -> AlbumRead | None:
    """
    Retrieve an Album from the database by ID.
    Returns the AlbumRead model if found, None otherwise.
    """
    query = select(Album).where(Album.id == id)
    result = await session.execute(query)
    db_album = result.scalar_one_or_none()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return AlbumRead.model_validate(db_album)


async def read_album_with_tracks(session: AsyncSession, id: int) -> AlbumReadWithTracks:
    """
    Retrieve an Album from the database with associated tracks
    Returns an album with a list of associated tracks
    """
    query = select(Album).options(selectinload(Album.tracks)).where(Album.id == id)
    result = await session.execute(query)
    db_album = result.scalar_one_or_none()
    return AlbumReadWithTracks.model_validate(db_album)


async def read_albums(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> [List[AlbumRead], int]:
    """
    Retrieve all Album from the database.
    Returns a list of AlbumRead models and the total count of albums.
    """
    query = select(Album).offset(offset).limit(limit)
    result = await session.execute(query)
    db_albums = result.scalars().all()

    # Query for total count
    count_query = select(func.count()).select_from(Album)
    total_count = await session.scalar(count_query)

    return [AlbumRead.model_validate(db_album) for db_album in db_albums], total_count


async def update_album(
    session: AsyncSession, id: int, album: AlbumUpdate
) -> AlbumRead | None:
    """
    Update an existing Album in the database using the passed in AlbumUpdate model.
    Returns the updated AlbumRead model if found, None otherwise.
    """
    db_album = await read_album(session, id)
    if db_album is None:
        return None

    for key, value in album.dict(exclude_unset=True).items():
        setattr(db_album, key, value)

    await session.commit()
    await session.refresh(db_album)
    return db_album


async def patch_album(
    session: AsyncSession, id: int, album: AlbumPatch
) -> AlbumRead | None:
    """
    Partially update an existing Album in the database using the passed in AlbumPatch model.
    Returns the updated AlbumRead model if found, None otherwise.
    """
    db_album = await read_album(session, id)
    if db_album is None:
        return None

    for key, value in album.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_album, key, value)

    await session.commit()
    await session.refresh(db_album)
    return db_album
