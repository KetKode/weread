# Generated by Django 4.2.5 on 2023-10-10 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers'),
        ),
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.CharField(blank=True, help_text='Summary of the book', max_length=2000, null=True),
        ),
    ]