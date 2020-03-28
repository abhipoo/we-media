# Generated by Django 3.0.4 on 2020-03-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0008_auto_20200324_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='creator',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='related_content',
            field=models.ManyToManyField(blank=True, related_name='_content_related_content_+', to='discuss.content'),
        ),
    ]
