from django.shortcuts import get_object_or_404
from ninja import Router

from . import models, schemas

router = Router()


@router.get("/researcher/{str:name}", response=schemas.Researcher)
def get_researcher_name(request, name: str):
    researcher = get_object_or_404(models.Researcher, name=name)
    return schemas.Researcher.from_orm(researcher)
