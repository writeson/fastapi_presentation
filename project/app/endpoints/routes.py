from typing import List, TypeVar, Any
from types import ModuleType

from fastapi import APIRouter, Depends, Path, status, HTTPException
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


# Create some generic types to use in the code that follows
InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


def build_routes(
    prefix: str,
    tags: str,
    module: ModuleType,
    children_modules: List[ModuleType],
) -> APIRouter:
    router = APIRouter(
        prefix=f"/{prefix}",
        tags=[f"{tags}"],
        responses={404: {"description": "Not found"}},
        dependencies=[Depends(get_db)],
    )
    # Modify the prefix to be the singular version
    prefix = prefix[:-1]
    
    params = {
        "router": router,
        "prefix": prefix,
        "tags": tags,
        "module": module,
        "children_modules": children_modules,
    }

    create_item_route(**params)
    get_items_route(**params)
    get_item_route(**params)
    get_item_children_route(**params)
    update_item_route(**params)
    patch_item_route(**params)
    return router


def create_item_route(
        router: APIRouter, 
        prefix: str, 
        tags: str,
        module: ModuleType,
        children_modules: List[ModuleType],
):
    """
    Create the generic create item route
    """
    @router.post(
        "/",
        response_model=CombinedResponseCreate[
            getattr(module, f"{prefix.title().replace("_", "")}Read")
        ],
        status_code=status.HTTP_201_CREATED,
    )
    async def create_item(
        data: getattr(module, f"{prefix.title().replace("_", "")}Create"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.create_item(
                session=session,
                data=data,
                input_class=getattr(module, f"{prefix.title().replace("_", "")}"),
                output_class=getattr(module, f"{prefix.title().replace("_", "")}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"{prefix.title().replace("_", "")} already exists",
                )
            return CombinedResponseCreate(
                meta_data=MetaDataCreate(),
                response=db_item,
            )

def get_items_route(
        router: APIRouter,
        prefix: str,
        tags: str,
        module: ModuleType,
        children_modules: List[ModuleType],
):
    """
    Create the generic get item route
    """
    @router.get(
        "/",
        response_model=CombinedResponseReadAll[
            List[getattr(module, f"{prefix.title().replace("_", "")}Read")], int
        ],
    )
    async def read_items(
        offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
    ):
        async with db as session:
            items, total_count = await crud.read_items(
                session=session,
                offset=offset,
                limit=limit,
                input_class=getattr(module, f"{prefix.title().replace("_", "")}"),
                output_class=getattr(module, f"{prefix.title().replace("_", "")}Read"),
            )
            return CombinedResponseReadAll(
                response=items,
                total_count=total_count,
            )


def get_item_route(
        router: APIRouter,
        prefix: str,
        tags: str,
        module: ModuleType,
        children_modules: List[ModuleType],
):
    """
    Create the generic get item route
    """
    @router.get(
        "/{id}",
        response_model=CombinedResponseRead[
            getattr(module, f"{prefix.title().replace("_", "")}Read")
        ],
    )
    async def read_item(
        id: int = Path(..., title=f"The ID of the {prefix} to get"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.read_item(
                session=session,
                id=id,
                input_class=getattr(module, f"{prefix.title().replace("_", "")}"),
                output_class=getattr(module, f"{prefix.title().replace("_", "")}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{prefix.title().replace("_", "")} not found",
                )
            item_read = getattr(module, f"{prefix.title().replace("_", "")}Read")
            return CombinedResponseRead(response=item_read.model_validate(db_item))


def get_item_children_route(
        router: APIRouter,
        prefix: str,
        tags: str,
        module: ModuleType,
        children_modules: List[ModuleType],
):
    # Build children routes
    for child_module in children_modules:
        parent_class = getattr(module, f"{prefix.title().replace("_", "")}")
        child_prefix = child_module.__name__.split(".")[-1]
        child_local_prefix = child_prefix[:-1]
        child_class = getattr(child_module, f"{child_local_prefix.title().replace("_", "")}")
        child_read_class = getattr(
            child_module, f"{child_local_prefix.title().replace("_", "")}Read"
        )
        relationship_name = get_relationship_name(parent_class, child_class)

        # Add the route with the factory-created function
        route_handler = create_child_route(
            parent_class,
            child_class,
            child_read_class,
            child_prefix,
            child_local_prefix,
            relationship_name
        )
        router.add_api_route(
            path=f"/{{id}}/{child_prefix}",
            endpoint=route_handler,
            tags=[tags],
            response_model=CombinedResponseReadAll[List[child_read_class], int],
            methods=["GET"],
        )
        
        
def update_item_route(
        router: APIRouter,
        prefix: str,
        tags: str,
        module: ModuleType,
        children_modules: List[ModuleType],
):
    @router.put(
        "/{id}",
        response_model=CombinedResponseUpdate[
            getattr(module, f"{prefix.title().replace("_", "")}Read")
        ],
    )
    async def update_item(
        data: getattr(module, f"{prefix.title().replace("_", "")}Update"),
        id: int = Path(..., title=f"The ID of the {prefix} to update"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.update_item(
                session=session,
                id=id,
                data=data,
                input_class=getattr(module, f"{prefix.title().replace("_", "")}"),
                output_class=getattr(module, f"{prefix.title().replace("_", "")}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{prefix.title().replace("_", "")} not found",
                )

            # construct the response in the expected format
            return CombinedResponseUpdate(
                meta_data=MetaDataUpdate(),
                response=db_item,
            )

def patch_item_route(
        router: APIRouter,
        prefix: str,
        tags: str,
        module: ModuleType,
        children_modules: List[ModuleType],
):
    @router.patch(
        "/{id}",
        response_model=CombinedResponsePatch[
            getattr(module, f"{prefix.title().replace("_", "")}Read")
        ],
    )
    async def patch_artist(
        data: getattr(module, f"{prefix.title().replace("_", "")}Patch"),
        id: int = Path(..., title=f"The ID of the {prefix} to patch"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.patch_item(
                session=session,
                id=id,
                data=data,
                input_class=getattr(module, f"{prefix.title().replace("_", "")}Read"),
                output_class=getattr(module, f"{prefix.title().replace("_", "")}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{prefix.title().replace("_", "")} not found",
                )

            # construct the response in the expected format
            return CombinedResponsePatch(
                meta_data=MetaDataPatch(),
                response=db_item,
            )


def create_child_route(
        parent_class, 
        child_class, 
        child_read_class, 
        child_prefix: str, 
        child_local_prefix: str,
        relationship_name: str,
):
    async def read_item_children(
            id: int = Path(..., title=f"The ID of the {child_local_prefix} to get"),
            offset: int = 0,
            limit: int = 10,
            db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            children, total_count = await crud.read_children_items(
                session=session,
                parent_id=id,
                offset=offset,
                limit=limit,
                parent_class=parent_class,
                input_class=child_class,
                output_class=child_read_class,
                relationship_name=relationship_name,
            )
            return CombinedResponseReadAll(
                response=children,
                total_count=total_count,
            )
    return read_item_children


def get_relationship_name(parent_class, child_class):
    """
    Get the relationship name between two classes.
    """
    for relationship in parent_class.__mapper__.relationships:
        if relationship.mapper.class_ == child_class:
            return relationship.key
    raise ValueError(f"No relationship found between {parent_class.__name__} and {child_class.__name__}")
