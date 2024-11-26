from typing import List

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.genres import crud as genre_crud
from project.app.models.metadata import (
    MetaDataCreate,
    MetaDataUpdate,
    MetaDataPatch,
)
from project.app.models.combined import (
    CombinedResponseCreate,
    CombinedResponseReadAll,
    CombinedResponseRead,
    CombinedResponseUpdate,
    CombinedResponsePatch,
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


@router.post(
    "/",
    response_model=CombinedResponseCreate[GenreRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_genre(genre: GenreCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_genre = await genre_crud.create_genre(session=session, genre=genre)

        # construct the response in the expected format
        return CombinedResponseCreate(
            meta_data=MetaDataCreate(),
            response=db_genre,
        )


@router.get("/", response_model=CombinedResponseReadAll[List[GenreRead], int])
async def read_genres(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        genres, total_count = await genre_crud.read_genres(
            session=session, offset=offset, limit=limit
        )
        return CombinedResponseReadAll(
            response=genres,
            total_count=total_count,
        )


@router.get("/{id}", response_model=CombinedResponseRead[GenreRead])
async def read_genre(
    id: int = Path(..., title="The ID of the genre to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_genre = await genre_crud.read_genre(session=session, id=id)
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return CombinedResponseRead(response=GenreRead.model_validate(db_genre))


@router.put("/{id}", response_model=CombinedResponseUpdate[GenreRead])
async def update_genre(
    genre: GenreUpdate,
    id: int = Path(..., title="The ID of the genre to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_genre = await genre_crud.update_genre(session=session, id=id, genre=genre)
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")

        # construct the response in the expected format
        return CombinedResponseUpdate(
            meta_data=MetaDataUpdate(),
            response=db_genre,
        )


@router.patch("/{id}", response_model=CombinedResponsePatch[GenreRead])
async def patch_genre(
    genre: GenrePatch,
    id: int = Path(..., title="The ID of the genre to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_genre = await genre_crud.patch_genre(session=session, id=id, genre=genre)
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")

        # construct the response in the expected format
        return CombinedResponsePatch(
            meta_data=MetaDataPatch(),
            response=db_genre,
        )
