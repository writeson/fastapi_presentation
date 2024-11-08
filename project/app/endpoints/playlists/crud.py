from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.playlists import (
    Playlist,
    PlaylistCreate,
    PlaylistRead,
    PlaylistUpdate,
    PlaylistPatch,
)


async def create_playlist(session: AsyncSession, genre: PlaylistCreate):
    """
    Create a new Playlist in the database from the passed in PlaylistCreate model.
    Returns the created PlaylistRead model.
    """
    db_playlist = Playlist(name=genre.name)
    session.add(db_playlist)
    await session.commit()
    await session.refresh(db_playlist)
    return PlaylistRead.model_validate(db_playlist)


async def read_playlist(session: AsyncSession, id: int) -> PlaylistRead:
    """
    Retrieve a Playlist from the database by ID.
    Returns the PlaylistRead model if found, raises HTTPException otherwise.
    """
    query = select(Playlist).where(Playlist.id == id)
    result = await session.execute(query)
    db_playlist = result.scalar_one_or_none()
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return PlaylistRead.model_validate(db_playlist)


async def read_playlists(
        session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[PlaylistRead]:
    """
    Retrieve all Playlists from the database.
    Returns a list of PlaylistRead models.
    """
    query = select(Playlist).offset(offset).limit(limit)
    result = await session.execute(query)
    db_playlists = result.scalars().all()
    return [PlaylistRead.model_validate(db_playlist) for db_playlist in db_playlists]


async def update_playlist(
        session: AsyncSession, id: int, genre: PlaylistUpdate
) -> PlaylistRead:
    """
    Update an existing Playlist in the database using the passed in PlaylistUpdate model.
    Returns the updated PlaylistRead model if found, raises HTTPException otherwise.
    """
    db_playlist = await read_playlist(session, id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")

    for key, value in genre.dict(exclude_unset=True).items():
        setattr(db_playlist, key, value)

    await session.commit()
    await session.refresh(db_playlist)
    return PlaylistRead.model_validate(db_playlist)


async def patch_playlist(
        session: AsyncSession, id: int, genre: PlaylistPatch
) -> PlaylistRead:
    """
    Partially update an existing Playlist in the database using the passed in PlaylistPatch model.
    Returns the updated PlaylistRead model if found, raises HTTPException otherwise.
    """
    db_playlist = await read_playlist(session, id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")

    for key, value in genre.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_playlist, key, value)

    await session.commit()
    await session.refresh(db_playlist)
    return PlaylistRead.model_validate(db_playlist)
