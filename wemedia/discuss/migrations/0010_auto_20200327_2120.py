# Generated by Django 3.0.4 on 2020-03-27 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0009_auto_20200326_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]
