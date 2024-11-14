from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.customers import (
    Customer,
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
    CustomerPatch,
)


async def create_customer(session: AsyncSession, customer: CustomerCreate) -> CustomerRead:
    """
    Create a new Customer in the database from the passed in CustomerCreate model.
    Returns the created CustomerRead model.
    """
    db_customer = Customer(title=customer.title)
    session.add(db_customer)
    await session.commit()
    await session.refresh(db_customer)
    return CustomerRead.model_validate(db_customer)


async def read_customer(session: AsyncSession, id: int) -> CustomerRead:
    """
    Retrieve a Customer from the database by ID.
    Returns the CustomerRead model if found, None otherwise.
    """
    query = (
        select(Customer)
        .where(Customer.id == id)
    )
    result = await session.execute(query)
    db_customer = result.unique().scalar_one_or_none()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


async def read_customers(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[CustomerRead]:
    """
    Retrieve all Customer from the database.
    Returns a list of CustomerRead models.
    """
    query = (
        select(Customer)
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(query)
    db_customers = result.scalars().all()
    return [CustomerRead.model_validate(db_customer) for db_customer in db_customers]


async def update_customer(session: AsyncSession, id: int, album: CustomerUpdate) -> CustomerRead:
    """
    Update an existing Customer in the database using the passed in CustomerUpdate model.
    Returns the updated CustomerRead model if found, None otherwise.
    """
    db_customer = await read_customer(session, id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in album.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)

    await session.commit()
    await session.refresh(db_customer)
    return CustomerRead.model_validate(db_customer)


async def patch_customer(session: AsyncSession, id: int, album: CustomerPatch) -> CustomerRead:
    """
    Partially update an existing Customer in the database using the passed in CustomerPatch model.
    Returns the updated CustomerRead model if found, None otherwise.
    """
    db_customer = await read_customer(session, id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in album.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_customer, key, value)

    await session.commit()
    await session.refresh(db_customer)
    return CustomerRead.model_validate(db_customer)
