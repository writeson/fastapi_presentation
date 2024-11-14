from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.models.employees import (
    Employee,
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
    EmployeePatch,
)


async def create_employee(session: AsyncSession, employee: EmployeeCreate) -> EmployeeRead:
    """
    Create a new Employee in the database from the passed in EmployeeCreate model.
    Returns the created EmployeeRead model.
    """
    db_employee = Employee(title=employee.title)
    session.add(db_employee)
    await session.commit()
    await session.refresh(db_employee)
    return EmployeeRead.model_validate(db_employee)


async def read_employee(session: AsyncSession, id: int) -> EmployeeRead:
    """
    Retrieve a Employee from the database by ID.
    Returns the EmployeeRead model if found, None otherwise.
    """
    query = (
        select(Employee)
        .where(Employee.id == id)
    )
    result = await session.execute(query)
    db_employee = result.unique().scalar_one_or_none()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


async def read_employees(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[EmployeeRead]:
    """
    Retrieve all Employee from the database.
    Returns a list of EmployeeRead models.
    """
    query = (
        select(Employee)
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(query)
    db_employees = result.scalars().all()
    return [EmployeeRead.model_validate(db_employee) for db_employee in db_employees]


async def update_employee(session: AsyncSession, id: int, album: EmployeeUpdate) -> EmployeeRead:
    """
    Update an existing Employee in the database using the passed in EmployeeUpdate model.
    Returns the updated EmployeeRead model if found, None otherwise.
    """
    db_employee = await read_employee(session, id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in album.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    await session.commit()
    await session.refresh(db_employee)
    return EmployeeRead.model_validate(db_employee)


async def patch_employee(session: AsyncSession, id: int, album: EmployeePatch) -> EmployeeRead:
    """
    Partially update an existing Employee in the database using the passed in EmployeePatch model.
    Returns the updated EmployeeRead model if found, None otherwise.
    """
    db_employee = await read_employee(session, id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in album.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_employee, key, value)

    await session.commit()
    await session.refresh(db_employee)
    return EmployeeRead.model_validate(db_employee)
