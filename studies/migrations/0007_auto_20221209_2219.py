# Generated by Django 3.2.13 on 2022-12-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0006_studynotice_study'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='title',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='studynotice',
            name='content',
            field=models.CharField(max_length=50),
        ),
    ]
