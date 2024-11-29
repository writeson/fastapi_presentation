from typing import List

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.artists import crud as artist_crud
from project.app.endpoints.common import (
    create_item,
    read_items,
    read_item,
    update_item,
    patch_item,
)
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
from project.app.models.artists import (
    Artist,
    ArtistCreate,
    ArtistRead,
    ArtistUpdate,
    ArtistPatch,
)
from project.app.models.albums import Album, AlbumRead


router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post(
    "/",
    response_model=CombinedResponseCreate[ArtistRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_artist(artist: ArtistCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_artist = await create_item(session, artist, Artist, ArtistRead)
        if db_artist is None:
            raise HTTPException(status_code=400, detail="Artist already exists")
        return CombinedResponseCreate(
            meta_data=MetaDataCreate(),
            response=db_artist,
        )


@router.get("/", response_model=CombinedResponseReadAll[List[ArtistRead], int])
async def read_artists(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        artists, total_count= await read_items(session, offset, limit, Artist, ArtistRead)
        return CombinedResponseReadAll(
            response=artists,
            total_count=total_count,
        )


@router.get("/{id}", response_model=CombinedResponseRead[ArtistRead])
async def read_artist(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_artist = await read_item(session, id, Artist, ArtistRead)
        if db_artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")
        return CombinedResponseRead(response=ArtistRead.model_validate(db_artist))


@router.get("/{id}/albums", response_model=CombinedResponseReadAll[List[AlbumRead], int])
async def read_artist_albums(
    id: int = Path(..., title="The ID of the artist to get"),
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        albums, total_count= await read_items(session, offset, limit, Album, AlbumRead)
        return CombinedResponseReadAll(
            response=albums,
            total_count=total_count,
        )


@router.put("/{id}", response_model=CombinedResponseUpdate[ArtistRead])
async def update_artist(
    artist: ArtistUpdate,
    id: int = Path(..., title="The ID of the artist to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_artist = await update_item(session, id, artist, Artist, ArtistRead)
        if db_artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")

        # construct the response in the expected format
        return CombinedResponseUpdate(
            meta_data=MetaDataUpdate(),
            response=db_artist,
        )


@router.patch("/{id}", response_model=CombinedResponsePatch[ArtistRead])
async def patch_artist(
    artist: ArtistPatch,
    id: int = Path(..., title="The ID of the artist to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_artist = await patch_item(session, id, artist, Artist, ArtistRead)
        if db_artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")

        # construct the response in the expected format
        return CombinedResponsePatch(
            meta_data=MetaDataPatch(),
            response=db_artist,
        )
