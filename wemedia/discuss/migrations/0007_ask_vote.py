# Generated by Django 3.0.7 on 2020-07-02 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0006_auto_20200630_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='ask',
            name='vote',
            field=models.IntegerField(default=0),
        ),
    ]
