from project.app.models.invoice_items import (
    InvoiceItemCreate,
    InvoiceItemRead,
    InvoiceItemUpdate,
    InvoiceItemPatch,
)
from project.app.database import get_db
from project.app.endpoints.invoice_items import crud as invoice_item_crud

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/invoice_items",
    tags=["InvoiceItems"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=InvoiceItemRead, status_code=status.HTTP_201_CREATED)
async def create_invoice_item(
    invoice_item: InvoiceItemCreate, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await invoice_item_crud.create_invoice_item(
            session=session, invoice_item=invoice_item
        )


@router.get("/", response_model=list[InvoiceItemRead])
async def read_invoice_items(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await invoice_item_crud.read_invoice_items(
            session=session, offset=offset, limit=limit
        )


@router.get("/{id}", response_model=InvoiceItemRead)
async def read_invoice_item(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_invoice_item = await invoice_item_crud.read_invoice_item(
            session=session, id=id
        )
        if db_invoice_item is None:
            raise HTTPException(status_code=404, detail="InvoiceItem not found")
        return db_invoice_item


@router.put("/{id}", response_model=InvoiceItemRead)
async def update_invoice_item(
    invoice_item: InvoiceItemUpdate,
    id: int = Path(..., title="The ID of the invoice_item to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_invoice_item = await invoice_item_crud.update_invoice_item(
            session=session, id=id, invoice_item=invoice_item
        )
        if db_invoice_item is None:
            raise HTTPException(status_code=404, detail="InvoiceItem not found")
        return db_invoice_item


@router.patch("/{id}", response_model=InvoiceItemRead)
async def patch_invoice_item(
    invoice_item: InvoiceItemPatch,
    id: int = Path(..., title="The ID of the invoice_item to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_invoice_item = await invoice_item_crud.patch_invoice_item(
            session=session, id=id, invoice_item=invoice_item
        )
        if db_invoice_item is None:
            raise HTTPException(status_code=404, detail="InvoiceItem not found")
        return db_invoice_item
