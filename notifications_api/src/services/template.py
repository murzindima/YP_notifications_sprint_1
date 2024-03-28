from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.models.template import Template as TemplateModel
from src.schemas.template import Template as TemplateSchema
from src.services.base import BaseService
from src.services.data_repository.postgres import PostgresService


class TemplateService(BaseService):
    """Service class for managing roles, extending the BaseService."""


@lru_cache
def get_template_service(
    pg_session: AsyncSession = Depends(get_session),
) -> TemplateService:
    """Dependency function to get an instance of the TemplateService."""
    return TemplateService(
        model_schema_class=TemplateSchema,
        postgres_service=PostgresService(session=pg_session, model_class=TemplateModel),
    )
