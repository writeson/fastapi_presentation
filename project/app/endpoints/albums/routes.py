from typing import List

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.albums import crud as album_crud
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
from project.app.models.albums import (
    AlbumCreate,
    AlbumRead,
    AlbumReadWithTracks,
    AlbumUpdate,
    AlbumPatch,
)


router = APIRouter(
    prefix="/albums",
    tags=["Albums"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post(
    "/",
    response_model=CombinedResponseCreate[AlbumRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_album(album: AlbumCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_album = await album_crud.create_album(session=session, album=album)

        # construct the response in the expected format
        return CombinedResponseCreate(
            meta_data=MetaDataCreate(),
            response=db_album,
        )


@router.get("/", response_model=CombinedResponseReadAll[List[AlbumRead], int])
async def read_albums(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        albums, total_count = await album_crud.read_albums(
            session=session, offset=offset, limit=limit
        )
        return CombinedResponseReadAll(
            response=albums,
            total_count=total_count,
        )


@router.get("/{id}", response_model=CombinedResponseRead[AlbumRead])
async def read_album(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_album = await album_crud.read_album(session=session, id=id)
        if db_album is None:
            raise HTTPException(status_code=404, detail="Album not found")
        return CombinedResponseRead(response=AlbumRead.model_validate(db_album))


@router.get("/{id}/tracks", response_model=CombinedResponseRead[AlbumReadWithTracks])
async def read_album_with_tracks(
    id: int = Path(..., title="The ID of the album to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_album = await album_crud.read_album_with_tracks(session=session, id=id)
        if db_album is None:
            raise HTTPException(status_code=404, detail="Album not found")
        return CombinedResponseRead(
            response=AlbumReadWithTracks.model_validate(db_album)
        )


@router.put("/{id}", response_model=CombinedResponseUpdate[AlbumRead])
async def update_album(
    album: AlbumUpdate,
    id: int = Path(..., title="The ID of the album to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_album = await album_crud.update_album(session=session, id=id, album=album)
        if db_album is None:
            raise HTTPException(status_code=404, detail="Album not found")

        # construct the response in the expected format
        return CombinedResponseUpdate(
            meta_data=MetaDataUpdate(),
            response=db_album,
        )


@router.patch("/{id}", response_model=CombinedResponsePatch[AlbumRead])
async def patch_album(
    album: AlbumPatch,
    id: int = Path(..., title="The ID of the album to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_album = await album_crud.patch_album(session=session, id=id, album=album)
        if db_album is None:
            raise HTTPException(status_code=404, detail="Album not found")

        # construct the response in the expected format
        return CombinedResponsePatch(
            meta_data=MetaDataPatch(),
            response=db_album,
        )
