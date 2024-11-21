from typing import List

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.genres import crud as genre_crud
from project.app.models.metadata import (
    MetaData,
    MetaDataReadAll,
)
from project.app.models.genres import (
    GenreCreate,
    GenreRead,
    GenreUpdate,
    GenrePatch,
)


router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=GenreRead, status_code=status.HTTP_201_CREATED)
async def create_genre(genre: GenreCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await genre_crud.create_genre(session=session, genre=genre)


@router.get("/", response_model=MetaDataReadAll[List[GenreRead], int])
async def read_genres(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        genres, total_count = await genre_crud.read_genres(
            session=session, offset=offset, limit=limit
        )
        retval = MetaDataReadAll[List[GenreRead], int](
            meta_data = MetaData(),
            response=[GenreRead.model_validate(genre) for genre in genres],
            total_count=total_count,
        )
        return retval


@router.get("/{id}", response_model=GenreRead)
async def read_genre(
    id: int = Path(..., title="The ID of the genre to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_genre = await genre_crud.read_genre(session=session, id=id)
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return db_genre


@router.put("/{id}", response_model=GenreRead)
async def update_genre(
    genre: GenreUpdate,
    id: int = Path(..., title="The ID of the genre to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_genre = await genre_crud.update_genre(session=session, id=id, genre=genre)
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return db_genre


@router.patch("/{id}", response_model=GenreRead)
async def patch_genre(
    genre: GenrePatch,
    id: int = Path(..., title="The ID of the genre to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_genre = await genre_crud.patch_genre(session=session, id=id, genre=genre)
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return db_genre
