from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

from .fields import (
    String10Field,
    String40Field,
    String70Field,
)


class InvoiceBase(SQLModel):
    invoice_date: datetime = Field(
        title="Invoice Date",
        description="The date of the invoice",
        sa_column=Column("InvoiceDate", DateTime),
    )
    billing_address: Optional[str] = String70Field(
        title="Billing Address",
        description="The billing address",
        mapped_name="BillingAddress",
    )
    billing_city: Optional[str] = String40Field(
        title="Billing City",
        description="The billing city",
        mapped_name="BillingCity",
    )
    billing_state: Optional[str] = String40Field(
        title="Billing State",
        description="The billing state",
        mapped_name="BillingState",
    )
    billing_country: Optional[str] = String40Field(
        title="Billing Country",
        description="The billing country",
        mapped_name="BillingCountry",
    )
    billing_postal_code: Optional[str] = String10Field(
        title="Billing Postal Code",
        description="The billing postal code",
        mapped_name="BillingPostalCode",
    )
    total: Decimal = Field(
        ge=0,
        title="Total",
        description="The total amount of the invoice",
        sa_column=Column("Total", Numeric(10, 2)),
    )


class Invoice(InvoiceBase, table=True):
    __tablename__ = "invoices"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("InvoiceId", Integer, primary_key=True),
        description="The unique identifier for the invoice",
    )
    customer_id: int = Field(
        sa_column=Column("CustomerId", Integer, ForeignKey("customers.CustomerId")),
        description="The customer identifier",
    )
    # invoice_date: datetime = Field(sa_column=Column("InvoiceDate", DateTime))
    # billing_address: Optional[str] = Field(sa_column=Column("BillingAddress", String))
    # billing_city: Optional[str] = Field(sa_column=Column("BillingCity", String))
    # billing_state: Optional[str] = Field(sa_column=Column("BillingState", String))
    # billing_country: Optional[str] = Field(sa_column=Column("BillingCountry", String))
    # billing_postal_code: Optional[str] = Field(
    #     sa_column=Column("BillingPostalCode", String)
    # )
    # total: Decimal = Field(sa_column=Column("Total", Numeric(10, 2)))

    # Add this relationship to link to InvoiceItems
    invoice_items: List["InvoiceItem"] = Relationship(back_populates="invoice")

    model_config = ConfigDict(from_attributes=True)


# Create operation
class InvoiceCreate(InvoiceBase):
    customer_id: int


# Read operation
class InvoiceRead(InvoiceBase):
    id: int
    customer_id: int

    model_config = ConfigDict(
        from_attributes=True, json_encoders={Decimal: lambda v: float(v)}
    )


class InvoiceReadWithInvoiceItems(InvoiceBase):
    id: int
    customer_id: int
    invoice_items: List["InvoiceItemRead"] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True, json_encoders={Decimal: lambda v: float(v)}
    )


# Update operation (Put)
class InvoiceUpdate(InvoiceBase):
    name: str | None = Field(default=None)


# Patch operation
class InvoicePatch(InvoiceBase):
    name: Optional[str] = Field(default=None)


from .invoice_items import InvoiceItem  # noqa: E402


from .invoice_items import InvoiceItemRead  # noqa: E402

# Read with relationships
# class InvoiceReadWithCustomer(InvoiceRead):
#     customer: "Customer"
