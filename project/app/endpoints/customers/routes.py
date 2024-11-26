from typing import List

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.customers import crud as customer_crud
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
from project.app.models.customers import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
    CustomerPatch,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post(
    "/",
    response_model=CombinedResponseCreate[CustomerRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_customer = await customer_crud.create_customer(
            session=session, customer=customer
        )

        # construct the response in the expected format
        return CombinedResponseCreate(
            meta_data=MetaDataCreate(),
            response=db_customer,
        )


@router.get("/", response_model=CombinedResponseReadAll[List[CustomerRead], int])
async def read_customers(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        customers, total_count = await customer_crud.read_customers(
            session=session, offset=offset, limit=limit
        )
        return CombinedResponseReadAll(
            response=customers,
            total_count=total_count,
        )


@router.get("/{id}", response_model=CombinedResponseRead[CustomerRead])
async def read_customer(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_customer = await customer_crud.read_customer(session=session, id=id)
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return CombinedResponseRead(response=CustomerRead.model_validate(db_customer))


# @router.get("/{id}/invoices", response_model=CustomerRead)
# async def read_customer(
#         id: int = Path(..., title="The ID of the artist to get"),
#         db: AsyncSession = Depends(get_db),
# ):
#     async with db as session:
#         db_customer = await customer_crud.read_customer(session=session, id=id)
#         if db_customer is None:
#             raise HTTPException(status_code=404, detail="Customer not found")
#         return db_customer


@router.put("/{id}", response_model=CombinedResponseUpdate[CustomerRead])
async def update_customer(
    customer: CustomerUpdate,
    id: int = Path(..., title="The ID of the customer to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_customer = await customer_crud.update_customer(
            session=session, id=id, customer=customer
        )
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # construct the response in the expected format
        return CombinedResponseUpdate(
            meta_data=MetaDataUpdate(),
            response=db_customer,
        )


@router.patch("/{id}", response_model=CombinedResponsePatch[CustomerRead])
async def patch_customer(
    customer: CustomerPatch,
    id: int = Path(..., title="The ID of the customer to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_customer = await customer_crud.patch_customer(
            session=session, id=id, customer=customer
        )
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # construct the response in the expected format
        return CombinedResponsePatch(
            meta_data=MetaDataPatch(),
            response=db_customer,
        )
