# Generated by Django 4.2 on 2024-12-27 21:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("option", "0002_auto_20241227_2108"),
    ]

    operations = [
        migrations.AddField(
            model_name="coverdcalloptions",
            name="strick_price",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
