from uuid import UUID
from pydantic import BaseModel


class TemplateCreate(BaseModel):
    """Schema for creating a new template."""

    name: str
    description: str | None = None
    template: str


class TemplateUpdate(BaseModel):
    """Schema for updating an existing template."""

    name: str | None = None
    description: str | None = None
    template: str | None = None


class Template(BaseModel):
    """Schema for representing a template."""

    id: UUID
    name: str
    description: str | None
    template: str

    class Config:
        from_attributes = True
