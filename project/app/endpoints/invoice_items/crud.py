from fastapi import HTTPException
from sqlalchemy import select

# from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.invoice_items import (
    InvoiceItem,
    InvoiceItemCreate,
    InvoiceItemRead,
    InvoiceItemUpdate,
    InvoiceItemPatch,
)


async def create_invoice_item(
    session: AsyncSession, invoice_item: InvoiceItemCreate
) -> InvoiceItemRead:
    """
    Create a new InvoiceItem in the database from the passed in InvoiceItemCreate model.
    Returns the created InvoiceItemRead model.
    """
    db_invoice_item = InvoiceItem(title=invoice_item.title)
    session.add(db_invoice_item)
    await session.commit()
    await session.refresh(db_invoice_item)
    return InvoiceItemRead.model_validate(db_invoice_item)


async def read_invoice_item(session: AsyncSession, id: int) -> InvoiceItemRead:
    """
    Retrieve a InvoiceItem from the database by ID.
    Returns the InvoiceItemRead model if found, None otherwise.
    """
    query = select(InvoiceItem).where(InvoiceItem.id == id)
    result = await session.execute(query)
    db_invoice_item = result.unique().scalar_one_or_none()
    if db_invoice_item is None:
        raise HTTPException(status_code=404, detail="Invoice item not found")
    return db_invoice_item


async def read_invoice_items(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[InvoiceItemRead]:
    """
    Retrieve all InvoiceItem from the database.
    Returns a list of InvoiceItemRead models.
    """
    query = select(InvoiceItem).offset(offset).limit(limit)
    result = await session.execute(query)
    db_invoice_items = result.scalars().all()
    return [
        InvoiceItemRead.model_validate(db_invoice_item)
        for db_invoice_item in db_invoice_items
    ]


async def update_invoice_item(
    session: AsyncSession, id: int, album: InvoiceItemUpdate
) -> InvoiceItemRead:
    """
    Update an existing InvoiceItem in the database using the passed in InvoiceItemUpdate model.
    Returns the updated InvoiceItemRead model if found, None otherwise.
    """
    db_invoice_item = await read_invoice_item(session, id)
    if db_invoice_item is None:
        raise HTTPException(status_code=404, detail="Invoice item not found")

    for key, value in album.dict(exclude_unset=True).items():
        setattr(db_invoice_item, key, value)

    await session.commit()
    await session.refresh(db_invoice_item)
    return InvoiceItemRead.model_validate(db_invoice_item)


async def patch_invoice_item(
    session: AsyncSession, id: int, album: InvoiceItemPatch
) -> InvoiceItemRead:
    """
    Partially update an existing InvoiceItem in the database using the passed in InvoiceItemPatch model.
    Returns the updated InvoiceItemRead model if found, None otherwise.
    """
    db_invoice_item = await read_invoice_item(session, id)
    if db_invoice_item is None:
        raise HTTPException(status_code=404, detail="InvoiceItem not found")

    for key, value in album.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_invoice_item, key, value)

    await session.commit()
    await session.refresh(db_invoice_item)
    return InvoiceItemRead.model_validate(db_invoice_item)
