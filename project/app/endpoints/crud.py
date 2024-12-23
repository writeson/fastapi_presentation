"""
This module contains common crud operations
used by the routes. These use Python generic types
to support multiple response classes and multiple
input classes
"""

from typing import List, Type, TypeVar
import inspect

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


ParentType = TypeVar("ParentType")
InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


async def create_item(
    session: AsyncSession,
    data: InputType,
    model_class: Type[InputType],
) -> OutputType:
    """
    Create a new item in the database.
    Returns the created item as the same class.
    """
    if not inspect.isclass(model_class):
        raise ValueError("model_class must be class object")

    db_item = model_class(**data.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def read_items(
    session: AsyncSession,
    offset: int = 0,
    limit: int = 10,
    model_class: Type[InputType] = None,
) -> [List[OutputType], int]:
    """
    Retrieve a paginated list of items from the database.
    Returns a list of items as the same class.
    """
    if not inspect.isclass(model_class):
        raise ValueError("model_class must be class object")

    query = select(model_class).offset(offset).limit(limit)
    result = await session.execute(query)
    db_items = result.scalars().all()

    # Query for total count
    count_query = select(func.count()).select_from(model_class)
    total_count = await session.scalar(count_query)

    return [(db_item) for db_item in db_items], total_count


async def read_item(
    session: AsyncSession,
    id: int,
    model_class: Type[InputType],
) -> OutputType:
    """
    Retrieve an item from the database by ID.
    Returns the item as the same class if found, None otherwise.
    """
    if not inspect.isclass(model_class):
        raise ValueError("model_class must be class object")

    query = select(model_class).where(model_class.id == id)
    result = await session.execute(query)
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"{model_class} not found")
    return db_item


async def update_item(
    session: AsyncSession,
    id: int,
    data: InputType,
    model_class: Type[InputType],
) -> OutputType:
    """
    Update an existing item in the database using the passed in input class and output class.
    Returns the updated item as the same class if found, returns None otherwise.
    """
    if not inspect.isclass(model_class):
        raise ValueError("model_class must be class object")

    query = select(model_class).where(model_class.id == id)
    result = await session.execute(query)
    db_item = result.scalar_one_or_none()
    if db_item is None:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def patch_item(
    session: AsyncSession,
    id: int,
    data: InputType,
    model_class: Type[InputType],
) -> OutputType:
    """
    Partially update an existing item in the database using the passed in input class and output class.
    Returns the updated item as the same class if found, returns None otherwise.
    """
    if not inspect.isclass(model_class):
        raise ValueError("model_class must be class object")

    query = select(model_class).where(model_class.id == id)
    result = await session.execute(query)
    db_item = result.scalar_one_or_none()
    if db_item is None:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_item, key, value)

    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item
