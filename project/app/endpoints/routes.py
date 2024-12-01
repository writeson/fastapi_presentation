from typing import List, TypeVar
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

    # Build create item route
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

    # Build read items route
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

    # Build children routes
    for child_module in children_modules:
        full_prefix = child_module.__name__.split(".")[-1]
        local_prefix = full_prefix[:-1]
        child_class = getattr(child_module, f"{local_prefix.title().replace("_", "")}")
        child_read_class = getattr(
            child_module, f"{local_prefix.title().replace("_", "")}Read"
        )

        @router.get(
            f"/{{id}}/{full_prefix}",
            response_model=CombinedResponseReadAll[List[child_read_class], int],
        )
        async def read_item_children(
            id: int = Path(..., title=f"The ID of the {local_prefix} to get"),
            offset: int = 0,
            limit: int = 10,
            db: AsyncSession = Depends(get_db),
        ):
            async with db as session:
                children, total_count = await crud.read_items(
                    session=session,
                    offset=offset,
                    limit=limit,
                    input_class=child_class,
                    output_class=child_read_class,
                )
                return CombinedResponseReadAll(
                    response=children,
                    total_count=total_count,
                )

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

    return router
