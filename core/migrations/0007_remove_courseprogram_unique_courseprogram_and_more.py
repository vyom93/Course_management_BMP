# Generated by Django 4.1.4 on 2023-06-07 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_program_id_courseprogram_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='courseprogram',
            name='unique_courseProgram',
        ),
        migrations.AddConstraint(
            model_name='courseprogram',
            constraint=models.UniqueConstraint(fields=('course_id', 'program_id', 'effective_from'), name='unique_courseProgram'),
        ),
    ]
