from datetime import datetime
from json import loads
from math import isnan
from multiprocessing.dummy import Pool
from urllib.parse import urlparse

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from googlesearch import search
from scholarly import ProxyGenerator, scholarly
from tqdm import tqdm

from api import models, schemas

print("Generating Proxies")
pg = ProxyGenerator()
try:
    success = pg.ScraperAPI("c5aed4fee563410c13f788691b47041e")
    scholarly.use_proxy(pg)
except Exception:
    print("proxies timed out")

alt_names = {
    "Douglas Leslie Maskell": "Douglas L. Maskell",
    "Jagath Chandana Rajapakse": "Jagath C. Rajapakse",
    "Joty Shafiq Rayhan": "Joty Shafiq",
    "Ke Yiping, Kelly": "Ke Yiping",
    "Lana Obraztsova": "Svetlana Obraztsova",
    "Luke Ong （翁之昊）": "Ong Luke",
    "Luo Siqiang （骆思强）": "Luo Siqiang",
    "Quek Hiok Chai": "Chai Quek",
    "Sourav Saha Bhowmick": "Sourav S Bhowmick",
    "Wee Keong NG": "W. K. Ng",
}


class Command(BaseCommand):
    help = "Imports the Initial Professor Data"

    def get_prof_scholarly(self, prof: models.Researcher):
        prof_name = alt_names.get(prof.name, prof.name)
        print(f"Adding prof: {prof_name}")
        try:
            data = schemas.GoogleScholar.parse_file(f"./data/{prof_name}.json")
            print(f"using cached {prof_name}")
        except Exception:
            data = scholarly.fill(next(scholarly.search_author(prof_name)))
            data = schemas.GoogleScholar.parse_obj(data)
            with open(f"./data/{prof_name}.json", "w+") as f:
                f.write(data.json())
        results = search(prof_name, num_results=10)

        prof.citations = data.citedby
        prof.scholar_id = data.scholar_id
        prof.save()

        print(f"Adding prof: {prof_name} citations")
        for year, citations in data.cites_per_year.items():
            models.Citation.objects.update_or_create(
                researcher=prof, year=datetime(year, 1, 1), count=citations
            )

        print(f"Adding prof: {prof_name} linkedin")
        for _ in range(10):
            link = next(results)
            if "linkedin.com" in urlparse(link).hostname:
                linkedin_url, _ = models.Website.objects.update_or_create(url=link)
                models.ResearcherWebsites.objects.update_or_create(
                    researcher=prof,
                    website=linkedin_url,
                    type=models.ResearcherWebsites.WebsiteType.LINKEDIN,
                )
                break

        print(f"Adding prof: {prof_name} image, interests and coauthors")
        image_url, _ = models.Website.objects.update_or_create(url=data.url_picture)
        models.ResearcherWebsites.objects.update_or_create(
            researcher=prof,
            website=image_url,
            type=models.ResearcherWebsites.WebsiteType.IMAGE,
        )

        prof.interests.add(
            *[
                models.Interest.objects.update_or_create(name=interest)[0]
                for interest in data.interests
            ]
        )
        prof.co_authors.add(
            *[
                models.Researcher.objects.update_or_create(
                    name=author.name, scholar_id=author.scholar_id
                )[0]
                for author in data.coauthors
            ]
        )

        print(f"Adding prof: {prof_name} publications")
        prof.publications.add(
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
        profs.Websites = profs.Websites.apply(
            lambda x: loads(x.replace("'", '"')) if isinstance(x, str) else None
        )

        faculty, _ = models.Faculty.objects.update_or_create(name="SCSE")

        print("Adding CSV Data")
        with transaction.atomic():
            for _i, name, email, dr_ntu, websites, dblp, citations in tqdm(
                profs.itertuples()
            ):
                researcher, _ = models.Researcher.objects.update_or_create(
                    name=alt_names.get(name, name),
                    email=email,
                    citations=citations if not isnan(citations) else None,
                    faculty=faculty,
                )
                dr_ntu, _ = models.Website.objects.update_or_create(url=dr_ntu)
                models.ResearcherWebsites.objects.update_or_create(
                    researcher=researcher,
                    website=dr_ntu,
                    type=models.ResearcherWebsites.WebsiteType.DR_NTU,
                )
                if isinstance(dblp, str):
                    dblp, _ = models.Website.objects.update_or_create(url=dblp)
                    models.ResearcherWebsites.objects.update_or_create(
                        researcher=researcher,
                        website=dblp,
                        type=models.ResearcherWebsites.WebsiteType.DBLP,
                    )
                if websites:
                    for website in websites:
                        website, _ = models.Website.objects.update_or_create(
                            url=website
                        )
                        models.ResearcherWebsites.objects.update_or_create(
                            researcher=researcher,
                            website=website,
                            type=models.ResearcherWebsites.WebsiteType.OTHER,
                        )

        profs = list(models.Researcher.objects.filter(name__in=list(profs.Name)))

        pool = Pool(processes=3)
        pool.map(self.get_prof_scholarly, profs)

        print("done")
