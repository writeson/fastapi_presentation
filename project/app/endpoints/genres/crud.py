from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.genres import (
    Genre,
    GenreCreate,
    GenreRead,
    GenreUpdate,
    GenrePatch,
)


async def create_genre(session: AsyncSession, genre: GenreCreate):
    """
    Create a new Genre in the database from the passed in GenreCreate model.
    Returns the created GenreRead model.
    """
    db_genre = Genre(name=genre.name)
    session.add(db_genre)
    await session.commit()
    await session.refresh(db_genre)
    return GenreRead.model_validate(db_genre)


async def read_genre(session: AsyncSession, id: int) -> GenreRead:
    """
    Retrieve a Genre from the database by ID.
    Returns the GenreRead model if found, raises HTTPException otherwise.
    """
    query = select(Genre).where(Genre.id == id)
    result = await session.execute(query)
    db_genre = result.scalar_one_or_none()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return GenreRead.model_validate(db_genre)


async def read_genres(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[GenreRead]:
    """
    Returns a list of GenreRead models and the total count of genres in the database.
    """
    # Query for paginated results
    query = select(Genre).offset(offset).limit(limit)
    result = await session.execute(query)
    db_genres = result.scalars().all()

    # Query for total count
    count_query = select(func.count()).select_from(Genre)
    total_count = await session.scalar(count_query)

    return [GenreRead.model_validate(db_genre) for db_genre in db_genres], total_count

async def update_genre(session: AsyncSession, id: int, genre: GenreUpdate) -> GenreRead:
    """
    Update an existing Genre in the database using the passed in GenreUpdate model.
    Returns the updated GenreRead model if found, raises HTTPException otherwise.
    """
    db_genre = await read_genre(session, id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    for key, value in genre.dict(exclude_unset=True).items():
        setattr(db_genre, key, value)

    await session.commit()
    await session.refresh(db_genre)
    return GenreRead.model_validate(db_genre)


async def patch_genre(session: AsyncSession, id: int, genre: GenrePatch) -> GenreRead:
    """
    Partially update an existing Genre in the database using the passed in GenrePatch model.
    Returns the updated GenreRead model if found, raises HTTPException otherwise.
    """
    db_genre = await read_genre(session, id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    for key, value in genre.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_genre, key, value)

    await session.commit()
    await session.refresh(db_genre)
    return GenreRead.model_validate(db_genre)
