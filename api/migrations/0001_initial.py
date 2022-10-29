# Generated by Django 4.1.2 on 2022-10-28 09:51

import django.contrib.postgres.indexes
import django.db.models.deletion
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        TrigramExtension(),
        migrations.CreateModel(
            name="Conference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Interest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Researcher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("email", models.EmailField(max_length=254, null=True)),
                ("citations", models.PositiveIntegerField(null=True)),
                ("scholar_id", models.TextField()),
                ("co_authors", models.ManyToManyField(to="api.researcher")),
                (
                    "faculty",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="api.faculty",
                    ),
                ),
                ("interests", models.ManyToManyField(to="api.interest")),
            ],
        ),
        migrations.CreateModel(
            name="Website",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="ResearcherWebsites",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.TextField(
                        choices=[
                            ("dr_ntu", "Dr Ntu"),
                            ("dblp", "Dblp"),
                            ("image", "Image"),
                            ("other", "Other"),
                        ]
                    ),
                ),
                (
                    "researcher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.researcher"
                    ),
                ),
                (
                    "website",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.website"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Publication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField()),
                ("year", models.DateField()),
                ("abstract", models.TextField()),
                (
                    "conference",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.conference",
                    ),
                ),
                (
                    "paper_url",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.website"
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="interest",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["name"],
                name="interest_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ),
        migrations.AddIndex(
            model_name="conference",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["name"],
                name="conference_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ),
        migrations.AddIndex(
            model_name="researcher",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["name"],
                name="researcher_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ),
        migrations.AddIndex(
            model_name="publication",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["title"],
                name="publication_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ),
    ]
