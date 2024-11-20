from project.app.models.employees import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
    EmployeePatch,
)
from project.app.database import get_db
from project.app.endpoints.employees import crud as employee_crud

from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)],
)


@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        return await employee_crud.create_employee(session=session, employee=employee)


@router.get("/", response_model=list[EmployeeRead])
async def read_employees(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        return await employee_crud.read_employees(
            session=session, offset=offset, limit=limit
        )


@router.get("/{id}", response_model=EmployeeRead)
async def read_employee(
    id: int = Path(..., title="The ID of the artist to get"),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        db_employee = await employee_crud.read_employee(session=session, id=id)
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return db_employee


@router.put("/{id}", response_model=EmployeeRead)
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
        return db_employee


@router.patch("/{id}", response_model=EmployeeRead)
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
        return db_employee
