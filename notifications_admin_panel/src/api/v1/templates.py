from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from core.messages import TEMPLATE_NOT_FOUND, TEMPLATES_NOT_FOUND
from queries.template import TemplateFilter, SearchTemplateFilter
from schemas.template import Template as TemplateSchema
from services.template import TemplateService, get_template_service

router = APIRouter()


@router.get("/", response_model=list[TemplateSchema])
async def all_templates(
    template_service: TemplateService = Depends(get_template_service),
    template_filter: TemplateFilter = Depends(),
) -> list[TemplateSchema]:
    """Returns all templates with pagination."""
    templates = await template_service.get_all_models(template_filter)

    if not templates:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=TEMPLATES_NOT_FOUND
        )

    return [TemplateSchema(**template.model_dump()) for template in templates]


@router.get("/{template_id}", response_model=TemplateSchema)
async def template_details(
    template_id: str, template_service: TemplateService = Depends(get_template_service)
) -> TemplateSchema:
    """Returns the template by identifier."""
    template = await template_service.get_model_by_id(template_id)
    if not template:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=TEMPLATE_NOT_FOUND)

    return TemplateSchema(**template.model_dump())
