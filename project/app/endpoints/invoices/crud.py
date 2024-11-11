from fastapi import HTTPException
from sqlalchemy import select

# from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.invoices import (
    Invoice,
    InvoiceCreate,
    InvoiceRead,
    InvoiceUpdate,
    InvoicePatch,
)


async def create_invoice(session: AsyncSession, album: InvoiceCreate) -> InvoiceRead:
    """
    Create a new Invoice in the database from the passed in InvoiceCreate model.
    Returns the created InvoiceRead model.
    """
    db_invoice = Invoice(title=album.title)
    session.add(db_invoice)
    await session.commit()
    await session.refresh(db_invoice)
    return InvoiceRead.model_validate(db_invoice)


async def read_invoice(session: AsyncSession, id: int) -> InvoiceRead:
    """
    Retrieve a Invoice from the database by ID.
    Returns the InvoiceRead model if found, None otherwise.
    """
    query = select(Invoice).where(Invoice.id == id)
    result = await session.execute(query)
    db_invoice = result.unique().scalar_one_or_none()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice


async def read_invoices(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[InvoiceRead]:
    """
    Retrieve all Invoice from the database.
    Returns a list of InvoiceRead models.
    """
    query = select(Invoice).offset(offset).limit(limit)
    result = await session.execute(query)
    db_invoices = result.scalars().all()
    return [InvoiceRead.model_validate(db_invoice) for db_invoice in db_invoices]


async def update_invoice(
    session: AsyncSession, id: int, album: InvoiceUpdate
) -> InvoiceRead:
    """
    Update an existing Invoice in the database using the passed in InvoiceUpdate model.
    Returns the updated InvoiceRead model if found, None otherwise.
    """
    db_invoice = await read_invoice(session, id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    for key, value in album.dict(exclude_unset=True).items():
        setattr(db_invoice, key, value)

    await session.commit()
    await session.refresh(db_invoice)
    return InvoiceRead.model_validate(db_invoice)


async def patch_invoice(
    session: AsyncSession, id: int, album: InvoicePatch
) -> InvoiceRead:
    """
    Partially update an existing Invoice in the database using the passed in InvoicePatch model.
    Returns the updated InvoiceRead model if found, None otherwise.
    """
    db_invoice = await read_invoice(session, id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    for key, value in album.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_invoice, key, value)

    await session.commit()
    await session.refresh(db_invoice)
    return InvoiceRead.model_validate(db_invoice)
