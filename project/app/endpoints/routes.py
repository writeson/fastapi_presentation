from typing import List, Tuple, TypeVar
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
from project.app.endpoints import children


# Create some generic types to use in the code that follows
InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


def build_routes(
    model: ModuleType,
    child_models: List[ModuleType],
) -> APIRouter:
    prefix, _, _ = get_model_names(model)
    tags = prefix.title().replace("_", " ")

    router = APIRouter(
        prefix=f"/{prefix}",
        tags=[f"{tags}"],
        responses={404: {"description": "Not found"}},
        dependencies=[Depends(get_db)],
    )
    # create the endpoint routes
    params = {
        "router": router,
        "model": model,
        "child_models": child_models,
    }
    create_item_route(**params)
    get_items_route(**params)
    get_item_route(**params)
    children.get_routes(**params)
    # get_item_children_route(**params)
    update_item_route(**params)
    patch_item_route(**params)
    return router


def create_item_route(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
):
    """
    Create the generic create item route
    """
    prefix, prefix_singular, class_name = get_model_names(model)

    @router.post(
        "/",
        response_model=CombinedResponseCreate[getattr(model, f"{class_name}Read")],
        status_code=status.HTTP_201_CREATED,
    )
    async def create_item(
        data: getattr(model, f"{class_name}Create"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.create_item(
                session=session,
                data=data,
                input_class=getattr(model, f"{class_name}"),
                output_class=getattr(model, f"{class_name}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"{class_name} already exists",
                )
            return CombinedResponseCreate(
                meta_data=MetaDataCreate(),
                response=db_item,
            )


def get_items_route(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
):
    """
    Create the generic get item route
    """
    prefix, prefix_singular, class_name = get_model_names(model)

    @router.get(
        "/",
        response_model=CombinedResponseReadAll[
            List[getattr(model, f"{class_name}Read")], int
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
                input_class=getattr(model, f"{class_name}"),
                output_class=getattr(model, f"{class_name}Read"),
            )
            return CombinedResponseReadAll(
                response=items,
                total_count=total_count,
            )


def get_item_route(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
):
    """
    Create the generic get item route
    """
    prefix, prefix_singular, class_name = get_model_names(model)

    @router.get(
        "/{id}",
        response_model=CombinedResponseRead[getattr(model, f"{class_name}Read")],
    )
    async def read_item(
        id: int = Path(..., title=f"The ID of the {prefix} to get"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.read_item(
                session=session,
                id=id,
                input_class=getattr(model, f"{class_name}"),
                output_class=getattr(model, f"{class_name}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{class_name} not found",
                )
            item_read = getattr(model, f"{class_name}Read")
            return CombinedResponseRead(response=item_read.model_validate(db_item))


def get_item_children_route_1(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
):
    prefix, prefix_singular, class_name = get_model_names(model)

    # Build children routes
    for child_model in child_models:
        parent_class = getattr(model, f"{class_name}")
        child_prefix = child_model.__name__.split(".")[-1]
        child_local_prefix = child_prefix[:-1]

        _, _, child_class_name = get_model_names(child_model)
        child_class = getattr(child_model, f"{child_class_name}")
        child_read_class = getattr(child_model, f"{child_class_name}Read")

        # Add the route with the factory-created function
        route_handler = create_child_route(
            parent_class,
            child_class,
            child_read_class,
            child_prefix,
            child_local_prefix,
        )
        router.add_api_route(
            path=f"/{{id}}/{child_prefix}",
            endpoint=route_handler,
            response_model=CombinedResponseReadAll[List[child_read_class], int],
            methods=["GET"],
        )


def update_item_route(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
):
    prefix, prefix_singular, class_name = get_model_names(model)

    @router.put(
        "/{id}",
        response_model=CombinedResponseUpdate[getattr(model, f"{class_name}Read")],
    )
    async def update_item(
        data: getattr(model, f"{class_name}Update"),
        id: int = Path(..., title=f"The ID of the {prefix} to update"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.update_item(
                session=session,
                id=id,
                data=data,
                input_class=getattr(model, f"{class_name}"),
                output_class=getattr(model, f"{class_name}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{class_name} not found",
                )

            # construct the response in the expected format
            return CombinedResponseUpdate(
                meta_data=MetaDataUpdate(),
                response=db_item,
            )


def patch_item_route(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
):
    prefix, prefix_singular, class_name = get_model_names(model)

    @router.patch(
        "/{id}",
        response_model=CombinedResponsePatch[getattr(model, f"{class_name}Read")],
    )
    async def patch_artist(
        data: getattr(model, f"{class_name}Patch"),
        id: int = Path(..., title=f"The ID of the {prefix} to patch"),
        db: AsyncSession = Depends(get_db),
    ):
        async with db as session:
            db_item = await crud.patch_item(
                session=session,
                id=id,
                data=data,
                input_class=getattr(model, f"{class_name}Read"),
                output_class=getattr(model, f"{class_name}Read"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{class_name} not found",
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
    raise ValueError(
        f"No relationship found between {parent_class.__name__} and {child_class.__name__}"
    )


def get_model_names(model: ModuleType) -> Tuple[str]:
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
    return prefix, prefix_singular, class_name
