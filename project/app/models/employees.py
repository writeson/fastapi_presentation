from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

from .fields import (
    String10Field,
    String20Field,
    String30Field,
    String24Field,
    String40Field,
    String60Field,
    String70Field,
)


class EmployeeBase(SQLModel):
    first_name: str = String20Field(
        title="First Name",
        description="The employee's first name",
        mapped_name="FirstName",
    )
    last_name: str = String20Field(
        title="Last Name",
        description="The employee's last name",
        mapped_name="LastName",
    )
    title: Optional[str] = String30Field(
        title="Title",
        description="The employee's job title",
        mapped_name="Title",
    )
    birth_date: Optional[datetime] = Field(
        title="Birth Date",
        description="The employee's birth date",
        sa_column=Column("BirthDate", DateTime),
    )
    hire_date: Optional[datetime] = Field(
        title="Hire Date",
        description="The employee's hire date",
        sa_column=Column("HireDate", DateTime),
    )
    address: Optional[str] = String70Field(
        title="Address",
        description="The employee's address",
        mapped_name="Address",
    )
    city: Optional[str] = String40Field(
        title="City",
        description="The employee's city",
        mapped_name="City",
    )
    state: Optional[str] = String40Field(
        title="State",
        description="The employee's state",
        mapped_name="State",
    )
    country: Optional[str] = String40Field(
        title="Country",
        description="The employee's country",
        mapped_name="Country",
    )
    postal_code: Optional[str] = String10Field(
        title="Postal Code",
        description="The employee's postal code",
        mapped_name="PostalCode",
    )
    phone: Optional[str] = String24Field(
        title="Phone",
        description="The employee's phone number",
        mapped_name="Phone",
    )
    fax: Optional[str] = String24Field(
        title="Fax",
        description="The employee's fax number",
        mapped_name="Fax",
    )
    email: Optional[str] = String60Field(
        title="Email",
        description="The employee's email address",
        mapped_name="Email",
    )


class Employee(EmployeeBase, table=True):
    __tablename__ = "employees"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("EmployeeId", Integer, primary_key=True),
        description="The unique identifier for the employee",
    )
    # first_name: str = Field(sa_column=Column("FirstName", String(20)))
    # last_name: str = Field(sa_column=Column("LastName", String(20)))
    # title: Optional[str] = Field(sa_column=Column("Title", String(30)))
    # birth_date: Optional[datetime] = Field(sa_column=Column("BirthDate", DateTime))
    # hire_date: Optional[datetime] = Field(sa_column=Column("HireDate", DateTime))
    # address: Optional[str] = Field(sa_column=Column("Address", String(70)))
    # city: Optional[str] = Field(sa_column=Column("City", String(40)))
    # state: Optional[str] = Field(sa_column=Column("State", String(40)))
    # country: Optional[str] = Field(sa_column=Column("Country", String(40)))
    # postal_code: Optional[str] = Field(sa_column=Column("PostalCode", String(10)))
    # phone: Optional[str] = Field(sa_column=Column("Phone", String(24)))
    # fax: Optional[str] = Field(sa_column=Column("Fax", String(24)))
    # email: Optional[str] = Field(sa_column=Column("Email", String(60)))
    reports_to: Optional[int] = Field(
        default=None,
        sa_column=Column("ReportsTo", Integer, ForeignKey("employees.EmployeeId")),
        description="The ID of the employee's manager",
    )

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
