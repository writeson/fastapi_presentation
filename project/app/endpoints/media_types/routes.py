from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.media_types import crud as media_type_crud
from project.app.models.media_types import (
    MediaTypeCreate,
    MediaTypeRead,
    MediaTypeUpdate,
    MediaTypePatch,
)


router = APIRouter(
    prefix="/media_types",
    tags=["Media Types"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=MediaTypeRead, status_code=status.HTTP_201_CREATED)
async def create_media_type(
    media_type: MediaTypeCreate, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await media_type_crud.create_media_type(
            session=session, media_type=media_type
        )


@router.get("/", response_model=list[MediaTypeRead])
async def read_media_types(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await media_type_crud.read_media_types(
            session=session, offset=offset, limit=limit
        )


@router.get("/{id}", response_model=MediaTypeRead)
async def read_media_type(
    id: int = Path(..., title="The ID of the media type to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_media_type = await media_type_crud.read_media_type(session=session, id=id)
        if db_media_type is None:
            raise HTTPException(status_code=404, detail="Media type not found")
        return db_media_type


@router.put("/{id}", response_model=MediaTypeRead)
async def update_media_type(
    media_type: MediaTypeUpdate,
    id: int = Path(..., title="The ID of the media type to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_media_type = await media_type_crud.update_media_type(
            session=session, id=id, media_type=media_type
        )
        if db_media_type is None:
            raise HTTPException(status_code=404, detail="Media type not found")
        return db_media_type


@router.patch("/{id}", response_model=MediaTypeRead)
async def patch_media_type(
    media_type: MediaTypePatch,
    id: int = Path(..., title="The ID of the media type to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_media_type = await media_type_crud.patch_media_type(
            session=session, id=id, media_type=media_type
        )
        if db_media_type is None:
            raise HTTPException(status_code=404, detail="Media type not found")
        return db_media_type
