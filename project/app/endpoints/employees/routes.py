from typing import List

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.database import get_db
from project.app.endpoints.employees import crud as employee_crud
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
from project.app.models.employees import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
    EmployeePatch,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post(
    "/",
    response_model=CombinedResponseCreate[EmployeeRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_employee = await employee_crud.create_employee(
            session=session, employee=employee
        )

        # construct the response in the expected format
        return CombinedResponseCreate(
            meta_data=MetaDataCreate(),
            response=db_employee,
        )


@router.get("/", response_model=CombinedResponseReadAll[List[EmployeeRead], int])
async def read_employees(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        employees, total_count = await employee_crud.read_employees(
            session=session, offset=offset, limit=limit
        )
        return CombinedResponseReadAll(
            response=employees,
            total_count=total_count,
        )


@router.get("/{id}", response_model=CombinedResponseRead[EmployeeRead])
async def read_employee(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_employee = await employee_crud.read_employee(session=session, id=id)
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return CombinedResponseRead(response=EmployeeRead.model_validate(db_employee))


@router.put("/{id}", response_model=CombinedResponseUpdate[EmployeeRead])
async def update_employee(
    employee: EmployeeUpdate,
    id: int = Path(..., title="The ID of the employee to update"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_employee = await employee_crud.update_employee(
            session=session, id=id, employee=employee
        )
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        # construct the response in the expected format
        return CombinedResponseUpdate(
            meta_data=MetaDataUpdate(),
            response=db_employee,
        )


@router.patch("/{id}", response_model=CombinedResponsePatch[EmployeeRead])
async def patch_employee(
    employee: EmployeePatch,
    id: int = Path(..., title="The ID of the employee to patch"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_employee = await employee_crud.patch_employee(
            session=session, id=id, employee=employee
        )
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        # construct the response in the expected format
        return CombinedResponsePatch(
            meta_data=MetaDataPatch(),
            response=db_employee,
        )
