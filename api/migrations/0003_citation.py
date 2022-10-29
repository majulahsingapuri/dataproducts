# Generated by Django 4.1.2 on 2022-10-28 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_researcherwebsites_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Citation",
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
                ("year", models.DateField()),
                ("count", models.PositiveIntegerField()),
                (
                    "researcher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.researcher"
                    ),
                ),
            ],
        ),
    ]