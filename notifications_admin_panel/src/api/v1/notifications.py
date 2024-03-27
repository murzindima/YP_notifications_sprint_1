from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.messages import TEMPLATE_NOT_FOUND, TEMPLATES_NOT_FOUND
from src.schemas.template import Template as TemplateSchema
from src.schemas.template import TemplateCreate as TemplateCreateSchema
from src.services.template import TemplateService, get_template_service

router = APIRouter()


@router.post("/", response_model=TemplateSchema, status_code=status.HTTP_201_CREATED)
async def create_notifications(
    template_data: TemplateCreateSchema,
    template_service: TemplateService = Depends(get_template_service)
) -> TemplateSchema:
    """Creates a new template."""
    template = await template_service.create_model(template_data)
    return template
