# Generated by Django 5.2.4 on 2025-07-07 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campsites", "0003_alter_campsiteimage_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="campsite",
            name="thumbnail_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="campsites.campsiteimage",
            ),
        ),
    ]
