from datetime import datetime
from multiprocessing.dummy import Pool
from random import shuffle

from django.core.management.base import BaseCommand
from scholarly import ProxyGenerator, scholarly

from api import models, schemas

print("Generating Proxies")
pg = ProxyGenerator()
try:
    pg.FreeProxies()
    scholarly.use_proxy(pg, pg)
    print("UsingProxy")
except Exception:
    print("proxies timed out")


class Command(BaseCommand):
    help = "Imports the Paper Data"

    def get_papers(self, paper: models.Publication):
        paper_name = paper.title
        print(f"Adding Paper: {paper_name}")
        try:
            data = schemas.GSPublicationFilled.parse_file(
                f"./data/publications/{paper_name}.json"
            )
            print(f"using cached {paper_name}")
        except Exception:
            print(f"fetching scholarly {paper_name}")
            data = scholarly.fill(next(scholarly.search_pubs(paper_name)))
            data = schemas.GSPublicationFilled.parse_obj(data)
            with open(f"./data/publications/{paper_name}.json", "w+") as f:
                f.write(data.json())

        url, _ = models.Website.objects.update_or_create(url=data.eprint_url)
        conference, _ = models.Conference.objects.update_or_create(name=data.bib.venue)

        paper.abstract = data.bib.abstract
        paper.num_citations = data.num_citations
        paper.year = datetime(data.bib.pub_year, 1, 1)
        paper.paper_url = url
        paper.conference = conference
        paper.save()

    def handle(self, *args, **options):

        papers = list(
            models.Publication.objects.filter(
                researcher__faculty=models.Faculty.objects.first()
            )
        )
        shuffle(papers)

        pool = Pool(processes=2)
        pool.map(self.get_papers, papers[:100])

        print("done")
