# Generated by Django 3.0.6 on 2020-05-17 09:08

import cms.plugins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='name')),
            ],
            options={
                'verbose_name': 'collection',
                'verbose_name_plural': 'collections',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=120, verbose_name='text')),
                ('target', models.URLField(verbose_name='target')),
                ('color', cms.plugins.ColorField(blank=True, choices=[('red', 'red'), ('orange', 'orange'), ('yellow', 'yellow'), ('olive', 'olive'), ('green', 'green'), ('teal', 'teal'), ('violett', 'violett'), ('purple', 'purple'), ('pink', 'pink'), ('brown', 'brown'), ('grey', 'grey'), ('black', 'black')], max_length=20)),
                ('order', models.IntegerField(default=0)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='link_collections.Collection', verbose_name='Collection')),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
                'ordering': ['order'],
            },
        ),
    ]