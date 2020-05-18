# Generated by Django 3.0.6 on 2020-05-17 09:08

import cms.plugins
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import feincms3.cleanse
import imagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_key', models.CharField(choices=[('default', 'Default')], default='default', max_length=100, verbose_name='template')),
                ('language_code', models.CharField(choices=[('de', 'German'), ('fr', 'French'), ('it', 'Italian')], default='de', max_length=10, verbose_name='language')),
                ('meta_title', models.CharField(blank=True, help_text='Used for Open Graph and other meta tags.', max_length=200, verbose_name='title')),
                ('meta_description', models.TextField(blank=True, help_text='Override the description for this page.', verbose_name='description')),
                ('meta_image', imagefield.fields.ImageField(blank=True, height_field='meta_image_height', help_text='Set the Open Graph image.', upload_to='meta/%Y/%m', verbose_name='image', width_field='meta_image_width')),
                ('meta_canonical', models.URLField(blank=True, help_text='If you need this you probably know.', verbose_name='canonical URL')),
                ('meta_author', models.CharField(blank=True, help_text='Override the author meta tag.', max_length=200, verbose_name='author')),
                ('meta_robots', models.CharField(blank=True, help_text='Override the robots meta tag.', max_length=200, verbose_name='robots')),
                ('meta_image_width', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('meta_image_height', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('meta_image_ppoi', imagefield.fields.PPOIField(default='0.5x0.5', max_length=20)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(max_length=180, verbose_name='slug')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('edited_date', models.DateTimeField(auto_now=True, verbose_name='edited at')),
                ('image', imagefield.fields.ImageField(blank=True, height_field='image_height', null=True, upload_to='', verbose_name='header image', width_field='image_width')),
                ('image_width', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('image_height', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('image_ppoi', imagefield.fields.PPOIField(default='0.5x0.5', max_length=20)),
            ],
            options={
                'ordering': ['-publication_date'],
                'get_latest_by': 'publication_date',
            },
        ),
        migrations.CreateModel(
            name='ArticlePlugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=180, verbose_name='title')),
                ('count', models.IntegerField(default=3, verbose_name='count')),
                ('template_key', models.CharField(choices=[('blog/plugins/default.html', 'default'), ('blog/plugins/simple_list.html', 'list')], default='blog/plugin_default.html', max_length=100)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'article plugin',
                'verbose_name_plural': 'article plugins',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=240, verbose_name='text')),
                ('color', cms.plugins.ColorField(blank=True, choices=[('red', 'red'), ('orange', 'orange'), ('yellow', 'yellow'), ('olive', 'olive'), ('green', 'green'), ('teal', 'teal'), ('violett', 'violett'), ('purple', 'purple'), ('pink', 'pink'), ('brown', 'brown'), ('grey', 'grey'), ('black', 'black')], max_length=20)),
                ('style', models.CharField(blank=True, choices=[('', 'none'), ('secondary', 'secondary')], default='', max_length=20, verbose_name='style')),
                ('align', models.CharField(blank=True, choices=[('', 'default'), ('center', 'center'), ('right', 'right'), ('block', 'block')], max_length=30, verbose_name='alignment')),
                ('line_break', models.BooleanField(default=True, verbose_name='break')),
                ('target', models.CharField(max_length=800, verbose_name='target')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(choices=[('de', 'German'), ('fr', 'French'), ('it', 'Italian')], default='de', max_length=10, verbose_name='language')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('image', imagefield.fields.ImageField(blank=True, height_field='image_height', null=True, upload_to='', verbose_name='header image', width_field='image_width')),
                ('image_width', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('image_height', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('image_ppoi', imagefield.fields.PPOIField(default='0.5x0.5', max_length=20)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='EventPlugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=180, verbose_name='title')),
                ('count', models.IntegerField(default=3, verbose_name='count')),
                ('template_key', models.CharField(choices=[('events/plugins/default.html', 'default')], default='events/plugins/default.html', max_length=100)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'event plugin',
                'verbose_name_plural': 'event plugins',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(choices=[('de', 'German'), ('fr', 'French'), ('it', 'Italian')], default='de', max_length=10, verbose_name='language')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'name space',
                'verbose_name_plural': 'name spaces',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='RichText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', feincms3.cleanse.CleansedRichTextField(verbose_name='text')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_richtext_set', to='blog.Article')),
            ],
            options={
                'verbose_name': 'rich text',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagefield.fields.ImageField(height_field='height', upload_to='images/%Y/%m', verbose_name='image', width_field='width')),
                ('width', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='image width')),
                ('height', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='image height')),
                ('ppoi', imagefield.fields.PPOIField(default='0.5x0.5', max_length=20, verbose_name='primary point of interest')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('caption', models.CharField(blank=True, max_length=200, verbose_name='caption')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='title')),
                ('fullwidth', models.BooleanField(default=False, verbose_name='full width')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_image_set', to='blog.Article')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='HTML',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html', models.TextField(help_text='The content will be inserted directly into the page. It is VERY important that the HTML snippet is well-formed!', verbose_name='HTML')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_html_set', to='blog.Article')),
            ],
            options={
                'verbose_name': 'HTML',
                'verbose_name_plural': 'HTML',
            },
        ),
        migrations.CreateModel(
            name='External',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_external_set', to='blog.Article')),
            ],
            options={
                'verbose_name': 'external',
            },
        ),
    ]
