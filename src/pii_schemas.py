from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class PIIBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, pattern=r"^\+?1?\d{10,14}$")
    address: str | None = Field(None, max_length=500)
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, min_length=2, max_length=2)
    zip_code: str | None = Field(None, pattern=r"^\d{5}(-\d{4})?$")

    @field_validator("first_name", "last_name")
    @classmethod
    def name_alphanumeric(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z\s\-']+$", v):
            raise ValueError("Names must contain only letters, spaces, hyphens, and apostrophes")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str | None) -> str | None:
        if v:
            digits = re.sub(r"\D", "", v)
            if len(digits) == 11 and digits.startswith("1"):
                digits = digits[1:]
            return digits
        return v


class PIICreate(PIIBase):
    pass


class SearchSource(BaseModel):
    source_name: str
    source_url: str | None = None
    data_found: bool
    data_details: str | None = None


class SearchResultResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str | None
    phone: str | None
    address: str | None
    created_at: str
    sources: list[SearchSource]

    class Config:
        from_attributes = True


class SearchHistoryItem(BaseModel):
    id: int
    first_name: str
    last_name: str
    created_at: str
    result_count: int

    class Config:
        from_attributes = True