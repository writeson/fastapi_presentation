from project.app.models.albums import (
    Album,
    AlbumCreate,
    AlbumRead,
    AlbumUpdate,
    AlbumPatch,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_album(session: AsyncSession, album: AlbumCreate):
    """
    Create a new Album in the database from the passed in AlbumCreate model.
    Returns the created AlbumRead model.
    """
    db_album = Album(title=album.title)
    session.add(db_album)
    await session.commit()
    await session.refresh(db_album)
    return db_album


async def read_album(session: AsyncSession, id: int) -> AlbumRead | None:
    """
    Retrieve an Album from the database by ID.
    Returns the AlbumRead model if found, None otherwise.
    """
    query = select(Album).where(Album.id == id)
    result = await session.execute(query)
    db_album = result.scalar_one_or_none()
    return db_album

async def read_albums(session: AsyncSession, offset: int=0, limit: int=10) -> list[AlbumRead]:
    """
    Retrieve all Album from the database.
    Returns a list of AlbumRead models.
    """
    query = select(Album).offset(offset).limit(limit)
    result = await session.execute(query)
    db_albums = result.scalars().all()
    return db_albums


async def update_album(session: AsyncSession, id: int, album: AlbumUpdate) -> AlbumRead | None:
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


async def patch_album(session: AsyncSession, id: int, album: AlbumPatch) -> AlbumRead | None:
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