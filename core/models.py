from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=20)
    id = models.CharField(primary_key=True, max_length=6)

    def __str__(self):
        return self.id;

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=20)
    course_name = models.CharField(max_length=80)
    course_credits = models.CharField(max_length=15)

    def __str__(self):
        return self.course_id;

class Faculty(models.Model):
    faculty_fname = models.CharField(primary_key=True, max_length=50)
    faculty_sname = models.CharField(max_length=10)

    def __str__(self):
        return self.faculty_fname;

class CourseOffered(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    year = models.IntegerField()
    sem = models.IntegerField()
    course_type = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'program_id', 'year', 'sem'], name='unique_courseOffered'),
        ]

    def __str__(self):
        return str(self.course_id) + "    " + str(self.program_id) + "    " + str(self.year) + "    " + str(self.sem);

class CourseFaculty(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.CharField(max_length=1)
    faculty_sname = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'section'], name='unique_courseFaculty'),
        ]

    def __str__(self):
        return str(self.course_id) + "    " + str(self.section) + "    " + str(self.faculty_sname);

class CourseSlots(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    slot = models.CharField(max_length=5)

    def __str__(self):
        return str(self.course_id);

class LectureTimetable(models.Model):
    course_id_t = models.CharField(primary_key=True, max_length=20)
    program_id_t = models.CharField(max_length=6)
    year_t = models.IntegerField()
    sem_t = models.IntegerField()
    course_type_t = models.CharField(max_length=30)
    section_t = models.IntegerField()
    faculty_sname_t = models.CharField(max_length=20)
    slot_t = models.CharField(max_length=5)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id_t', 'program_id_t', 'year_t', 'sem_t', 'course_type_t', 'section_t', 'faculty_sname_t', 'slot_t'], name='unique_courseTimetable'),
        ]

    def __str__(self):
        return str(self.course_id_t) + "    " + str(self.program_id_t) + "    " + str(self.year_t) + "    " + str(self.sem_t) + "    " + str(self.course_type_t)+ "    " + str(self.section_t) + "    " + str(self.faculty_sname_t) + "    " + str(self.slot_t);

class Acad_year(models.Model):
    sem_id = models.CharField(max_length=10)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    year = models.IntegerField()
    section = models.CharField(max_length=1)
    faculty_sname = models.CharField(max_length=30)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['sem_id', 'course_id', 'program_id', 'year', 'section'], name='unique_sem'),
        ]

    def __str__(self):
        return str(self.sem_id) + "    " + str(self.course_id) + "    " + str(self.program_id.id) + "    " + str(self.year) + "    " + str(self.section) + "    " + str(self.faculty_sname);


