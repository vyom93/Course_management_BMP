# Generated by Django 4.1.4 on 2023-06-21 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_courseprogram_unique_courseprogram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='id',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
    ]