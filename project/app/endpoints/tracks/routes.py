from project.app.models.tracks import (
    TrackCreate,
    TrackRead,
    TrackUpdate,
    TrackPatch,
)
from project.app.database import  get_db
from project.app.endpoints.tracks import crud as track_crud

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/tracks",
    tags=["Tracks"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=TrackRead, status_code=status.HTTP_201_CREATED)
async def create_track(track: TrackCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await track_crud.create_track(session=session, track=track)


@router.get("/", response_model=list[TrackRead])
async def read_tracks(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await track_crud.read_tracks(session=session, offset=offset, limit=limit)


@router.get("/{id}", response_model=TrackRead)
async def read_track(id: int = Path(..., title="The ID of the artist to get"), db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_track = await track_crud.read_track(session=session, id=id)
        if db_track is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_track


@router.put("/{id}", response_model=TrackRead)
async def update_track(
    track: TrackUpdate,
    id: int = Path(..., title="The ID of the track to update"),
    db: AsyncSession = Depends(get_db)
):
    async with db as session:
        db_track = await track_crud.update_track(session=session, id=id, track=track)
        if db_track is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_track

@router.patch("/{id}", response_model=TrackRead)
async def patch_track(
    track: TrackPatch,
    id: int = Path(..., title="The ID of the track to patch"),
    db: AsyncSession = Depends(get_db)
):
    async with db as session:
        db_track = await track_crud.patch_track(session=session, id=id, track=track)
        if db_track is None:
            raise HTTPException(status_code=404, detail="Track not found")
        return db_track