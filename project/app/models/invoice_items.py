from typing import Optional
from decimal import Decimal
from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


class InvoiceItemBase(SQLModel):
    unit_price: Decimal = Field(
        ge=0,
        title="Unit Price",
        description="The unit price of the item",
        sa_column=Column("UnitPrice", Numeric(10, 2), nullable=False),
    )
    quantity: int = Field(
        ge=0,
        title="Quantity",
        description="The quantity of items",
        sa_column=Column("Quantity", Integer, nullable=False),
    )


class InvoiceItem(InvoiceItemBase, table=True):
    __tablename__ = "invoice_items"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("InvoiceLineId", Integer, primary_key=True),
        description="The unique identifier for the invoice line item",
    )
    invoice_id: int = Field(
        ge=0,
        sa_column=Column(
            "InvoiceId", Integer, ForeignKey("invoices.InvoiceId"), nullable=False
        ),
        title="Key to Invoice",
        description="Foreign key to the invoice",
    )
    track_id: int = Field(
        ge=0,
        sa_column=Column(
            "TrackId", Integer, ForeignKey("tracks.TrackId"), nullable=False
        ),
        title="Key to Track",
        description="Foreign key to the track",
    )

    invoice: Optional["Invoice"] = Relationship(back_populates="invoice_items")
    track: Optional["Track"] = Relationship(back_populates="invoice_items")

    model_config = ConfigDict(from_attributes=True)


# Create operation
class InvoiceItemCreate(InvoiceItemBase):
    invoice_id: int
    track_id: int


# Read operation
class InvoiceItemRead(InvoiceItemBase):
    id: int
    invoice_id: int
    track_id: int

    model_config = ConfigDict(from_attributes=True)


# Update operation (Put)
class InvoiceItemUpdate(InvoiceItemBase):
    unit_price: Optional[Decimal] = None
    quantity: Optional[int] = None


# Patch operation
class InvoiceItemPatch(InvoiceItemBase):
    unit_price: Optional[Decimal] = None
    quantity: Optional[int] = None


from .invoices import Invoice  # noqa: E402
from .tracks import Track  # noqa: E402
