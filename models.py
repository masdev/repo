from pydantic import BaseModel,ConfigDict, BeforeValidator, Field, field_validator
from typing import Optional, Annotated, List

PyObjectId = Annotated[str, BeforeValidator(str)]

# this class is for inserting a new car into database
class CarModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    brand: str = Field(...)
    make: str = Field(...)
    year: int = Field(..., gt=1970, lt=2100)
    cm3: int = Field(..., gt=0, lt=10000)
    km: int = Field(..., gt=0, lt=1000000)
    price: int = Field(..., gt=0, lt=99000000)
    user_id: str = Field(...)
    picture_url: Optional[str] = Field(None)

    @field_validator("brand")
    @classmethod
    def check_brand_case(cls, v: str) -> str:
        return v.title()

    @field_validator("make")
    @classmethod
    def check_make_case(cls, v: str) -> str:
        return v.title()

    model_config = ConfigDict(
        populate_by_name=True,
        populate_by_alias=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "brand": "Ford",
                "make": "Fiesta",
                "year": "1999",
                "cm3": 1500,
                "km": 55000,
                "price": 6000,
            },
        },
    )

# this class is for updating a new car into database
class UpdateCarModel(BaseModel):
    brand: Optional[str] = Field(...)
    make: Optional[str] = Field(...)
    year: Optional[int] = Field(..., gt=1970, lt=2100)
    cm3: Optional[int] = Field(..., gt=0, lt=10000)
    km: Optional[int] = Field(..., gt=0, lt=1000*1000)
    price: Optional[int] = Field(..., gt=0, lt=99*1000*1000)
    picture_url: Optional[str] = Field(None)

    @field_validator("brand")
    @classmethod
    def check_brand_case(cls, v: str) -> str:
        return v.title()

    @field_validator("make")
    @classmethod
    def check_make_case(cls, v: str) -> str:
        return v.title()

    model_config = ConfigDict(
        populate_by_name=True,
        populate_by_alias=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "brand": "Ford",
                "make": "Fiesta",
                "year": 1999,
                "cm3": 1500,
                "km": 55000,
                "price": 6000,
            },
        },
    )

class CarCollection(BaseModel):
    cars: List[CarModel]

class CarCollectionPagination(CarCollection):
    page: int = Field(ge=1, default=1)
    has_more: bool

######################### USER MODELS ###################################


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(...)

class LoginModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class CurrentUserModel(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3, max_length=15)