from django.shortcuts import get_object_or_404
from ninja import Router

from schemas import PaginatedList, paginate

from . import models, schemas

router = Router()


@router.get("/researcher", response=PaginatedList[schemas.Researcher])
def get_researchers(request, page: int = 1, limit: int = 10):
    results = models.Researcher.objects.all()
    return paginate(results, schemas.Researcher, page, limit)


@router.get("/researcher/search", response=PaginatedList[schemas.Researcher])
def get_researcher_search(request, q: str = None, page: int = 1, limit: int = 10):
    if q:
        results = models.Researcher.objects.fuzzy_search(q)
        return paginate(results, schemas.Researcher, page, limit)
    results = models.Researcher.objects.all()
    return paginate(results, schemas.Researcher, page, limit)


@router.get("/researcher/{str:name}", response=schemas.Researcher)
def get_researcher_name(request, name: str):
    researcher = get_object_or_404(models.Researcher, name=name)
    return schemas.Researcher.from_orm(researcher)


@router.get(
    "/researcher/{str:name}/websites", response=PaginatedList[schemas.ResearcherWebsite]
)
def get_researcher_websites(request, name: str, page: int = 1, limit: int = 10):
    researcher = get_object_or_404(models.Researcher, name=name)
    results = models.ResearcherWebsites.objects.filter(
        researcher=researcher
    ).prefetch_related("website")
    return paginate(results, schemas.ResearcherWebsite, page, limit)
