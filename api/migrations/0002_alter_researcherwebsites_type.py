# Generated by Django 4.1.2 on 2022-10-28 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="researcherwebsites",
            name="type",
            field=models.TextField(
                choices=[
                    ("dr_ntu", "Dr Ntu"),
                    ("dblp", "Dblp"),
                    ("image", "Image"),
                    ("linkedin", "Linkedin"),
                    ("other", "Other"),
                ]
            ),
        ),
    ]
