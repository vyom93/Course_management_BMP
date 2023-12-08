# Generated by Django 4.1.4 on 2023-07-09 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_timetable_course_id_alter_timetable_program_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureTimetable',
            fields=[
                ('course_id_t', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('program_id_t', models.CharField(max_length=6)),
                ('year_t', models.IntegerField()),
                ('sem_t', models.IntegerField()),
                ('course_type_t', models.CharField(max_length=30)),
                ('section_t', models.IntegerField()),
                ('faculty_sname_t', models.CharField(max_length=20)),
                ('slot_t', models.CharField(max_length=5)),
            ],
        ),
        migrations.DeleteModel(
            name='Timetable',
        ),
        migrations.AddConstraint(
            model_name='lecturetimetable',
            constraint=models.UniqueConstraint(fields=('course_id_t', 'program_id_t', 'year_t', 'sem_t', 'course_type_t', 'section_t', 'faculty_sname_t', 'slot_t'), name='unique_courseTimetable'),
        ),
    ]