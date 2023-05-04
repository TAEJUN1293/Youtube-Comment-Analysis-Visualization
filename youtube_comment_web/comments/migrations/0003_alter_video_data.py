# Generated by Django 4.1.7 on 2023-05-04 04:52

import comments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0002_alter_video_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="data",
            field=models.JSONField(
                default={}, validators=[comments.models.validate_json_format]
            ),
        ),
    ]
