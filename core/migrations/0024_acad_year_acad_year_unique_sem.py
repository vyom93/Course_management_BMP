# Generated by Django 4.1.4 on 2023-11-14 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_autumn_one_faculty_sname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acad_year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem_id', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
                ('section', models.CharField(max_length=1)),
                ('faculty_sname', models.CharField(max_length=30)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('program_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.program')),
            ],
        ),
        migrations.AddConstraint(
            model_name='acad_year',
            constraint=models.UniqueConstraint(fields=('sem_id', 'course_id', 'program_id', 'year', 'section'), name='unique_sem'),
        ),
    ]
