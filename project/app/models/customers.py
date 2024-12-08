from typing import Optional
from sqlalchemy import Column, Integer, Index
from sqlmodel import SQLModel, Field, ForeignKey
from pydantic import ConfigDict

from .fields import (
    String10Field,
    String20Field,
    String24Field,
    String40Field,
    String60Field,
    String70Field,
    String80Field,
)


class CustomerBase(SQLModel):
    first_name: str = String40Field(
        title="First Name",
        description="The customer's first name",
        mapped_name="FirstName",
    )
    last_name: str = String20Field(
        title="Last Name",
        description="The customer's last name",
        mapped_name="LastName",
    )
    email: str = String60Field(
        title="Email",
        description="The customer's email address",
        mapped_name="Email",
    )
    company: Optional[str] = String80Field(
        title="Company",
        description="The customer's company",
        mapped_name="Company",
    )
    address: Optional[str] = String70Field(
        title="Address",
        description="The customer's address",
        mapped_name="Address",
    )
    city: Optional[str] = String40Field(
        title="City",
        description="The customer's city",
        mapped_name="City",
    )
    state: Optional[str] = String40Field(
        title="State",
        description="The customer's state",
        mapped_name="State",
    )
    country: Optional[str] = String40Field(
        title="Country",
        description="The customer's country",
        mapped_name="Country",
    )
    postal_code: Optional[str] = String10Field(
        title="Postal Code",
        description="The customer's postal code",
        mapped_name="PostalCode",
    )
    phone: Optional[str] = String24Field(
        title="Phone",
        description="The customer's phone number",
        mapped_name="Phone",
    )
    fax: Optional[str] = String24Field(
        title="Fax",
        description="The customer's fax number",
        mapped_name="Fax",
    )


class Customer(CustomerBase, table=True):
    __tablename__ = "customers"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("CustomerId", Integer, primary_key=True),
        description="The unique identifier for the customer",
    )
    # first_name: str = Field(sa_column=Column("FirstName", String(40)))
    # last_name: str = Field(sa_column=Column("LastName", String(20)))
    # email: str = Field(sa_column=Column("Email", String(60)))
    # company: Optional[str] = Field(sa_column=Column("Company", String(80)))
    # address: Optional[str] = Field(sa_column=Column("Address", String(70)))
    # city: Optional[str] = Field(sa_column=Column("City", String(40)))
    # state: Optional[str] = Field(sa_column=Column("State", String(40)))
    # country: Optional[str] = Field(sa_column=Column("Country", String(40)))
    # postal_code: Optional[str] = Field(sa_column=Column("PostalCode", String(10)))
    # phone: Optional[str] = Field(sa_column=Column("Phone", String(24)))
    # fax: Optional[str] = Field(sa_column=Column("Fax", String(24)))
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
