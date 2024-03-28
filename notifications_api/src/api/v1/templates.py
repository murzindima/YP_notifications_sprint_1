from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.messages import TEMPLATE_NOT_FOUND, TEMPLATES_NOT_FOUND
from src.schemas.template import Template as TemplateSchema
from src.schemas.template import TemplateCreate as TemplateCreateSchema
from src.services.template import TemplateService, get_template_service

router = APIRouter()


@router.post("/", response_model=TemplateSchema, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: TemplateCreateSchema,
    template_service: TemplateService = Depends(get_template_service),
) -> TemplateSchema:
    """Creates a new template."""
    template = await template_service.create_model(template_data)
    return template


@router.get("/", response_model=list[TemplateSchema], status_code=status.HTTP_200_OK)
async def all_templates(
    template_service: TemplateService = Depends(get_template_service),
) -> list[TemplateSchema]:
    """Returns all templates with pagination."""
    templates = await template_service.get_all_models()

    if not templates:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=TEMPLATES_NOT_FOUND
        )

    return [TemplateSchema(**template.model_dump()) for template in templates]


@router.get(
    "/{template_id}", response_model=TemplateSchema, status_code=status.HTTP_200_OK
)
async def template_details(
    template_id: UUID, template_service: TemplateService = Depends(get_template_service)
) -> TemplateSchema:
    """Returns the template by identifier."""
    template = await template_service.get_model_by_id(template_id)
    if not template:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=TEMPLATE_NOT_FOUND)

    return TemplateSchema(**template.model_dump())


@router.put(
    "/{template_id}", response_model=TemplateSchema, status_code=status.HTTP_200_OK
)
async def update_template(
    template_id: UUID,
    template_data: TemplateCreateSchema,
    template_service: TemplateService = Depends(get_template_service),
) -> TemplateSchema:
    """Updates the template by identifier."""
    template = await template_service.update_model(template_id, template_data)
    if not template:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=TEMPLATE_NOT_FOUND)

    return TemplateSchema(**template.model_dump())


@router.delete(
    "/{template_id}", response_model=TemplateSchema, status_code=status.HTTP_200_OK
)
async def delete_template(
    template_id: UUID, template_service: TemplateService = Depends(get_template_service)
) -> TemplateSchema:
    """Deletes the template by identifier."""
    template = await template_service.delete_model(template_id)
    if not template:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=TEMPLATE_NOT_FOUND)

    return TemplateSchema(**template.model_dump())
