# Generated by Django 2.1.15 on 2021-10-30 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ingredients'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
    ]
