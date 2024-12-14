from typing import Optional, List
from functools import partial
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

from .fields import ValidationConstant, create_string_field

FirstNameField = partial(
    create_string_field,
    "First Name",
    "The employee's first name",
    ValidationConstant.STRING_20,
)
LastNameField = partial(
    create_string_field,
    "Last Name",
    "The employee's last name",
    ValidationConstant.STRING_20,
)
TitleField = partial(
    create_string_field,
    "Title",
    "The employee's job title",
    ValidationConstant.STRING_30,
)
AddressField = partial(
    create_string_field,
    "Address",
    "The employee's address",
    ValidationConstant.STRING_70,
)
CityField = partial(
    create_string_field, "City", "The employee's city", ValidationConstant.STRING_40
)
StateField = partial(
    create_string_field, "State", "The employee's state", ValidationConstant.STRING_40
)
CountryField = partial(
    create_string_field,
    "Country",
    "The employee's country",
    ValidationConstant.STRING_40,
)
PostalCodeField = partial(
    create_string_field,
    "Postal Code",
    "The employee's postal code",
    ValidationConstant.STRING_10,
)
PhoneField = partial(
    create_string_field, "Phone", "The employee's phone", ValidationConstant.STRING_24
)
FaxField = partial(
    create_string_field,
    "Fax",
    "The employee's fax number",
    ValidationConstant.STRING_24,
)
EmailField = partial(
    create_string_field, "Email", "The employee's email", ValidationConstant.STRING_60
)


class EmployeeBase(SQLModel):
    first_name: str = FirstNameField(mapped_name="FirstName")
    last_name: str = LastNameField(mapped_name="LastName")
    title: Optional[str] = TitleField(mapped_name="Title")
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
    address: Optional[str] = AddressField(mapped_name="Address")
    city: Optional[str] = CityField(mapped_name="City")
    state: Optional[str] = StateField(mapped_name="State")
    country: Optional[str] = CountryField(mapped_name="Country")
    postal_code: Optional[str] = PostalCodeField(mapped_name="PostalCode")
    phone: Optional[str] = PhoneField(mapped_name="Phone")
    fax: Optional[str] = FaxField(mapped_name="Fax")
    email: Optional[str] = EmailField(mapped_name="Email")
    reports_to: Optional[int] = Field(
        default=None,
        sa_column=Column(
            "ReportsTo", Integer, ForeignKey("employees.EmployeeId"), index=True
        ),
        description="The ID of the employee's manager",
    )


class Employee(EmployeeBase, table=True):
    __tablename__ = "employees"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("EmployeeId", Integer, primary_key=True),
        description="The unique identifier for the employee",
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
    first_name: Optional[str] = FirstNameField()
    last_name: Optional[str] = LastNameField()
    title: Optional[str] = TitleField()
    birth_date: Optional[datetime]
    hire_date: Optional[datetime]
    address: Optional[str] = AddressField()
    city: Optional[str] = CityField()
    state: Optional[str] = StateField()
    country: Optional[str] = CountryField()
    postal_code: Optional[str] = PostalCodeField()
    phone: Optional[str] = PhoneField()
    fax: Optional[str] = FaxField()
    email: Optional[str] = EmailField()
    reports_to: Optional[int]
