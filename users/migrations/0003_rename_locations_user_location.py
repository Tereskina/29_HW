# Generated by Django 4.1.7 on 2023-03-10 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_location_user_locations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='locations',
            new_name='location',
        ),
    ]
