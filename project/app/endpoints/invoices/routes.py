from project.app.models.invoices import (
    Invoice,  # noqa: F401
    InvoiceCreate,
    InvoiceRead,
    InvoiceUpdate,
    InvoicePatch,
)
from project.app.database import get_db
from project.app.endpoints.invoices import crud as invoice_crud

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
async def create_invoice(track: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await invoice_crud.create_invoice(session=session, track=track)


@router.get("/", response_model=list[InvoiceRead])
async def read_invoices(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await invoice_crud.read_invoices(
            session=session, offset=offset, limit=limit
        )


@router.get("/{id}", response_model=InvoiceRead)
async def read_invoice(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_invoice = await invoice_crud.read_invoice(session=session, id=id)
        if db_invoice is None:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return db_invoice


@router.put("/{id}", response_model=InvoiceRead)
async def update_invoice(
    track: InvoiceUpdate,
    id: int = Path(..., title="The ID of the track to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_invoice = await invoice_crud.update_invoice(
            session=session, id=id, track=track
        )
        if db_invoice is None:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return db_invoice


@router.patch("/{id}", response_model=InvoiceRead)
async def patch_invoice(
    track: InvoicePatch,
    id: int = Path(..., title="The ID of the track to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_invoice = await invoice_crud.patch_invoice(
            session=session, id=id, track=track
        )
        if db_invoice is None:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return db_invoice
