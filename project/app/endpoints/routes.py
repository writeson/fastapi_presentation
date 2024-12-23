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
    """
    This function builds all the CRUD routes for the passed
    in model (artist, albums, etc.). It creates a router for
    all the CRUD routes, and passes that and the model to
    functions to create the different routes.

    :params ModuleType: the module containing the model definitions
    :params List[ModuleType]: the list of modules containing child model definitions
    :returns APIRouter: a populated router FastAPI will handle
    """
    # takes advantage of the plural/singular naming conventions
    prefix, _, _ = get_model_names(model)
    tags = prefix.title().replace("_", " ")

    # create a router for the model
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
    }
    create_item_route(**params)
    get_items_route(**params)
    get_item_route(**params)
    update_item_route(**params)
    patch_item_route(**params)

    # add the child modules for the specialized children routes
    params.update({"child_models": child_models})
    children.get_routes(**params)
    return router


def create_item_route(
    router: APIRouter,
    model: ModuleType,
):
    """
    Create the generic create item route in the router parameter for
    the model parameter
    """
    # takes advantage of the plural/singular naming conventions
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
        """
        The generic create item (class_name) for the route

        :params data: the Create sqlmodel definition
        :db AsyncSession: the asynchronous database session to use
        """
        async with db as session:
            db_item = await crud.create_item(
                session=session,
                data=data,
                model_class=getattr(model, f"{class_name}"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"{class_name} creation failed",
                )
            return CombinedResponseCreate(
                meta_data=MetaDataCreate(),
                response=db_item,
            )


def get_items_route(
    router: APIRouter,
    model: ModuleType,
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
                model_class=getattr(model, f"{class_name}"),
            )
            return CombinedResponseReadAll(
                response=items,
                total_count=total_count,
            )


def get_item_route(
    router: APIRouter,
    model: ModuleType,
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
                model_class=getattr(model, f"{class_name}"),
            )
            if db_item is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{class_name} not found",
                )
            item_read = getattr(model, f"{class_name}Read")
            return CombinedResponseRead(response=item_read.model_validate(db_item))


def update_item_route(
    router: APIRouter,
    model: ModuleType,
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
                model_class=getattr(model, f"{class_name}"),
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
                model_class=getattr(model, f"{class_name}"),
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


def get_model_names(model: ModuleType) -> Tuple[str, str, str]:
    """
    Returns the prefix, singular version of the prefix and the class_name for the model

    :params model: the model module to get the names from
    :returns: Tuple[str, str, str] containing the prefix, singular version of the prefix and the class
    name for the model
    """
    model_name = model.__name__.split(".")[-1].lower()
    prefix = model_name
    prefix_singular = prefix.rstrip("s")
    class_name = prefix_singular.title().replace("_", "")
    return prefix, prefix_singular, class_name
