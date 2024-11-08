from project.app.models.artists import (
    ArtistCreate,
    ArtistRead,
    ArtistReadWithAlbums,
    ArtistUpdate,
    ArtistPatch,
)
from project.app.database import get_db
from project.app.endpoints.artists import crud as artist_crud

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=ArtistRead, status_code=status.HTTP_201_CREATED)
async def create_artist(artist: ArtistCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await artist_crud.create_artist(session=session, artist=artist)


@router.get("/", response_model=list[ArtistRead])
async def read_artists(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await artist_crud.read_artists(
            session=session, offset=offset, limit=limit
        )


@router.get("/{id}", response_model=ArtistRead)
async def read_artist(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_artist = await artist_crud.read_artist(session=session, id=id)
        if db_artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")
        return db_artist


@router.get("/{id}/albums", response_model=ArtistReadWithAlbums)
async def read_artist_with_albums(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_artist = await artist_crud.read_artist_with_albums(session=session, id=id)
        if db_artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")
        return db_artist


@router.put("/{id}", response_model=ArtistRead)
async def update_artist(
    artist: ArtistUpdate,
    id: int = Path(..., title="The ID of the artist to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_artist = await artist_crud.update_artist(
            session=session, id=id, artist=artist
        )
        if db_artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")
        return db_artist


@router.patch("/{id}", response_model=ArtistRead)
async def patch_artist(
    artist: ArtistPatch,
    id: int = Path(..., title="The ID of the artist to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_artist = await artist_crud.patch_artist(
            session=session, id=id, artist=artist
        )
        if db_artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")
        return db_artist
