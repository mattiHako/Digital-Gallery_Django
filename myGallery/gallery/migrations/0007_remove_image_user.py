# Generated by Django 5.0.3 on 2024-04-01 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_alter_image_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
    ]
