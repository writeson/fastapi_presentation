from typing import List, Tuple, TypeVar
from types import ModuleType

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints import crud
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
from project.app.models.albums import Album, AlbumRead
from project.app.models.tracks import Track, TrackRead
from project.app.models.playlists import Playlist, PlaylistRead
from project.app.models.media_types import MediaType, MediaTypeRead
from project.app.models.genres import Genre, GenreRead
from project.app.models.invoice_items import InvoiceItem, InvoiceItemRead






def get_routes(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
) -> None:
    """
    iterate through the child models and build the specific routes for each model

    :params router: the router to add the routes to
    :params model: the model to build the routes for
    :params child_models: the child models to build the routes for
    """""
    route_handlers = {
        "Artist": {"Album": _child_album_handler},
        "Album": {"Track": _child_track_handler},
        "Track": {"InvoiceItem": _child_invoice_item_handler},
    }
    # iterate through the child models
    for child_model in child_models:
        class_name = get_model_class_name(model)
        child_class_name = get_model_class_name(child_model)
        
        # create the child route
        route_handler_func = route_handlers.get(class_name, {}).get(child_class_name, None)
        if route_handler_func is not None:
            route_handler_func(router)
    

def _child_album_handler(router: APIRouter):
    @router.get(
        path="/{id}/albums",
        response_model=CombinedResponseReadAll[List[AlbumRead], int],
    )
    async def read_artist_albums(
        id: int, offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
    ) -> [List[AlbumRead], int]:
        """
        Retrieve an Artist the database with a paginated
        list of associated albums
        """
        async with db as session:
            query = (
                select(Album)
                .where(Album.artist_id == id)
                .order_by(Album.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_albums = result.scalars().all()
            if db_albums is None:
                raise HTTPException(status_code=404, detail="Albums not found")
            
            # Query for total count of albums
            count_query = (
                select(func.count(Album.id))
                .where(Album.artist_id == id)
            )
            total_count = await session.scalar(count_query)
        
            albums = [AlbumRead.model_validate(db_album) for db_album in db_albums]
            
            return CombinedResponseReadAll(
                response=albums,
                total_count=total_count,
            )


def _child_track_handler(router: APIRouter):
    @router.get(
        path="/{id}/tracks",
        response_model=CombinedResponseReadAll[List[TrackRead], int],
    )
    async def read_album_tracks(
            id: int, offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
    ) -> [List[TrackRead], int]:
        """
        Retrieve an Album the database with a paginated
        list of associated albums
        """
        async with db as session:
            query = (
                select(Track)
                .where(Track.album_id == id)
                .order_by(Track.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_tracks = result.scalars().all()
            if db_tracks is None:
                raise HTTPException(status_code=404, detail="Tracks not found")

            # Query for total count of tracks
            count_query = (
                select(func.count(Track.id))
                .where(Track.album_id == id)
            )
            total_count = await session.scalar(count_query)

            tracks = [TrackRead.model_validate(db_track) for db_track in db_tracks]

            return CombinedResponseReadAll(
                response=tracks,
                total_count=total_count,
            )


def _child_invoice_item_handler(router: APIRouter):
    @router.get(
        path="/{id}/invoice_items",
        response_model=CombinedResponseReadAll[List[InvoiceItemRead], int],
    )
    async def read_track_invoice_items(
            id: int, offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
    ) -> [List[InvoiceItemRead], int]:
        """
        Retrieve a Track from the database with a paginated
        list of associated invoice items
        """
        async with db as session:
            query = (
                select(InvoiceItem)
                .where(InvoiceItem.track_id == id)
                .order_by(InvoiceItem.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_invoice_items = result.scalars().all()
            if db_invoice_items is None:
                raise HTTPException(status_code=404, detail="Invoice items not found")

            # Query for total count of invoice items
            count_query = (
                select(func.count(InvoiceItem.id))
                .where(InvoiceItem.track_id == id)
            )
            total_count = await session.scalar(count_query)

            invoice_items = [InvoiceItemRead.model_validate(db_invoice_item) for db_invoice_item in db_invoice_items]

            return CombinedResponseReadAll(
                response=invoice_items,
                total_count=total_count,
            )


# def _child_media_type_handler(router: APIRouter):
#     @router.get(
#         path="/{id}/media_types",
#         response_model=CombinedResponseReadAll[List[MediaTypeRead], int],
#     )
#     async def read_media_types(
#             id: int, offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
#     ) -> [List[MediaTypeRead], int]:
#         """
#         Retrieve a Track the database with a paginated
#         list of associated media types
#         """
#         async with db as session:
#             query = (
#                 select(MediaType)
#                 .where(MediaType.track_id == id)
#                 .order_by(MediaType.id)
#                 .offset(offset)
#                 .limit(limit)
#             )
#             # Execute the query
#             result = await session.execute(query)
#             db_media_types = result.scalars().all()
#             if db_media_types is None:
#                 raise HTTPException(status_code=404, detail="Media types not found")
# 
#             # Query for total count of media types
#             count_query = (
#                 select(func.count(MediaType.id))
#                 .where(MediaType.track_id == id)
#             )
#             total_count = await session.scalar(count_query)
# 
#             media_types = [TrackRead.model_validate(db_media_type) for db_media_type in db_media_types]
# 
#             return CombinedResponseReadAll(
#                 response=media_types,
#                 total_count=total_count,
#             )
# 
# 
# def _child_genre_handler(router: APIRouter):
#     @router.get(
#         path="/{id}/genres",
#         response_model=CombinedResponseReadAll[List[GenreRead], int],
#     )
#     async def read_track_genres(
#             id: int, offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
#     ) -> [List[GenreRead], int]:
#         """
#         Retrieve a Track the database with a paginated
#         list of associated genres
#         """
#         async with db as session:
#             query = (
#                 select(Genre)
#                 .where(Genre.track_id == id)
#                 .order_by(Genre.id)
#                 .offset(offset)
#                 .limit(limit)
#             )
#             # Execute the query
#             result = await session.execute(query)
#             db_genres = result.scalars().all()
#             if db_genres is None:
#                 raise HTTPException(status_code=404, detail="Genres not found")
# 
#             # Query for total count of tracks
#             count_query = (
#                 select(func.count(Genre.id))
#                 .where(Genre.track_id == id)
#             )
#             total_count = await session.scalar(count_query)
# 
#             genres = [TrackRead.model_validate(db_genre) for db_genre in db_genres]
# 
#             return CombinedResponseReadAll(
#                 response=genres,
#                 total_count=total_count,
#             )


def get_model_class_name(model: ModuleType) -> Tuple[str]:
    """
    Returns the prefix, singular version of the prefix and the tags for the model

    :params model: the model module to get the names from
    :returns: Tuple[str] containing the prefix, singular version of the prefix and the class
    name for the model
    """
    model_name = model.__name__.split(".")[-1].lower()
    prefix = model_name
    prefix_singular = prefix.rstrip("s")
    class_name = prefix_singular.title().replace("_", "")
    return class_name
