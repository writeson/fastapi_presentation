from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.playlists import crud as playlist_crud
from project.app.models.playlists import (
    PlaylistCreate,
    PlaylistRead,
    PlaylistUpdate,
    PlaylistPatch,
)


router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=PlaylistRead, status_code=status.HTTP_201_CREATED)
async def create_playlist(genre: PlaylistCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await playlist_crud.create_playlist(session=session, genre=genre)


@router.get("/", response_model=list[PlaylistRead])
async def read_playlists(
        offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await playlist_crud.read_playlists(
            session=session, offset=offset, limit=limit
        )


@router.get("/{id}", response_model=PlaylistRead)
async def read_playlist(
        id: int = Path(..., title="The ID of the genre to get"),
        db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_playlist = await playlist_crud.read_playlist(session=session, id=id)
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return db_playlist


@router.put("/{id}", response_model=PlaylistRead)
async def update_playlist(
        genre: PlaylistUpdate,
        id: int = Path(..., title="The ID of the playlist to update"),
        db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_playlist = await playlist_crud.update_playlist(
            session=session, id=id, genre=genre
        )
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return db_playlist


@router.patch("/{id}", response_model=PlaylistRead)
async def patch_playlist(
        genre: PlaylistPatch,
        id: int = Path(..., title="The ID of the playlist to patch"),
        db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_playlist = await playlist_crud.patch_playlist(
            session=session, id=id, genre=genre
        )
        if db_playlist is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return db_playlist
