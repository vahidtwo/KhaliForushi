# Generated by Django 4.2 on 2024-12-27 21:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("option", "0003_coverdcalloptions_strick_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coverdcalloptions",
            name="cover_call",
            field=models.FloatField(),
        ),
    ]
