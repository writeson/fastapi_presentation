from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


class EmployeeBase(SQLModel):
    last_name: str = Field(
        default=None,
        description="The employee's last name",
        title="Last Name",
        max_length=20,
    )
    first_name: str = Field(
        default=None,
        description="The employee's first name",
        title="First Name",
        max_length=20,
    )
    title: Optional[str] = Field(
        default=None,
        description="The employee's job title",
        title="Title",
        max_length=30,
    )
    birth_date: Optional[datetime] = Field(
        default=None,
        description="The employee's birth date",
        title="Birth Date",
    )
    hire_date: Optional[datetime] = Field(
        default=None,
        description="The date the employee was hired",
        title="Hire Date",
    )
    address: Optional[str] = Field(
        default=None,
        description="The employee's address",
        title="Address",
        max_length=70,
    )
    city: Optional[str] = Field(
        default=None,
        description="The employee's city",
        title="City",
        max_length=40,
    )
    state: Optional[str] = Field(
        default=None,
        description="The employee's state",
        title="State",
        max_length=40,
    )
    country: Optional[str] = Field(
        default=None,
        description="The employee's country",
        title="Country",
        max_length=40,
    )
    postal_code: Optional[str] = Field(
        default=None,
        description="The employee's postal code",
        title="Postal Code",
        max_length=10,
    )
    phone: Optional[str] = Field(
        default=None,
        description="The employee's phone number",
        title="Phone",
        max_length=24,
    )
    fax: Optional[str] = Field(
        default=None,
        description="The employee's fax number",
        title="Fax",
        max_length=24,
    )
    email: Optional[str] = Field(
        default=None,
        description="The employee's email address",
        title="Email",
        max_length=60,
    )


class Employee(EmployeeBase, table=True):
    __tablename__ = "employees"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("EmployeeId", Integer, primary_key=True),
        description="The unique identifier for the employee",
    )
    last_name: str = Field(sa_column=Column("LastName", String(20)))
    first_name: str = Field(sa_column=Column("FirstName", String(20)))
    title: Optional[str] = Field(sa_column=Column("Title", String(30)))
    reports_to: Optional[int] = Field(
        default=None,
        sa_column=Column("ReportsTo", Integer, ForeignKey("employees.EmployeeId")),
        description="The ID of the employee's manager",
    )
    birth_date: Optional[datetime] = Field(sa_column=Column("BirthDate", DateTime))
    hire_date: Optional[datetime] = Field(sa_column=Column("HireDate", DateTime))
    address: Optional[str] = Field(sa_column=Column("Address", String(70)))
    city: Optional[str] = Field(sa_column=Column("City", String(40)))
    state: Optional[str] = Field(sa_column=Column("State", String(40)))
    country: Optional[str] = Field(sa_column=Column("Country", String(40)))
    postal_code: Optional[str] = Field(sa_column=Column("PostalCode", String(10)))
    phone: Optional[str] = Field(sa_column=Column("Phone", String(24)))
    fax: Optional[str] = Field(sa_column=Column("Fax", String(24)))
    email: Optional[str] = Field(sa_column=Column("Email", String(60)))

    manager: Optional["Employee"] = Relationship(
        back_populates="subordinates",
        sa_relationship_kwargs={"remote_side": "Employee.id"},
    )
    subordinates: List["Employee"] = Relationship(back_populates="manager")

    model_config = ConfigDict(from_attributes=True)

    __table_args__ = (Index("IFK_EmployeeReportsTo", "ReportsTo"),)


class EmployeeCreate(EmployeeBase):
    pass


# Read operation
class EmployeeRead(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Update operation (Put)
class EmployeeUpdate(EmployeeBase):
    pass


# Patch operation
class EmployeePatch(EmployeeBase):
    pass
