from typing import Optional
from sqlalchemy import Column, Integer, String, Index
from sqlmodel import SQLModel, Field, ForeignKey
from pydantic import ConfigDict


class CustomerBase(SQLModel):
    first_name: str = Field(
        default=None,
        description="The customer's first name",
        title="First Name",
        max_length=40,
    )
    last_name: str = Field(
        default=None,
        description="The customer's last name",
        title="Last Name",
        max_length=20,
    )
    email: str = Field(
        default=None,
        description="The customer's email address",
        title="Email",
        max_length=60,
    )
    company: Optional[str] = Field(
        default=None,
        description="The customer's company",
        title="Company",
        max_length=80,
    )
    address: Optional[str] = Field(
        default=None,
        description="The customer's address",
        title="Address",
        max_length=70,
    )
    city: Optional[str] = Field(
        default=None,
        description="The customer's city",
        title="City",
        max_length=40,
    )
    state: Optional[str] = Field(
        default=None,
        description="The customer's state",
        title="State",
        max_length=40,
    )
    country: Optional[str] = Field(
        default=None,
        description="The customer's country",
        title="Country",
        max_length=40,
    )
    postal_code: Optional[str] = Field(
        default=None,
        description="The customer's postal code",
        title="Postal Code",
        max_length=10,
    )
    phone: Optional[str] = Field(
        default=None,
        description="The customer's phone number",
        title="Phone",
        max_length=24,
    )
    fax: Optional[str] = Field(
        default=None,
        description="The customer's fax number",
        title="Fax",
        max_length=24,
    )


class Customer(CustomerBase, table=True):
    __tablename__ = "customers"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("CustomerId", Integer, primary_key=True),
        description="The unique identifier for the customer",
    )
    first_name: str = Field(sa_column=Column("FirstName", String(40)))
    last_name: str = Field(sa_column=Column("LastName", String(20)))
    email: str = Field(sa_column=Column("Email", String(60)))
    company: Optional[str] = Field(sa_column=Column("Company", String(80)))
    address: Optional[str] = Field(sa_column=Column("Address", String(70)))
    city: Optional[str] = Field(sa_column=Column("City", String(40)))
    state: Optional[str] = Field(sa_column=Column("State", String(40)))
    country: Optional[str] = Field(sa_column=Column("Country", String(40)))
    postal_code: Optional[str] = Field(sa_column=Column("PostalCode", String(10)))
    phone: Optional[str] = Field(sa_column=Column("Phone", String(24)))
    fax: Optional[str] = Field(sa_column=Column("Fax", String(24)))
    support_rep_id: Optional[int] = Field(
        default=None,
        sa_column=Column("SupportRepId", Integer, ForeignKey("employees.EmployeeId")),
        description="The ID of the customer's support representative",
    )

    model_config = ConfigDict(from_attributes=True)

    __table_args__ = (Index("IFK_CustomerSupportRepId", "SupportRepId"),)


class CustomerCreate(CustomerBase):
    pass


# Read operation
class CustomerRead(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Update operation (Put)
class CustomerUpdate(CustomerBase):
    pass


# Patch operation
class CustomerPatch(CustomerBase):
    pass
