from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.media_types import (
    MediaType,
    MediaTypeCreate,
    MediaTypeRead,
    MediaTypeUpdate,
    MediaTypePatch,
)


async def create_media_type(session: AsyncSession, media_type: MediaTypeCreate):
    """
    Create a new MediaType in the database from the passed in MediaTypeCreate model.
    Returns the created MediaTypeRead model.
    """
    db_media_type = MediaType(name=media_type.name)
    session.add(db_media_type)
    await session.commit()
    await session.refresh(db_media_type)
    return MediaTypeRead.model_validate(db_media_type)


async def read_media_type(session: AsyncSession, id: int) -> MediaTypeRead:
    """
    Retrieve a MediaType from the database by ID.
    Returns the MediaTypeRead model if found, raises HTTPException otherwise.
    """
    query = select(MediaType).where(MediaType.id == id)
    result = await session.execute(query)
    db_media_type = result.scalar_one_or_none()
    if db_media_type is None:
        raise HTTPException(status_code=404, detail="Media type not found")
    return MediaTypeRead.model_validate(db_media_type)


async def read_media_types(
        session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[MediaTypeRead]:
    """
    Retrieve all Media types from the database.
    Returns a list of MediaRead models.
    """
    query = select(MediaType).offset(offset).limit(limit)
    result = await session.execute(query)
    db_media_types = result.scalars().all()
    return [MediaTypeRead.model_validate(db_media_type) for db_media_type in db_media_types]


async def update_media_type(
        session: AsyncSession, id: int, media_type: MediaTypeUpdate
) -> MediaTypeRead:
    """
    Update an existing MediaType in the database using the passed in MediaTypeUpdate model.
    Returns the updated MediaTypeRead model if found, raises HTTPException otherwise.
    """
    db_media_type = await read_media_type(session, id)
    if db_media_type is None:
        raise HTTPException(status_code=404, detail="Media type not found")

    for key, value in media_type.dict(exclude_unset=True).items():
        setattr(db_media_type, key, value)

    await session.commit()
    await session.refresh(db_media_type)
    return MediaTypeRead.model_validate(db_media_type)


async def patch_media_type(
        session: AsyncSession, id: int, media_type: MediaTypePatch
) -> MediaTypeRead:
    """
    Partially update an existing MediaType in the database using the passed in MediaTypePatch model.
    Returns the updated MediaTypeRead model if found, raises HTTPException otherwise.
    """
    db_media_type = await read_media_type(session, id)
    if db_media_type is None:
        raise HTTPException(status_code=404, detail="Media type not found")

    for key, value in media_type.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_media_type, key, value)

    await session.commit()
    await session.refresh(db_media_type)
    return MediaTypeRead.model_validate(db_media_type)
