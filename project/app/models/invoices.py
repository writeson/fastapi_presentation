from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from functools import partial

from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


from .fields import ValidationConstant, create_string_field

BillingAddressField = partial(
    create_string_field,
    "Billing Address",
    "The billing address",
    ValidationConstant.STRING_70,
)
BillingCityField = partial(
    create_string_field,
    "Billing City",
    "The billing city",
    ValidationConstant.STRING_40,
)
BillingStateField = partial(
    create_string_field,
    "Billing State",
    "The billing state",
    ValidationConstant.STRING_40,
)
BillingCountryField = partial(
    create_string_field,
    "Billing Country",
    "The billing country",
    ValidationConstant.STRING_40,
)
BillingPostalCodeField = partial(
    create_string_field,
    "Billing Postal Code",
    "The billing postal code",
    ValidationConstant.STRING_10,
)


class InvoiceBase(SQLModel):
    invoice_date: datetime = Field(
        title="Invoice Date",
        description="The date of the invoice",
        sa_column=Column("InvoiceDate", DateTime),
    )
    billing_address: Optional[str] = BillingAddressField(
        mapped_name="BillingAddress",
    )
    billing_city: Optional[str] = BillingCityField(
        mapped_name="BillingCity",
    )
    billing_state: Optional[str] = BillingStateField(
        mapped_name="BillingState",
    )
    billing_country: Optional[str] = BillingCountryField(
        mapped_name="BillingCountry",
    )
    billing_postal_code: Optional[str] = BillingPostalCodeField(
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
    billing_address: str | None = BillingAddressField()
    billing_city: str | None = BillingCityField()
    billing_state: str | None = BillingStateField()
    billing_country: str | None = BillingCountryField()
    billing_postal_code: str | None = BillingPostalCodeField()
    total: Decimal = Field(
        ge=0,
        title="Total",
        description="The total amount of the invoice",
    )


# Patch operation
class InvoicePatch(InvoiceBase):
    billing_address: Optional[str | None] = BillingAddressField()
    billing_city: Optional[str | None] = BillingCityField()
    billing_state: Optional[str | None] = BillingStateField()
    billing_country: Optional[str | None] = BillingCountryField()
    billing_postal_code: Optional[str | None] = BillingPostalCodeField()
    total: Optional[Decimal] = Field(
        ge=0,
        title="Total",
        description="The total amount of the invoice",
    )


from .invoice_items import InvoiceItem  # noqa: E402


from .invoice_items import InvoiceItemRead  # noqa: E402
