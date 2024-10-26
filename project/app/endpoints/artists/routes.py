from project.app.models.artists import (
    ArtistCreate,
    ArtistRead,
    ArtistUpdate,
    ArtistPatch,
)
from project.app.database import  get_db
from project.app.endpoints.artists import crud as artist_crud

from fastapi import APIRouter, Depends, Path, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/artists/", response_model=ArtistRead, status_code=status.HTTP_201_CREATED)
async def create_artist(artist: ArtistCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await artist_crud.create_artist(session=session, artist=artist)
    
    
    # with Session(engine) as session:
    #     db_artist = ArtistCreate(name=artist.name)
    #     session.add(db_artist)
    #     session.commit()
    #     session.refresh(db_artist)
    #     return db_artist

# @router.get("/artists/{artist_id}", response_model=ArtistRead)
# def read_artist(artist_id: int):
#     with Session(engine) as session:
#         artist = session.get(ArtistsRead, artist_id)
#         if not artist:
#             raise HTTPException(status_code=404, detail="Artist not found")
#         return artist
# 
# @router.put("/artists/{artist_id}", response_model=ArtistRead)
# def update_artist(artist_id: int, artist: ArtistUpdate):
#     with Session(engine) as session:
#         db_artist = session.get(ArtistsBase, artist_id)
#         if not db_artist:
#             raise HTTPException(status_code=404, detail="Artist not found")
#         artist_data = artist.dict()
#         for key, value in artist_data.items():
#             setattr(db_artist, key, value)
#         session.add(db_artist)
#         session.commit()
#         session.refresh(db_artist)
#         return db_artist
# 
# @router.patch("/artists/{artist_id}", response_model=ArtistRead)
# def patch_artist(artist_id: int, artist: ArtistPatch):
#     with Session(engine) as session:
#         db_artist = session.get(ArtistsBase, artist_id)
#         if not db_artist:
#             raise HTTPException(status_code=404, detail="Artist not found")
#         artist_data = artist.dict(exclude_unset=True)
#         for key, value in artist_data.items():
#             setattr(db_artist, key, value)
#         session.add(db_artist)
#         session.commit()
#         session.refresh(db_artist)
#         return db_artist
