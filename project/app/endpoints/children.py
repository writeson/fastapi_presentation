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
        "Artist": {
            "Album": _child_album_handler
        }
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
        Retrieve an Artist the database with an paginated
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
            count_query = select(func.count()).select_from(Album)
            total_count = await session.scalar(count_query)
        
            albums = [AlbumRead.model_validate(db_album) for db_album in db_albums]
            
            return CombinedResponseReadAll(
                response=albums,
                total_count=total_count,
            )




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
