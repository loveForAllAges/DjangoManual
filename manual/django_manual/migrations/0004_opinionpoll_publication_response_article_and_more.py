# Generated by Django 4.2.7 on 2023-11-29 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_manual', '0003_alter_book_pubdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpinionPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_manual.opinionpoll')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=100)),
                ('publications', models.ManyToManyField(to='django_manual.publication')),
            ],
            options={
                'ordering': ['headline'],
            },
        ),
        migrations.CreateModel(
            name='TablespaceExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, db_tablespace='indexes', max_length=30)),
                ('data', models.CharField(db_index=True, max_length=255)),
                ('shortcut', models.CharField(max_length=7)),
                ('edges', models.ManyToManyField(db_tablespace='indexes', to='django_manual.tablespaceexample')),
            ],
            options={
                'db_tablespace': 'tables',
                'indexes': [models.Index(db_tablespace='other_indexes', fields=['shortcut'], name='django_manu_shortcu_90fa86_idx')],
            },
        ),
    ]
