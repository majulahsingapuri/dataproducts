from django.shortcuts import get_object_or_404
from ninja import Router

from schemas import PaginatedList, paginate

from . import models, schemas

router = Router()


@router.get("/researcher", response=PaginatedList[schemas.Researcher])
def get_researchers(request, page: int = 1, limit: int = 10):
    results = models.Researcher.objects.all().prefetch_related(
        "interests", "co_authors", "publications"
    )
    return paginate(results, schemas.Researcher, page, limit)


@router.get("/researcher/search", response=PaginatedList[schemas.ResearcherStub])
def get_researcher_search(request, q: str = None, page: int = 1, limit: int = 10):
    results = models.Researcher.objects.all()
    if q:
        results = results.fuzzy_search(q)
    return paginate(results, schemas.ResearcherStub, page, limit)


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


@router.get("/researcher/{str:name}/citations", response=list[schemas.Citation])
def get_researcher_citations(request, name: str):
    researcher = get_object_or_404(models.Researcher, name=name)
    results = models.Citation.objects.filter(researcher=researcher).order_by("year")
    return [schemas.Citation.from_orm(citation) for citation in results]


@router.get(
    "/researcher/{str:name}/publications", response=PaginatedList[schemas.Publication]
)
def get_researcher_publications(request, name: str, page: int = 1, limit: int = 10):
    researcher = get_object_or_404(models.Researcher, name=name)
    results = models.Publication.objects.filter(researcher=researcher).prefetch_related(
        "paper_url", "conference"
    )

    return paginate(results, schemas.Publication, page, limit)
