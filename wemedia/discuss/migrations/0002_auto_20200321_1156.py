# Generated by Django 3.0.4 on 2020-03-21 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discuss', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_id', models.IntegerField()),
                ('to_id', models.IntegerField()),
                ('relation_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='desciption',
            new_name='description',
        ),
    ]
