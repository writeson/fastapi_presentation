from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, DateTime, String, Numeric, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


class InvoiceBase(SQLModel):
    invoice_date: datetime = Field(
        default=None, description="The date of the invoice", title="Invoice Date"
    )
    billing_address: Optional[str] = Field(
        default=None,
        description="The billing address",
        title="Billing Address",
        max_length=70,
    )
    billing_city: Optional[str] = Field(
        default=None,
        description="The billing city",
        title="Billing City",
        max_length=40,
    )
    billing_state: Optional[str] = Field(
        default=None,
        description="The billing state",
        title="Billing State",
        max_length=40,
    )
    billing_country: Optional[str] = Field(
        default=None,
        description="The billing country",
        title="Billing Country",
        max_length=40,
    )
    billing_postal_code: Optional[str] = Field(
        default=None,
        description="The billing postal code",
        title="Billing Postal Code",
        max_length=10,
    )
    total: Decimal = Field(description="The total amount of the invoice", title="Total")


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
    invoice_date: datetime = Field(sa_column=Column("InvoiceDate", DateTime))
    billing_address: Optional[str] = Field(sa_column=Column("BillingAddress", String))
    billing_city: Optional[str] = Field(sa_column=Column("BillingCity", String))
    billing_state: Optional[str] = Field(sa_column=Column("BillingState", String))
    billing_country: Optional[str] = Field(sa_column=Column("BillingCountry", String))
    billing_postal_code: Optional[str] = Field(
        sa_column=Column("BillingPostalCode", String)
    )
    total: Decimal = Field(sa_column=Column("Total", Numeric(10, 2)))

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
