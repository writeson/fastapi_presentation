from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.tracks import (
    Track,
    TrackCreate,
    TrackRead,
    TrackReadWithPlaylists,
    TrackUpdate,
    TrackPatch,
)


async def create_track(session: AsyncSession, album: TrackCreate) -> TrackRead:
    """
    Create a new Track in the database from the passed in TrackCreate model.
    Returns the created TrackRead model.
    """
    db_track = Track(title=album.title)
    session.add(db_track)
    await session.commit()
    await session.refresh(db_track)
    return TrackRead.model_validate(db_track)


async def read_track(session: AsyncSession, id: int) -> TrackRead:
    """
    Retrieve a Track from the database by ID.
    Returns the TrackRead model if found, None otherwise.
    """
    query = (
        select(Track)
        .options(
            joinedload(Track.genre),
            joinedload(Track.media_type),
        )
        .where(Track.id == id)
    )
    result = await session.execute(query)
    db_track = result.unique().scalar_one_or_none()
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return db_track


async def read_tracks(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[TrackRead]:
    """
    Retrieve all Track from the database.
    Returns a list of TrackRead models.
    """
    query = (
        select(Track)
        .options(
            joinedload(Track.genre),
            joinedload(Track.media_type),
        )
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(query)
    db_tracks = result.scalars().all()
    return [TrackRead.model_validate(db_track) for db_track in db_tracks]


async def read_track_with_playlists(
    session: AsyncSession, id: int
) -> TrackReadWithPlaylists:
    query = (
        select(Track)
        .options(
            joinedload(Track.genre),
            joinedload(Track.media_type),
            joinedload(Track.playlists),
        )
        .where(Track.id == id)
    )
    result = await session.execute(query)
    db_track = result.unique().scalar_one_or_none()
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return TrackReadWithPlaylists.model_validate(db_track)


async def update_track(session: AsyncSession, id: int, album: TrackUpdate) -> TrackRead:
    """
    Update an existing Track in the database using the passed in TrackUpdate model.
    Returns the updated TrackRead model if found, None otherwise.
    """
    db_track = await read_track(session, id)
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    for key, value in album.dict(exclude_unset=True).items():
        setattr(db_track, key, value)

    await session.commit()
    await session.refresh(db_track)
    return TrackRead.model_validate(db_track)


async def patch_track(session: AsyncSession, id: int, album: TrackPatch) -> TrackRead:
    """
    Partially update an existing Track in the database using the passed in TrackPatch model.
    Returns the updated TrackRead model if found, None otherwise.
    """
    db_track = await read_track(session, id)
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    for key, value in album.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_track, key, value)

    await session.commit()
    await session.refresh(db_track)
    return TrackRead.model_validate(db_track)
