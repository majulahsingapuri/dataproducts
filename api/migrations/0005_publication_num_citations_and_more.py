# Generated by Django 4.1.2 on 2022-10-29 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_researcher_publications"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="num_citations",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="publication",
            name="paper_url",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="api.website"
            ),
        ),
        migrations.AlterField(
            model_name="publication",
            name="year",
            field=models.DateField(null=True),
        ),
    ]
