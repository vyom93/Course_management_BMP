from django.contrib import admin
from .models import Program, Course, Faculty, CourseOffered, CourseFaculty, CourseSlots, LectureTimetable, Acad_year

# Register your models here.
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(CourseOffered)
admin.site.register(CourseFaculty)
admin.site.register(CourseSlots)
admin.site.register(LectureTimetable)
admin.site.register(Acad_year)
admin.site.site_header = 'Timetable Generator'