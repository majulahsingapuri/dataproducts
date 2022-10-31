from django.contrib.postgres.indexes import GinIndex
from django.db import models

from models import FuzzySearchable


class Website(models.Model):
    url = models.URLField()

    def __str__(self) -> str:
        return self.url


class Interest(models.Model):
    class Meta:
        indexes = [
            GinIndex(
                name="interest_name_gin_idx",
                fields=["name"],
                opclasses=["gin_trgm_ops"],
            )
        ]

    objects = FuzzySearchable.as_manager()

    name = models.TextField()

    def __str__(self) -> str:
        return self.name


class Conference(models.Model):
    class Meta:
        indexes = [
            GinIndex(
                name="conference_name_gin_idx",
                fields=["name"],
                opclasses=["gin_trgm_ops"],
            )
        ]

    objects = FuzzySearchable.as_manager()

    name = models.TextField()

    def __str__(self) -> str:
        return self.name


class Faculty(models.Model):
    name = models.TextField()

    def __str__(self) -> str:
        return self.name


class Publication(models.Model):
    class Meta:
        indexes = [
            GinIndex(
                name="publication_name_gin_idx",
                fields=["title"],
                opclasses=["gin_trgm_ops"],
            )
        ]

    objects = FuzzySearchable.as_manager()

    title = models.TextField()
    abstract = models.TextField()
    num_citations = models.PositiveIntegerField()
    year = models.DateField(null=True)
    group = models.PositiveIntegerField(null=True)
    paper_url = models.ForeignKey(Website, on_delete=models.PROTECT, null=True)
    conference = models.ForeignKey(Conference, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title


class Researcher(models.Model):
    class Meta:
        indexes = [
            GinIndex(
                name="researcher_name_gin_idx",
                fields=["name"],
                opclasses=["gin_trgm_ops"],
            )
        ]

    objects = FuzzySearchable.as_manager()

    name = models.TextField(unique=True)
    email = models.EmailField(null=True, unique=True)
    citations = models.PositiveIntegerField(null=True)
    scholar_id = models.TextField()
    faculty = models.ForeignKey(Faculty, on_delete=models.RESTRICT, null=True)
    interests = models.ManyToManyField(Interest)
    co_authors = models.ManyToManyField("self")
    publications = models.ManyToManyField(Publication)

    def __str__(self) -> str:
        return self.name


class Citation(models.Model):
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    year = models.DateField()
    count = models.PositiveIntegerField()


class ResearcherWebsites(models.Model):
    class WebsiteType(models.TextChoices):
        DR_NTU = "dr_ntu"
        DBLP = "dblp"
        IMAGE = "image"
        LINKEDIN = "linkedin"
        OTHER = "other"

    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    type = models.TextField(choices=WebsiteType.choices)
