from datetime import datetime
from multiprocessing.dummy import Pool

import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Q
from scholarly import ProxyGenerator, scholarly

from api import models, schemas

print("Generating Proxies")
pg = ProxyGenerator()
try:
    scholarly.use_proxy(pg, pg)
    print("UsingProxy")
except Exception:
    print("proxies timed out")


class Command(BaseCommand):
    help = "Imports the Initial Professor Data"

    def get_researchers(self, researcher: models.Researcher):
        researcher_name = researcher.name
        print(f"Adding Researcher: {researcher_name}")
        try:
            data = schemas.GoogleScholar.parse_file(f"./data/{researcher_name}.json")
            print(f"using cached {researcher_name}")
        except Exception:
            data = scholarly.fill(next(scholarly.search_author(researcher_name)))
            data = schemas.GoogleScholar.parse_obj(data)
            with open(f"./data/{researcher_name}.json", "w+") as f:
                f.write(data.json())

        researcher.citations = data.citedby
        researcher.scholar_id = data.scholar_id
        researcher.save()

        print(f"Adding Researcher: {researcher_name} citations")
        for year, citations in data.cites_per_year.items():
            models.Citation.objects.update_or_create(
                researcher=researcher, year=datetime(year, 1, 1), count=citations
            )

        print(f"Adding Researcher: {researcher_name} image, interests and coauthors")
        image_url, _ = models.Website.objects.update_or_create(url=data.url_picture)
        models.ResearcherWebsites.objects.update_or_create(
            researcher=researcher,
            website=image_url,
            type=models.ResearcherWebsites.WebsiteType.IMAGE,
        )

        researcher.interests.add(
            *[
                models.Interest.objects.update_or_create(name=interest)[0]
                for interest in data.interests
            ]
        )
        researcher.co_authors.add(
            *[
                models.Researcher.objects.update_or_create(
                    name=author.name, defaults=dict(scholar_id=author.scholar_id)
                )[0]
                for author in data.coauthors
            ]
        )

        print(f"Adding Researcher: {researcher_name} publications")
        researcher.publications.add(
            *[
                models.Publication.objects.update_or_create(
                    title=publication.bib.title,
                    year=datetime(int(publication.bib.pub_year), 1, 1)
                    if publication.bib.pub_year
                    else None,
                    num_citations=publication.num_citations,
                )[0]
                for publication in data.publications
            ]
        )

    def handle(self, *args, **options):

        print("Loading CSV")
        profs = pd.read_csv("SCSE_profs.csv")

        researchers = list(
            models.Researcher.objects.filter(~Q(name__in=list(profs.Name)))
        )

        pool = Pool(processes=4)
        pool.map(self.get_researchers, researchers)

        print("done")
