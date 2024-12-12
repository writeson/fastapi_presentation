from typing import Optional
from functools import partial

from sqlalchemy import Column, Integer, Index
from sqlmodel import SQLModel, Field, ForeignKey
from pydantic import ConfigDict

from .fields import ValidationConstant, create_string_field

FirstNameField = partial(
    create_string_field,
    "First Name",
    "The customer's first name",
    ValidationConstant.STRING_40,
)
LastNameField = partial(
    create_string_field,
    "Last Name",
    "The customer's last name",
    ValidationConstant.STRING_20,
)
EmailField = partial(
    create_string_field, "Email", "The customer's email", ValidationConstant.STRING_60
)
CompanyField = partial(
    create_string_field,
    "Company",
    "The customer's company",
    ValidationConstant.STRING_80,
)
AddressField = partial(
    create_string_field,
    "Address",
    "The customer's address",
    ValidationConstant.STRING_70,
)
CityField = partial(
    create_string_field, "City", "The customer's city", ValidationConstant.STRING_40
)
StateField = partial(
    create_string_field, "State", "The customer's state", ValidationConstant.STRING_40
)
CountryField = partial(
    create_string_field,
    "Country",
    "The customer's country",
    ValidationConstant.STRING_40,
)
PostalCodeField = partial(
    create_string_field,
    "Postal Code",
    "The customer's postal code",
    ValidationConstant.STRING_10,
)
PhoneField = partial(
    create_string_field, "Phone", "The customer's phone", ValidationConstant.STRING_24
)
FaxField = partial(
    create_string_field,
    "Fax",
    "The customer's fax number",
    ValidationConstant.STRING_24,
)


class CustomerBase(SQLModel):
    first_name: str = FirstNameField(
        mapped_name="FirstName",
    )
    last_name: str = LastNameField(
        mapped_name="LastName",
    )
    email: str = EmailField(
        mapped_name="Email",
    )
    company: Optional[str] = CompanyField(
        mapped_name="Company",
    )
    address: Optional[str] = AddressField(
        mapped_name="Address",
    )
    city: Optional[str] = CityField(
        mapped_name="City",
    )
    state: Optional[str] = StateField(
        mapped_name="State",
    )
    country: Optional[str] = CountryField(
        mapped_name="Country",
    )
    postal_code: Optional[str] = PostalCodeField(
        mapped_name="PostalCode",
    )
    phone: Optional[str] = PhoneField(
        mapped_name="Phone",
    )
    fax: Optional[str] = FaxField(
        mapped_name="Fax",
    )


class Customer(CustomerBase, table=True):
    __tablename__ = "customers"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("CustomerId", Integer, primary_key=True),
        description="The unique identifier for the customer",
    )
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
    first_name: str = FirstNameField()
    last_name: str = LastNameField()
    email: str = EmailField()
    company: Optional[str] = CompanyField()
    address: Optional[str] = AddressField()
    city: Optional[str] = CityField()
    state: Optional[str] = StateField()
    country: Optional[str] = CountryField()
    postal_code: Optional[str] = PostalCodeField()
    phone: Optional[str] = PhoneField()
    fax: Optional[str] = FaxField()


# Patch operation
class CustomerPatch(CustomerBase):
    first_name: Optional[str] = FirstNameField()
    last_name: Optional[str] = LastNameField()
    email: Optional[str] = EmailField()
    company: Optional[str] = CompanyField()
    address: Optional[str] = AddressField()
    city: Optional[str] = CityField()
    state: Optional[str] = StateField()
    country: Optional[str] = CountryField()
    postal_code: Optional[str] = PostalCodeField()
    phone: Optional[str] = PhoneField()
    fax: Optional[str] = FaxField()
