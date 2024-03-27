from uuid import UUID

from sqlalchemy import select

from src.services.data_repository.postgres_crud import PostgresCrudService
from src.models.template import Template as TemplateModel


class PostgresService(PostgresCrudService):
    """A data storage service implementation for working with Postgres."""

    async def get_template(self, template_id: UUID) -> TemplateModel | None:
        """Retrieve a role."""
        async with self.session.begin():
            model = await self.session.get(TemplateModel, template_id)
            return model

    async def get_template_id_by_name(self, template_name: str) -> UUID | None:
        """Retrieve a role identifier by name."""
        async with self.session.begin():
            stmt = select(TemplateModel.id).where(TemplateModel.name == template_name)
            result = await self.session.execute(stmt)
            role_id = result.scalar()
            return role_id
