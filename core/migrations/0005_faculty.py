# Generated by Django 4.1.4 on 2023-06-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_course_course_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty_fname', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('faculty_sname', models.CharField(max_length=10)),
            ],
        ),
    ]
