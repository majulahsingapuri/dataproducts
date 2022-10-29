from typing import Dict, Optional

from pydantic import BaseModel

from api import models


class Coauthor(BaseModel):
    container_type: str
    filled: list
    scholar_id: str
    source: str
    name: str
    affiliation: str


class Bib(BaseModel):
    title: str
    pub_year: Optional[str] = None
    citation: str


class BibFull(BaseModel):
    title: str
    author: list[str]
    pub_year: str
    venue: str
    abstract: str


class PublicationFull(BaseModel):
    container_type: str
    source: str
    bib: BibFull
    filled: bool
    gsrank: int
    pub_url: str
    author_id: list[str]
    url_scholarbib: str
    url_add_sclib: str
    num_citations: int
    citedby_url: str
    url_related_articles: str
    eprint_url: str


class Publication(BaseModel):
    container_type: str
    source: str
    bib: Bib
    filled: bool
    author_pub_id: str
    num_citations: int
    citedby_url: Optional[str] = None
    cites_id: Optional[list[str]] = None
    public_access: Optional[bool] = None


class PublicAccess(BaseModel):
    available: int
    not_available: int


class GoogleScholar(BaseModel):
    container_type: str
    filled: list[str]
    source: str
    scholar_id: str
    url_picture: str
    name: str
    affiliation: str
    email_domain: str
    interests: list[str]
    citedby: int
    organization: Optional[int]
    homepage: Optional[str]
    citedby5y: int
    hindex: int
    hindex5y: int
    i10index: int
    i10index5y: int
    cites_per_year: Dict[int, int]
    coauthors: list[Coauthor]
    publications: list[Publication]
    public_access: PublicAccess


class Researcher(BaseModel):
    name: str
    email: Optional[str]
    citations: Optional[int]
    scholar_id: str
    faculty: Optional[str]
    interests: list[str]
    co_authors: list[str]
    publications: list[str]

    @classmethod
    def from_orm(cls, researcher: models.Researcher):
        return cls(
            name=researcher.name,
            email=researcher.email,
            citations=researcher.citations,
            scholar_id=researcher.scholar_id,
            faculty=researcher.faculty.name,
            interests=[item.name for item in researcher.interests.all()],
            co_authors=[item.name for item in researcher.co_authors.all()],
            publications=[item.name for item in researcher.publications.all()],
        )