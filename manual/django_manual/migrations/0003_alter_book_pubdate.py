# Generated by Django 4.2.7 on 2023-11-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_manual', '0002_author_book_publisher_store_book_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pubdate',
            field=models.DateField(auto_now_add=True),
        ),
    ]
