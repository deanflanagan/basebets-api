# Generated by Django 3.2 on 2021-04-26 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210425_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='viewset',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]
