# Generated by Django 4.1.2 on 2022-10-31 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_alter_researcher_email_alter_researcher_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="group",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
