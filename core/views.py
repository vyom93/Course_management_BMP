from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core.models import Program, Course, Faculty, CourseOffered, CourseFaculty, CourseSlots, LectureTimetable, Acad_year
from csv import DictReader
from django.core.management import BaseCommand
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q
from django.contrib import messages
import sqlite3
import time
import csv

# Create your views here.

################################ HOME ################################
def home(request):
    return render(request, 'home.html')

################################ PROGRAM MASTER ################################

def program_master(request):
    showall=Program.objects.all().order_by('id')
    return render(request, 'program_master.html',{"data":showall})

def insert_program(request):
    if request.method=="POST":
        if request.POST.get('id') and request.POST.get('name'):
            saverecord=Program()
            saverecord.id=request.POST.get('id')
            saverecord.name=request.POST.get('name')
            saverecord.save()
            messages.success(request,'Program '+saverecord.name+ ' with ID '+saverecord.id+ ' is saved successfully..!')
            return render(request,'insert_program.html')
    else :
        return render(request,'insert_program.html')

def edit_program(request,id):
    editprogramobj=Program.objects.get(id=id)
    return render(request,'edit_program.html',{"Program":editprogramobj})

def update_program(request,id):
    program = Program.objects.filter(name=id).update(id=request.POST.get('program_id'))
    time.sleep(5)
    return render(request, 'edit_program.html',{"Program":program})

################################ SCHEME ################################
def scheme(request,id):
    # current_database_name = settings.DATABASES['default']['NAME']
    # cursor = connection.cursor()
    # cursor.execute("select Course.course_name,Course.course_credits,CourseOffered.year,CourseOffered.sem from CourseOffered left join Course on Course.course_id=CourseOffered.course_id")
    temp=CourseOffered.objects.filter(program_id=id)
    data_list=[]
    year_list=[]
    for i in temp :
        temp2=Course.objects.get(course_id=i.course_id)
        data_list.append((temp2.course_name,temp2.course_credits,i.year,i.sem))

    # for item1,item2 in zip(data_list,year_list):
    #     print(item1,item2)
    context = {
        'data_list': data_list,
        # 'year_list': year_list,
    }
    showall=Program.objects.all().order_by('id')
    return render(request, 'scheme.html',context)

    

################################ COURSE MASTER ################################

def course_master(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                course=Course(course_id=row[0], course_name=row[1], course_credits=row[2])  
                if(Course.objects.filter(course_id=row[0]).exists()):
                    Course.objects.filter(course_id=row[0]).update(course_name=row[1], course_credits=row[2])
                else:
                    course.save()
            messages.success(request,'File imported successfully..!')
            time.sleep(3)

    showall=Course.objects.all().order_by('course_id')
    return render(request, 'course_master.html',{"data":showall})

def search_course(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query':
                search_query = value

        # Print the search query to the console
        # print(f"Search Query: {search_query}")

        
        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()

        # Retrieve the desired columns from the tables
        cursor.execute('SELECT course_id FROM core_course WHERE course_id LIKE ?', ('%' + search_query + '%',))
        searched_courses = cursor.fetchall()
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()
        showall = Course.objects.filter(course_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_master.html',{"data":showall})
    else:
        return render(request, 'course_master.html') 

def insert_course(request):
    if request.method=="POST":
        if request.POST.get('course_id') and request.POST.get('course_name') and request.POST.get('course_credits'):
            saverecord=Course()
            saverecord.course_id=request.POST.get('course_id')
            saverecord.course_name=request.POST.get('course_name')
            saverecord.course_credits=request.POST.get('course_credits')
            saverecord.save()
            messages.success(request,'Course "'+saverecord.course_name+ '" with Course No. "'+saverecord.course_id+ '" is saved successfully..!')
            return render(request,'insert_course.html')
    else :
        return render(request,'insert_course.html')

def edit_course(request, id):
    editcourseobj=Course.objects.get(course_id=id)
    return render(request,'edit_course.html',{"Course":editcourseobj})

def update_course(request, id):
    course = Course.objects.filter(course_id=id).update(course_name=request.POST.get('course_name'), course_credits=request.POST.get('course_credits'))
    time.sleep(5)
    return render(request, 'edit_course.html',{"Course":course})

# def delete_course(request, id):
#     Course.objects.filter(course_id=id).delete()
#     showall = Course.objects.all().order_by('course_id')
    # return render(request, 'course_master.html',{"data":showall})



################################ FACULTY MASTER ################################

def faculty_master(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                faculty=Faculty(faculty_fname=row[0], faculty_sname=row[1])  
                if(Faculty.objects.filter(faculty_fname=row[0]).exists()):
                    Faculty.objects.filter(faculty_fname=row[0]).update(faculty_sname=row[1])
                else:
                    faculty.save()
            messages.success(request,'File imported successfully..!')
            time.sleep(3)
    
    showall=Faculty.objects.all().order_by('faculty_fname')
    return render(request, 'faculty_master.html',{"data":showall})

def insert_faculty(request):
    if request.method=="POST":
        if request.POST.get('faculty_fname') and request.POST.get('faculty_sname'):
            saverecord=Faculty()
            saverecord.faculty_fname=request.POST.get('faculty_fname')
            saverecord.faculty_sname=request.POST.get('faculty_sname')
            saverecord.save()
            messages.success(request,'Faculty "'+saverecord.faculty_fname+ '" with short name "'+saverecord.faculty_sname+ '" is saved successfully..!')
            return render(request,'insert_faculty.html')
    else :
        return render(request,'insert_faculty.html')

def edit_faculty(request, id):
    editfacultyobj=Faculty.objects.get(faculty_fname=id)
    return render(request,'edit_faculty.html',{"Faculty":editfacultyobj})

def update_faculty(request, id):
    faculty = Faculty.objects.filter(faculty_fname=id).update(faculty_sname=request.POST.get('faculty_sname'))
    time.sleep(5)
    return render(request, 'edit_faculty.html',{"Faculty":faculty})

def available_faculty_autumn1(request):
    
    connection=sqlite3.connect('courses-2023.db')
    cursor=connection.cursor()

    cursor.execute('SELECT faculty_sname FROM core_faculty except SELECT faculty_sname from core_acad_year where sem_id="AS1"')
    # cursor.execute('SELECT faculty_fname, faculty_sname FROM core_faculty where faculty_sname NOT IN ( SELECT f.faculty_sname FROM core_faculty f JOIN core_autumn_one a ON f.faculty_sname = a.faculty_sname ')
    
    searched_data = cursor.fetchall()
    for i in range(len(searched_data)):
        searched_data[i] = searched_data[i][0]
        print(searched_data[i])

    connection.close()

    showall=Faculty.objects.filter(faculty_sname__in = searched_data).order_by('faculty_fname')
    return render(request, 'faculty_master.html',{"data":showall})

def available_faculty_autumn2(request):
    
    connection=sqlite3.connect('courses-2023.db')
    cursor=connection.cursor()

    cursor.execute('SELECT faculty_sname FROM core_faculty except SELECT faculty_sname from core_acad_year where sem_id="AS2"')
    # cursor.execute('SELECT faculty_fname, faculty_sname FROM core_faculty where faculty_sname NOT IN ( SELECT f.faculty_sname FROM core_faculty f JOIN core_autumn_one a ON f.faculty_sname = a.faculty_sname ')
    
    searched_data = cursor.fetchall()
    for i in range(len(searched_data)):
        searched_data[i] = searched_data[i][0]
        print(searched_data[i])

    connection.close()

    showall=Faculty.objects.filter(faculty_sname__in = searched_data).order_by('faculty_fname')
    return render(request, 'faculty_master.html',{"data":showall})

def available_faculty_winter1(request):
    
    connection=sqlite3.connect('courses-2023.db')
    cursor=connection.cursor()

    cursor.execute('SELECT faculty_sname FROM core_faculty except SELECT faculty_sname from core_acad_year where sem_id="WS1"')
    # cursor.execute('SELECT faculty_fname, faculty_sname FROM core_faculty where faculty_sname NOT IN ( SELECT f.faculty_sname FROM core_faculty f JOIN core_autumn_one a ON f.faculty_sname = a.faculty_sname ')
    
    searched_data = cursor.fetchall()
    print(searched_data)

    for i in range(len(searched_data)):
        searched_data[i] = searched_data[i][0]
        print(searched_data[i])

    connection.close()

    showall=Faculty.objects.filter(faculty_sname__in = searched_data).order_by('faculty_fname')
    return render(request, 'faculty_master.html',{"data":showall})

################################ COURSES OFFERED ################################

def course_offered(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                course = Course.objects.get(course_id=row[0])
                program = Program.objects.get(id=row[1])
                year = row[2]
                sem = row[3]
                course_type = row[4]

                courseoffered=CourseOffered(course_id=course, program_id=program, year=year, sem=sem, course_type=course_type)  
                if(CourseOffered.objects.filter(course_id=course, program_id=program, year=row[2], sem=row[3]).exists()):
                    CourseOffered.objects.filter(course_id=course, program_id=program, year=row[2], sem=row[3]).update(course_type=row[4])
                else:
                    courseoffered.save()
            messages.success(request,'File imported successfully..!')
            time.sleep(3)
    
    showall=CourseOffered.objects.all().order_by('course_id')
    return render(request, 'course_offered.html',{"data":showall})

def insert_course_offered(request):
    if request.method=="POST":
        if request.POST.get('course_id') and request.POST.get('program_id') and request.POST.get('year') and request.POST.get('sem') and request.POST.get('course_type'):
            course_id = request.POST.get('course_id')
            program_id = request.POST.get('program_id')
            year = request.POST.get('year')
            sem = request.POST.get('sem')
            course_type = request.POST.get('course_type')

            course = get_object_or_404(Course, course_id=course_id)
            program = get_object_or_404(Program, id=program_id)

            saverecord = CourseOffered(course_id=course, program_id=program, year=year, sem=sem, course_type=course_type)
            saverecord.save()
            
            # saverecord=CourseOffered()
            # saverecord.course_id=request.POST.get('course_id')
            # saverecord.program_id=request.POST.get('program_id')
            # saverecord.year=request.POST.get('year')
            # saverecord.sem=request.POSt.get('sem')
            # saverecord.course_type=request.POST.get('course_type')
            # saverecord.save()
            messages.success(request,'Course "'+str(saverecord.course_id)+ '" is offered in "Year ' + str(saverecord.year)+ ' Semester ' + str(saverecord.sem)+ ' ".')
            return render(request,'insert_course_offered.html')
    else :
        return render(request,'insert_course_offered.html')

def search_program(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query':
                search_query = value

        # Print the search query to the console
        # print(f"Search Query: {search_query}")

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()

        # Retrieve the desired columns from the tables
        cursor.execute('SELECT program_id_id FROM core_courseoffered WHERE program_id_id = ?', (search_query,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()
        showall = CourseOffered.objects.filter(program_id_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_offered.html',{"data":showall})
    else:
        return render(request, 'course_offered.html') 

################################ FACULTY ASSIGNMENT ################################

def course_faculty(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                print(row[0])
                
                course = Course.objects.get(course_id=row[0])
                coursefaculty=CourseFaculty(course_id=course, section=row[1], faculty_sname=row[2])  
                if(CourseFaculty.objects.filter(course_id=row[0], section=row[1]).exists()):
                    CourseFaculty.objects.filter(course_id=row[0], section=row[1]).update(faculty_sname=row[2])
                else:
                    coursefaculty.save()
            messages.success(request,'File imported successfully..!')
            time.sleep(3)
    
    showall=CourseFaculty.objects.all().order_by('course_id')
    return render(request, 'course_faculty.html',{"data":showall})

def insert_course_faculty(request):
    if request.method=="POST":
        if request.POST.get('course_id') and request.POST.get('section') and request.POST.get('faculty_sname'):
            course_id = request.POST.get('course_id')
            section = request.POST.get('section')
            faculty_sname = request.POST.get('faculty_sname')

            course = get_object_or_404(Course, course_id=course_id)
            saverecord = CourseFaculty(course_id=course, section=section, faculty_sname=faculty_sname)
            saverecord.save()

            # saverecord=CourseFaculty()
            # saverecord.course_id=request.POST.get('course_id')
            # saverecord.section=request.POST.get('section')
            # saverecord.faculty_sname=request.POST.get('faculty_sname')
            # saverecord.save()
            messages.success(request,'Course "'+str(saverecord.course_id)+ '" is assigned to " ' + str(saverecord.faculty_sname)+ ' ".')
            return render(request,'insert_course_faculty.html')
    else :
        return render(request,'insert_course_faculty.html')

def search_faculty(request):
    if request.method=="GET":
        query=request.META['QUERY_STRING']
        query_params=query.split('&')
        search_query=''

        for param in query_params:
            key,value=param.split('=')
            if key=='search_query':
                search_query=value

        connection=sqlite3.connect('courses-2023.db')
        cursor=connection.cursor()

        cursor.execute('SELECT * FROM core_coursefaculty WHERE faculty_sname LIKE ?',(search_query,))
        searched_data = cursor.fetchall()
        # print(searched_data)
        for i in range(len(searched_data)):
            searched_data[i] = searched_data[i][2]
            print(searched_data[i])

        connection.close()
        showall = CourseFaculty.objects.filter(faculty_sname__in=searched_data).order_by('course_id')
        print(showall)
        return render(request, 'course_faculty.html',{"data":showall})
    else:
        return render(request, 'course_faculty.html')

################################ Electives ################################

def electives(request):
    connection=sqlite3.connect('courses-2023.db')
    cursor=connection.cursor()

    cursor.execute('SELECT * FROM core_courseoffered WHERE course_type!= ?',('Core',))
    searched_data = cursor.fetchall()
    print(searched_data)
    for i in range(len(searched_data)):
        searched_data[i] = searched_data[i][4]
        print(searched_data[i])

    connection.close()

    showall=CourseOffered.objects.filter(course_id__in=searched_data).order_by('course_id')
    return render(request, 'electives.html',{"data":showall})

def search_elective(request):
    if request.method=="GET":
        query=request.META['QUERY_STRING']
        query_params=query.split('&')
        search_query=''

        for param in query_params:
            key,value=param.split('=')
            if key=='search_query':
                search_query=value

        connection=sqlite3.connect('courses-2023.db')
        cursor=connection.cursor()

        cursor.execute('SELECT * FROM core_courseoffered WHERE course_id_id= ?',(search_query,))
        searched_data = cursor.fetchall()
        print(searched_data)
        for i in range(len(searched_data)):
            searched_data[i] = searched_data[i][4]
            print(searched_data[i])

        connection.close()
        showall = CourseOffered.objects.filter(course_id_id__in=searched_data).order_by('course_id')
        print(showall)
        return render(request, 'electives.html',{"data":showall})
    else:
        return render(request, 'electives.html') 

################################ SLOT ASSIGNMENT ################################

def slots(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                course = Course.objects.get(course_id=row[0])
                slots=CourseSlots(course_id=course, slot=row[1])

                if(CourseSlots.objects.filter(course_id=row[0]).exists()):
                    CourseSlots.objects.filter(course_id=row[0]).update(slot=row[1])
                else:
                    slots.save()

            messages.success(request,'File imported successfully..!')
            time.sleep(3)
    
    showall=CourseSlots.objects.all().order_by('course_id')
    return render(request, 'slots.html',{"data":showall})

def insert_slot(request):
    if request.method=="POST":
        if request.POST.get('course_id') and request.POST.get('slot'):
            course_id = request.POST.get('course_id')
            slot = request.POST.get('slot')

            course = get_object_or_404(Course, course_id=course_id)
            saverecord = CourseSlots(course_id=course, slot=slot)
            saverecord.save()

            # saverecord=CourseSlots()
            # saverecord.course_id=request.POST.get('course_id')
            # saverecord.slot=request.POST.get('slot')
            # saverecord.save()
            messages.success(request,'Slot "'+str(saverecord.slot)+ '" is assigned to " ' + str(saverecord.course_id)+ ' ".')
            return render(request,'insert_slot.html')
    else :
        return render(request,'insert_slot.html')

def edit_slot(request,id):
    editslotobj=CourseSlots.objects.get(course_id=id)
    return render(request,'edit_slot.html',{"CourseSlots":editslotobj})

def update_slot(request,id):
    slot = CourseSlots.objects.filter(course_id=id).update(slot=request.POST.get('slot'))
    time.sleep(5)
    return render(request, 'edit_slot.html',{"CourseSlots":slot})

def search_slot(request):
    if request.method=="GET":
        query=request.META['QUERY_STRING']
        query_params=query.split('&')
        search_query=''

        for param in query_params:
            key,value=param.split('=')
            if key=='search_query':
                search_query=value

        connection=sqlite3.connect('courses-2023.db')
        cursor=connection.cursor()

        cursor.execute('SELECT * FROM core_courseslots WHERE slot LIKE ?',('%'+search_query+'%',))
        searched_data = cursor.fetchall()
        # print(searched_data)
        for i in range(len(searched_data)):
            searched_data[i] = searched_data[i][2]
            print(searched_data[i])

        connection.close()
        showall = CourseSlots.objects.filter(course_id__in=searched_data).order_by('course_id')
        print(showall)
        return render(request, 'slots.html',{"data":showall})
    else:
        return render(request, 'slots.html') 


################################ TIMETABLE GENERATION ################################
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Timetable.csv"'

    # Connect to the SQLite3 database
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()

    # Retrieve the desired columns from the tables
    cursor.execute('SELECT course_id_t FROM core_lecturetimetable')
    table1_column = cursor.fetchall()

    cursor.execute('SELECT program_id_t FROM core_lecturetimetable')
    table2_column = cursor.fetchall()

    cursor.execute('SELECT year_t FROM core_lecturetimetable')
    table3_column = cursor.fetchall()

    cursor.execute('SELECT sem_t FROM core_lecturetimetable')
    table4_column = cursor.fetchall()

    cursor.execute('SELECT course_type_t FROM core_lecturetimetable')
    table5_column = cursor.fetchall()

    cursor.execute('SELECT section_t FROM core_lecturetimetable')
    table6_column = cursor.fetchall()

    cursor.execute('SELECT faculty_sname_t FROM core_lecturetimetable')
    table7_column = cursor.fetchall()

    cursor.execute('SELECT slot_t FROM core_lecturetimetable')
    table8_column = cursor.fetchall()

    # Generate the CSV content
    writer = csv.writer(response)
    writer.writerow(['Course ID', 'Program ID', 'Year', 'Semester', 'Course Type', 'Section', 'Faculty', 'Slot'])
    #trim Faculty name from ("'faculty_name',") to ('faculty_name')
    for i in range(len(table1_column)):
        table1_column[i] = table1_column[i][0]
    for i in range(len(table2_column)):
        table2_column[i] = table2_column[i][0]
    for i in range(len(table3_column)):
        table3_column[i] = table3_column[i][0]
    for i in range(len(table4_column)):
        table4_column[i] = table4_column[i][0]
    for i in range(len(table5_column)):
        table5_column[i] = table5_column[i][0]
    for i in range(len(table6_column)):
        table6_column[i] = table6_column[i][0]
    for i in range(len(table7_column)):
        table7_column[i] = table7_column[i][0]
    for i in range(len(table8_column)):
        table8_column[i] = table8_column[i][0]
    
    print(table7_column)
    writer.writerows(zip(table1_column, table2_column, table3_column, table4_column, table5_column, table6_column, table7_column, table8_column))

    # Close the database connection
    connection.close()

    return response

def timetable(request):
    # Connect to the SQLite3 database
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT core_courseoffered.course_id_id, core_courseoffered.program_id_id, core_courseoffered.year, core_courseoffered.sem, core_courseoffered.course_type, core_coursefaculty.faculty_sname, core_coursefaculty.section, core_courseslots.slot FROM core_courseslots INNER JOIN core_courseoffered ON core_courseslots.course_id_id = core_courseoffered.course_id_id INNER JOIN core_coursefaculty ON core_courseoffered.course_id_id = core_coursefaculty.course_id_id ORDER BY core_courseoffered.course_id_id")
    row = cursor.fetchall()
    for i in row:
        # print(i)
        # print('\n')
        saverecord = LectureTimetable(course_id_t=i[0], program_id_t=i[1], year_t=i[2], sem_t=i[3], course_type_t=i[4], faculty_sname_t=i[5], section_t=i[6], slot_t=i[7])
        print(saverecord)
        saverecord.save()

    showall=LectureTimetable.objects.all().order_by('course_id_t')
    return render(request, 'timetable.html',{"data":showall})  

################################ AUTUMN ONE ################################

def autumn1(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                course_id = row[0]
                program_id = row[1]
                year = row[2]
                section = row[3]
                faculty_sname = row[4]
                sem_id = row[5]
                
                print(course_id, program_id, year, section, faculty_sname, sem_id)
                try:
                    if sem_id == 'AS1':
                        course = Course.objects.get(course_id=course_id)
                        program = Program.objects.get(id=program_id)

                        if Acad_year.objects.filter(
                            course_id=course,
                            program_id=program,
                            year=year,
                            section=section,
                            sem_id=sem_id
                        ).exists():
                            Acad_year.objects.filter(
                                course_id=course,
                                program_id=program,
                                year=year,
                                section=section,
                                sem_id=sem_id
                            ).update(faculty_sname=faculty_sname)
                        else:
                            Acad_year.objects.create(
                                course_id=course,
                                program_id=program,
                                year=year,
                                section=section,
                                faculty_sname=faculty_sname,
                                sem_id=sem_id
                            )

                except Course.DoesNotExist:
                    messages.error(request, f'Course with course_id {course_id} does not exist')
                except Program.DoesNotExist:
                    messages.error(request, f'Program with id {program_id} does not exist')

            messages.success(request, 'File imported successfully..!')
            time.sleep(3)

    showall = Acad_year.objects.filter(sem_id='AS1').order_by('course_id')
    # print(showall)
    return render(request, 'autumn1/autumn1.html', {"data": showall})

def insert_autumn1(request):
    if request.method=="POST":
        if request.POST.get('course_id') and request.POST.get('program_id') and request.POST.get('year') and request.POST.get('section') and request.POST.get('faculty_sname'):
            # print("1")
            course_id = request.POST.get('course_id')
            program_id = request.POST.get('program_id')
            year = request.POST.get('year')
            section = request.POST.get('section')
            faculty_sname = request.POST.get('faculty_sname')

            course = get_object_or_404(Course, course_id=course_id)
            program = get_object_or_404(Program, id=program_id)
            faculty = get_object_or_404(Faculty, faculty_sname=faculty_sname)

            saverecord=Acad_year(sem_id='AS1', course_id=course, program_id=program, year=year, section=section, faculty_sname=faculty)
            saverecord.save()
            messages.success(request,'Course "'+str(saverecord.course_id)+ '" is saved successfully in Autumn1..!')
            return render(request,'autumn1/insert_autumn1.html')
    else :
        return render(request,'autumn1/insert_autumn1.html')
    
def edit_autumn1(request,id):
    parsed_list = id.split('+')
    print(parsed_list)
    editautumn1obj=Acad_year.objects.get(course_id=parsed_list[0],program_id=parsed_list[1], year=parsed_list[2], section=parsed_list[3], sem_id='AS1')
    return render(request,'autumn1/edit_autumn1.html',{"Acad_year":editautumn1obj})

def update_autumn1(request,id):
    parsed_list = id.split('+')
    print(parsed_list)
    course_id, program_id, year, section = parsed_list
    autumn1 = Acad_year.objects.filter(course_id=course_id, program_id=program_id, year=year, section=section, sem_id='AS1').update(faculty_sname=request.POST.get('faculty_sname'))
    time.sleep(5)
    return render(request, 'autumn1/edit_autumn1.html',{"Acad_year":autumn1})

def search_content(request):
    if request.method=="GET":
        query=request.META['QUERY_STRING']
        query_params=query.split('&')
        search_query=''

        for param in query_params:
            key,value=param.split('=')
            if key=='search_query':
                search_query=value

        connection=sqlite3.connect('courses-2023.db')
        cursor=connection.cursor()

        cursor.execute('SELECT course_id_id FROM core_acad_year WHERE sem_id="AS1" and (course_id_id = ? or program_id_id = ? or year=? or faculty_sname=?)',(search_query,)*4)
        searched_data = cursor.fetchall()
        print(searched_data)
        for i in range(len(searched_data)):
            searched_data[i] = searched_data[i][0]
            # print(searched_data[i])

        connection.close()
        showall = Acad_year.objects.filter(course_id_id__in=searched_data).order_by('course_id_id')
        print(showall)
        return render(request, 'autumn1/autumn1.html',{"data":showall})
    else:
        return render(request, 'autumn1/autumn1.html') 

def not_autumn1(request):
    connection=sqlite3.connect('courses-2023.db')
    cursor=connection.cursor()

    cursor.execute('SELECT course_id FROM core_course EXCEPT select course_id_id from core_acad_year where sem_id="AS1"')

    searched_data = cursor.fetchall()
    print(searched_data)
    for i in range(len(searched_data)):
        searched_data[i] = searched_data[i][0]

    connection.close()

    showall=Course.objects.filter(course_id__in = searched_data).order_by('course_id')
    return render(request, 'course_master.html',{"data":showall})

def queries_autumn1(request):
    return render(request, 'autumn1/queries_autumn1.html')

def query1_autumn1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''
        search_query2 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value
            if key == 'search_query2':
                search_query2 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT course_id_id FROM core_acad_year WHERE sem_id="AS1" AND program_id_id = ? AND year = ?', (search_query1,search_query2,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = Course.objects.filter(course_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_master.html',{"data":showall})
    else:
        return render(request, 'course_master.html') 

def query2_autumn1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''
        search_query2 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value
            if key == 'search_query2':
                search_query2 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseoffered as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS1" AND a.program_id_id = ? AND course_type = ?', (search_query1,search_query2,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = CourseOffered.objects.filter(course_id__in=searched_courses, program_id=search_query1).order_by('course_id')
        return render(request, 'course_offered.html',{"data":showall})
    else:
        return render(request, 'course_offered.html') 

def query3_autumn1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseslots as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS1" AND c.slot = ?', (search_query1,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = CourseOffered.objects.filter(course_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_offered.html',{"data":showall})
    else:
        return render(request, 'course_offered.html') 

def query4_autumn1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_coursefaculty as c ON a.faculty_sname=c.faculty_sname WHERE sem_id="AS1" AND c.faculty_sname = ?', (search_query1,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = Acad_year.objects.filter(course_id__in=searched_courses, faculty_sname=search_query1).order_by('course_id')
        return render(request, 'autumn1/autumn1.html',{"data":showall})
    else:
        return render(request, 'autumn1/autumn1.html') 

def query5_autumn1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseoffered as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS1" AND c.course_type IS NOT "Core"')
    searched_courses = cursor.fetchall()
    # print(searched_courses)
    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = CourseOffered.objects.filter(course_id__in=searched_courses).order_by('course_id')
    return render(request, 'electives.html',{"data":showall})

def query6_autumn1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT f.faculty_sname FROM core_faculty as f EXCEPT SELECT a.faculty_sname FROM core_acad_year as a WHERE sem_id="AS1"')
    searched_courses = cursor.fetchall()

    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = Faculty.objects.filter(faculty_sname__in=searched_courses).order_by('faculty_sname')
    return render(request, 'faculty_master.html',{"data":showall})

def query7_autumn1(request):
    showall = Acad_year.objects.filter(~Q(sem_id="AS1")).order_by('course_id')    
    return render(request, 'autumn1/autumn1.html',{"data":showall})

def query8_autumn1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT a.course_id_id FROM core_acad_year as a left join core_courseslots as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS1" AND c.slot IS NULL')
    searched_courses = cursor.fetchall()

    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = Acad_year.objects.filter(course_id__in=searched_courses).order_by('course_id')
    return render(request, 'autumn1/autumn1.html',{"data":showall})

def query9_autumn1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id WHERE sem_id="AS1" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query9.html',{'data':searched_courses})

def query10_autumn1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf inner join core_courseoffered as co ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id and cf.course_id_id = co.course_id_id WHERE sem_id="AS1" AND course_type="Core" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query10.html',{'data':searched_courses})

def query11_autumn1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf inner join core_courseoffered as co ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id and cf.course_id_id = co.course_id_id WHERE sem_id="AS1" AND course_type IS NOT "Core" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query11.html',{'data':searched_courses})

# ################################ AUTUMN TWO ################################

def autumn2(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                course_id = row[0]
                program_id = row[1]
                year = row[2]
                section = row[3]
                faculty_sname = row[4]
                sem_id = row[5]
                
                print(course_id, program_id, year, section, faculty_sname, sem_id)
                try:
                    if sem_id == 'AS2':
                        course = Course.objects.get(course_id=course_id)
                        program = Program.objects.get(id=program_id)

                        if Acad_year.objects.filter(
                            course_id=course,
                            program_id=program,
                            year=year,
                            section=section,
                            sem_id=sem_id
                        ).exists():
                            Acad_year.objects.filter(
                                course_id=course,
                                program_id=program,
                                year=year,
                                section=section,
                                sem_id=sem_id
                            ).update(faculty_sname=faculty_sname)
                        else:
                            Acad_year.objects.create(
                                course_id=course,
                                program_id=program,
                                year=year,
                                section=section,
                                faculty_sname=faculty_sname,
                                sem_id=sem_id
                            )

                except Course.DoesNotExist:
                    messages.error(request, f'Course with course_id {course_id} does not exist')
                except Program.DoesNotExist:
                    messages.error(request, f'Program with id {program_id} does not exist')

            messages.success(request, 'File imported successfully..!')
            time.sleep(3)

    showall = Acad_year.objects.filter(sem_id='AS2').order_by('course_id')
    # print(showall)
    return render(request, 'autumn2/autumn2.html', {"data": showall})

def insert_autumn2(request):
    if request.method=="POST":
        if request.POST.get('course_id') and request.POST.get('program_id') and request.POST.get('year') and request.POST.get('section') and request.POST.get('faculty_sname'):
            # print("1")
            course_id = request.POST.get('course_id')
            program_id = request.POST.get('program_id')
            year = request.POST.get('year')
            section = request.POST.get('section')
            faculty_sname = request.POST.get('faculty_sname')

            course = get_object_or_404(Course, course_id=course_id)
            program = get_object_or_404(Program, id=program_id)
            faculty = get_object_or_404(Faculty, faculty_sname=faculty_sname)

            saverecord=Acad_year(sem_id='AS2', course_id=course, program_id=program, year=year, section=section, faculty_sname=faculty)
            saverecord.save()
            messages.success(request,'Course "'+str(saverecord.course_id)+ '" is saved successfully in Autumn2..!')
            return render(request,'autumn2/insert_autumn2.html')
    else :
        return render(request,'autumn2/insert_autumn2.html')
    
def edit_autumn2(request,id):
    parsed_list = id.split('+')
    print(parsed_list)
    editautumn2obj=Acad_year.objects.get(course_id=parsed_list[0],program_id=parsed_list[1], year=parsed_list[2], section=parsed_list[3],sem_id='AS2')
    return render(request,'autumn2/edit_autumn2.html',{"Acad_year":editautumn2obj})

def update_autumn2(request,id):
    parsed_list = id.split('+')
    print(parsed_list)
    course_id, program_id, year, section = parsed_list
    autumn2 = Acad_year.objects.filter(course_id=course_id, program_id=program_id, year=year, section=section, sem_id='AS2').update(faculty_sname=request.POST.get('faculty_sname'))
    time.sleep(5)
    return render(request, 'autumn2/edit_autumn2.html',{"Acad_year":autumn2})

def search_content2(request):
    if request.method=="GET":
        query=request.META['QUERY_STRING']
        query_params=query.split('&')
        search_query=''

        for param in query_params:
            key,value=param.split('=')
            if key=='search_query':
                search_query=value

        connection=sqlite3.connect('courses-2023.db')
        cursor=connection.cursor()

        cursor.execute('SELECT course_id_id FROM core_acad_year WHERE sem_id="AS2" and (course_id_id = ? or program_id_id = ? or year=? or faculty_sname=?)',(search_query,)*4)
        searched_data = cursor.fetchall()
        # print(searched_data)
        for i in range(len(searched_data)):
            searched_data[i] = searched_data[i][0]
            # print(searched_data[i])

        connection.close()
        showall = Acad_year.objects.filter(course_id_id__in=searched_data).order_by('course_id_id')
        print(showall)
        return render(request, 'autumn2/autumn2.html',{"data":showall})
    else:
        return render(request, 'autumn2/autumn2.html') 

def not_autumn2(request):
    connection=sqlite3.connect('courses-2023.db')
    cursor=connection.cursor()

    cursor.execute('SELECT course_id FROM core_course EXCEPT select course_id_id from core_acad_year where sem_id="AS2"')

    searched_data = cursor.fetchall()
    print(searched_data)
    for i in range(len(searched_data)):
        searched_data[i] = searched_data[i][0]

    connection.close()

    showall=Course.objects.filter(course_id__in = searched_data).order_by('course_id')
    return render(request, 'course_master.html',{"data":showall})

def queries_autumn2(request):
    return render(request, 'autumn2/queries_autumn2.html')

def query1_autumn2(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''
        search_query2 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value
            if key == 'search_query2':
                search_query2 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT course_id_id FROM core_acad_year WHERE sem_id="AS2" AND program_id_id = ? AND year = ?', (search_query1,search_query2,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = Course.objects.filter(course_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_master.html',{"data":showall})
    else:
        return render(request, 'course_master.html') 

def query2_autumn2(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''
        search_query2 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value
            if key == 'search_query2':
                search_query2 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseoffered as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS2" AND a.program_id_id = ? AND course_type = ?', (search_query1,search_query2,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = CourseOffered.objects.filter(course_id__in=searched_courses, program_id=search_query1).order_by('course_id')
        return render(request, 'course_offered.html',{"data":showall})
    else:
        return render(request, 'course_offered.html') 

def query3_autumn2(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseslots as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS2" AND c.slot = ?', (search_query1,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = CourseOffered.objects.filter(course_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_offered.html',{"data":showall})
    else:
        return render(request, 'course_offered.html') 

def query4_autumn2(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_coursefaculty as c ON a.faculty_sname=c.faculty_sname WHERE sem_id="AS2" AND c.faculty_sname = ?', (search_query1,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = Acad_year.objects.filter(course_id__in=searched_courses, faculty_sname=search_query1).order_by('course_id')
        return render(request, 'autumn2/autumn2.html',{"data":showall})
    else:
        return render(request, 'autumn2/autumn2.html') 

def query5_autumn2(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseoffered as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS2" AND c.course_type IS NOT "Core"')
    searched_courses = cursor.fetchall()
    # print(searched_courses)
    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = CourseOffered.objects.filter(course_id__in=searched_courses).order_by('course_id')
    return render(request, 'electives.html',{"data":showall})

def query6_autumn2(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT f.faculty_sname FROM core_faculty as f EXCEPT SELECT a.faculty_sname FROM core_acad_year as a WHERE sem_id="AS2"')
    searched_courses = cursor.fetchall()

    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = Faculty.objects.filter(faculty_sname__in=searched_courses).order_by('faculty_sname')
    return render(request, 'faculty_master.html',{"data":showall})

def query7_autumn2(request):
    showall = Acad_year.objects.filter(~Q(sem_id="AS2")).order_by('course_id')    
    return render(request, 'autumn2/autumn2.html',{"data":showall})

def query8_autumn2(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT a.course_id_id FROM core_acad_year as a left join core_courseslots as c ON a.course_id_id=c.course_id_id WHERE sem_id="AS2" AND c.slot IS NULL')
    searched_courses = cursor.fetchall()

    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = Acad_year.objects.filter(course_id__in=searched_courses).order_by('course_id')
    return render(request, 'autumn2/autumn2.html',{"data":showall})

def query9_autumn2(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id WHERE sem_id="AS2" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query9.html',{'data':searched_courses})

def query10_autumn2(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf inner join core_courseoffered as co ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id and cf.course_id_id = co.course_id_id WHERE sem_id="AS2" AND course_type="Core" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query10.html',{'data':searched_courses})

def query11_autumn2(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf inner join core_courseoffered as co ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id and cf.course_id_id = co.course_id_id WHERE sem_id="AS2" AND course_type IS NOT "Core" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query11.html',{'data':searched_courses})

# ################################ WINTER ONE ################################

def winter1(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            header = next(reader, None)
            for row in reader:
                course_id = row[0]
                program_id = row[1]
                year = row[2]
                section = row[3]
                faculty_sname = row[4]
                sem_id = row[5]
                
                print(course_id, program_id, year, section, faculty_sname, sem_id)
                try:
                    if sem_id == 'WS1':
                        course = Course.objects.get(course_id=course_id)
                        program = Program.objects.get(id=program_id)

                        if Acad_year.objects.filter(
                            course_id=course,
                            program_id=program,
                            year=year,
                            section=section,
                            sem_id=sem_id
                        ).exists():
                            Acad_year.objects.filter(
                                course_id=course,
                                program_id=program,
                                year=year,
                                section=section,
                                sem_id=sem_id
                            ).update(faculty_sname=faculty_sname)
                        else:
                            Acad_year.objects.create(
                                course_id=course,
                                program_id=program,
                                year=year,
                                section=section,
                                faculty_sname=faculty_sname,
                                sem_id=sem_id
                            )

                except Course.DoesNotExist:
                    messages.error(request, f'Course with course_id {course_id} does not exist')
                except Program.DoesNotExist:
                    messages.error(request, f'Program with id {program_id} does not exist')

            messages.success(request, 'File imported successfully..!')
            time.sleep(3)

    showall = Acad_year.objects.filter(sem_id='WS1').order_by('course_id')
    # print(showall)
    return render(request, 'winter1/winter1.html', {"data": showall})

def insert_winter1(request):
    if request.method=="POST":
        if request.POST.get('course_id') and request.POST.get('program_id') and request.POST.get('year') and request.POST.get('section') and request.POST.get('faculty_sname'):
            # print("1")
            course_id = request.POST.get('course_id')
            program_id = request.POST.get('program_id')
            year = request.POST.get('year')
            section = request.POST.get('section')
            faculty_sname = request.POST.get('faculty_sname')

            course = get_object_or_404(Course, course_id=course_id)
            program = get_object_or_404(Program, id=program_id)
            faculty = get_object_or_404(Faculty, faculty_sname=faculty_sname)

            saverecord=Acad_year(sem_id='WS1', course_id=course, program_id=program, year=year, section=section, faculty_sname=faculty)
            saverecord.save()
            messages.success(request,'Course "'+str(saverecord.course_id)+ '" is saved successfully in Winter1..!')
            return render(request,'winter1/insert_winter1.html')
    else :
        return render(request,'winter1/insert_winter1.html')
    
def edit_winter1(request,id):
    parsed_list = id.split('+')
    print(parsed_list)
    editwinter1obj=Acad_year.objects.get(course_id=parsed_list[0],program_id=parsed_list[1], year=parsed_list[2], section=parsed_list[3], sem_id='WS1')
    return render(request,'winter1/edit_winter1.html',{"Acad_year":editwinter1obj})

def update_winter1(request,id):
    parsed_list = id.split('+')
    print(parsed_list)
    course_id, program_id, year, section = parsed_list
    winter1 = Acad_year.objects.filter(course_id=course_id, program_id=program_id, year=year, section=section, sem_id='WS1').update(faculty_sname=request.POST.get('faculty_sname'))
    time.sleep(5)
    return render(request, 'winter1/edit_winter1.html',{"Acad_year":winter1})

def search_content3(request):
    if request.method=="GET":
        query=request.META['QUERY_STRING']
        query_params=query.split('&')
        search_query=''

        for param in query_params:
            key,value=param.split('=')
            if key=='search_query':
                search_query=value

        connection=sqlite3.connect('courses-2023.db')
        cursor=connection.cursor()

        cursor.execute('SELECT course_id_id FROM core_acad_year WHERE sem_id="WS1" and (course_id_id = ? or program_id_id = ? or year=? or faculty_sname=?)',(search_query,)*4)
        searched_data = cursor.fetchall()
        print(searched_data)
        for i in range(len(searched_data)):
            searched_data[i] = searched_data[i][0]
            # print(searched_data[i])

        connection.close()
        showall = Acad_year.objects.filter(course_id_id__in=searched_data).order_by('course_id_id')
        print(showall)
        return render(request, 'winter1/winter1.html',{"data":showall})
    else:
        return render(request, 'winter1/winter1.html') 

def not_winter1(request):
    connection=sqlite3.connect('courses-2023.db')
    cursor=connection.cursor()

    cursor.execute('SELECT course_id FROM core_course EXCEPT select course_id_id from core_acad_year where sem_id="WS1"')

    searched_data = cursor.fetchall()
    print(searched_data)
    for i in range(len(searched_data)):
        searched_data[i] = searched_data[i][0]

    connection.close()

    showall=Course.objects.filter(course_id__in = searched_data).order_by('course_id')
    return render(request, 'course_master.html',{"data":showall})

def queries_winter1(request):
    return render(request, 'winter1/queries_winter1.html')

def query1_winter1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''
        search_query2 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value
            if key == 'search_query2':
                search_query2 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT course_id_id FROM core_acad_year WHERE sem_id="WS1" AND program_id_id = ? AND year = ?', (search_query1,search_query2,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = Course.objects.filter(course_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_master.html',{"data":showall})
    else:
        return render(request, 'course_master.html') 

def query2_winter1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''
        search_query2 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value
            if key == 'search_query2':
                search_query2 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseoffered as c ON a.course_id_id=c.course_id_id WHERE sem_id="WS1" AND a.program_id_id = ? AND course_type = ?', (search_query1,search_query2,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = CourseOffered.objects.filter(course_id__in=searched_courses, program_id=search_query1).order_by('course_id')
        return render(request, 'course_offered.html',{"data":showall})
    else:
        return render(request, 'course_offered.html') 

def query3_winter1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseslots as c ON a.course_id_id=c.course_id_id WHERE sem_id="WS1" AND c.slot = ?', (search_query1,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = CourseOffered.objects.filter(course_id__in=searched_courses).order_by('course_id')
        return render(request, 'course_offered.html',{"data":showall})
    else:
        return render(request, 'course_offered.html') 

def query4_winter1(request):
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']  
        query_params = query_string.split('&')
        search_query1 = ''

        for param in query_params:
            key, value = param.split('=')
            if key == 'search_query1':
                search_query1 = value

        current_database_name = settings.DATABASES['default']['NAME']
        connection = sqlite3.connect(current_database_name)
        cursor = connection.cursor()
    
        # Retrieve the desired columns from the tables
        cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_coursefaculty as c ON a.faculty_sname=c.faculty_sname WHERE sem_id="WS1" AND c.faculty_sname = ?', (search_query1,))
        searched_courses = cursor.fetchall()
        # print(searched_courses)
        for i in range(len(searched_courses)):
            searched_courses[i] = searched_courses[i][0]

        connection.close()

        showall = Acad_year.objects.filter(course_id__in=searched_courses, faculty_sname=search_query1).order_by('course_id')
        return render(request, 'winter1/winter1.html',{"data":showall})
    else:
        return render(request, 'winter1/winter1.html') 

def query5_winter1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT a.course_id_id FROM core_acad_year as a inner join core_courseoffered as c ON a.course_id_id=c.course_id_id WHERE sem_id="WS1" AND c.course_type IS NOT "Core"')
    searched_courses = cursor.fetchall()
    # print(searched_courses)
    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = CourseOffered.objects.filter(course_id__in=searched_courses).order_by('course_id')
    return render(request, 'electives.html',{"data":showall})

def query6_winter1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT f.faculty_sname FROM core_faculty as f EXCEPT SELECT a.faculty_sname FROM core_acad_year as a WHERE sem_id="WS1"')
    searched_courses = cursor.fetchall()

    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = Faculty.objects.filter(faculty_sname__in=searched_courses).order_by('faculty_sname')
    return render(request, 'faculty_master.html',{"data":showall})

def query7_winter1(request):
    showall = Acad_year.objects.filter(~Q(sem_id="WS1")).order_by('course_id')    
    return render(request, 'winter1/winter1.html',{"data":showall})

def query8_winter1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    # Retrieve the desired columns from the tables
    cursor.execute('SELECT a.course_id_id FROM core_acad_year as a left join core_courseslots as c ON a.course_id_id=c.course_id_id WHERE sem_id="WS1" AND c.slot IS NULL')
    searched_courses = cursor.fetchall()

    for i in range(len(searched_courses)):
        searched_courses[i] = searched_courses[i][0]

    connection.close()

    showall = Acad_year.objects.filter(course_id__in=searched_courses).order_by('course_id')
    return render(request, 'winter1/winter1.html',{"data":showall})

def query9_winter1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id WHERE sem_id="WS1" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query9.html',{'data':searched_courses})

def query10_winter1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf inner join core_courseoffered as co ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id and cf.course_id_id = co.course_id_id WHERE sem_id="WS1" AND course_type="Core" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query10.html',{'data':searched_courses})

def query11_winter1(request):
    current_database_name = settings.DATABASES['default']['NAME']
    connection = sqlite3.connect(current_database_name)
    cursor = connection.cursor()
    
    cursor.execute('SELECT a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname, GROUP_CONCAT(DISTINCT(a.program_id_id)) AS batch_list FROM core_acad_year as a inner join core_course as c inner join core_coursefaculty as cf inner join core_courseoffered as co ON a.course_id_id=c.course_id and c.course_id = cf.course_id_id and cf.course_id_id = co.course_id_id WHERE sem_id="WS1" AND course_type IS NOT "Core" GROUP BY a.course_id_id, c.course_name, c.course_credits, cf.faculty_sname')
    searched_courses = cursor.fetchall()

    connection.close()

    return render(request, 'query11.html',{'data':searched_courses})

# def winter1(request):
#     if request.method == 'POST' and request.FILES.get('csv_file'):
#         csv_file = request.FILES['csv_file']
#         if not csv_file.name.endswith('.csv'):
#             messages.error(request, 'Please upload a CSV file.')
#         else:
#             decoded_file = csv_file.read().decode('utf-8').splitlines()
#             reader = csv.reader(decoded_file)
#             header = next(reader, None)
#             for row in reader:
#                 course_id = row[0]
#                 program_id = row[1]
#                 year = row[2]
#                 section = row[3]
#                 faculty_sname = row[4]

#                 try:
#                     course = Course.objects.get(course_id=course_id)
#                     program = Program.objects.get(id=program_id)

#                     if Winter_one.objects.filter(
#                         course_id=course,
#                         program_id=program,
#                         year=year,
#                         section=section
#                     ).exists():
#                         Winter_one.objects.filter(
#                             course_id=course,
#                             program_id=program,
#                             year=year,
#                             section=section
#                         ).update(faculty_sname=faculty_sname)
#                     else:
#                         Winter_one.objects.create(
#                             course_id=course,
#                             program_id=program,
#                             year=year,
#                             section=section,
#                             faculty_sname=faculty_sname
#                         )

#                 except Course.DoesNotExist:
#                     messages.error(request, f'Course with course_id {course_id} does not exist')
#                 except Program.DoesNotExist:
#                     messages.error(request, f'Program with id {program_id} does not exist')

#             messages.success(request, 'File imported successfully..!')
#             time.sleep(3)

#     showall = Winter_one.objects.all().order_by('course_id')
#     return render(request, 'winter1/winter1.html', {"data": showall})


# def insert_winter1(request):
#     if request.method=="POST":
#         if request.POST.get('course_id') and request.POST.get('program_id') and request.POST.get('year') and request.POST.get('section') and request.POST.get('faculty_sname'):
#             # print("1")
#             course_id = request.POST.get('course_id')
#             program_id = request.POST.get('program_id')
#             year = request.POST.get('year')
#             section = request.POST.get('section')
#             faculty_sname = request.POST.get('faculty_sname')

#             course = get_object_or_404(Course, course_id=course_id)
#             program = get_object_or_404(Program, id=program_id)
#             faculty = get_object_or_404(Faculty, faculty_sname=faculty_sname)

#             saverecord=Winter_one(course_id=course, program_id=program, year=year, section=section, faculty_sname=faculty)
#             saverecord.save()
#             messages.success(request,'Course "'+str(saverecord.course_id)+ '" is saved successfully in Winter1..!')
#             return render(request,'winter1/insert_winter1.html')
#     else :
#         return render(request,'winter1/insert_winter1.html')
    
# def edit_winter1(request,id):
#     parsed_list = id.split('+')
#     editwinter1obj=Winter_one.objects.get(course_id=parsed_list[0],program_id=parsed_list[1], year=parsed_list[2], section=parsed_list[3])
#     return render(request,'winter1/edit_winter1.html',{"Winter_one":editwinter1obj})

# def update_winter1(request,id):
#     parsed_list = id.split('+')
#     course_id,program_id, year, section = parsed_list
#     winter1 = Winter_one.objects.filter(course_id=course_id,program_id=program_id, year=year, section=section).update(faculty_sname=request.POST.get('faculty_sname'))
#     time.sleep(5)
#     return render(request, 'winter1/edit_winter1.html',{"Winter_one":winter1})

# def search_content3(request):
#     if request.method=="GET":
#         query=request.META['QUERY_STRING']
#         query_params=query.split('&')
#         search_query=''

#         for param in query_params:
#             key,value=param.split('=')
#             if key=='search_query':
#                 search_query=value

#         connection=sqlite3.connect('courses-2023.db')
#         cursor=connection.cursor()

#         cursor.execute('SELECT course_id_id FROM core_winter_one WHERE course_id_id = ? or program_id_id = ? or year=? or faculty_sname=?',(search_query,)*4)
#         searched_data = cursor.fetchall()
#         print(searched_data)
#         for i in range(len(searched_data)):
#             searched_data[i] = searched_data[i][0]
#             # print(searched_data[i])

#         connection.close()
#         showall = Winter_one.objects.filter(course_id_id__in=searched_data).order_by('course_id_id')
#         print(showall)
#         return render(request, 'winter1/winter1.html',{"data":showall})
#     else:
#         return render(request, 'winter1/winter1.html') 


# def not_winter1(request):
#     connection=sqlite3.connect('courses-2023.db')
#     cursor=connection.cursor()

#     cursor.execute('SELECT course_id FROM core_course EXCEPT select course_id_id from core_winter_one ')

#     searched_data = cursor.fetchall()
#     print(searched_data)
#     for i in range(len(searched_data)):
#         searched_data[i] = searched_data[i][0]

#     connection.close()

#     showall=Course.objects.filter(course_id__in = searched_data).order_by('course_id')
#     return render(request, 'course_master.html',{"data":showall})

# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import os

def database_prev(request):
    current_database_name = settings.DATABASES['default']['NAME']
    year = os.path.splitext(os.path.basename(current_database_name))[0].split('-')[1]
    print(year)
    if int(year) > 2023 :
        year = int(year) - 1
    else :
        year = 2023
    os.system('python3 manage.py database_prev')
    messages.success(request, 'Database Switched Successfully to Year ' + str(year-1) + '-' + str(year) + '.')
    return HttpResponseRedirect(reverse('home'))

def database_next(request):
    current_database_name = settings.DATABASES['default']['NAME']
    year = os.path.splitext(os.path.basename(current_database_name))[0].split('-')[1]
    print(year)
    year = int(year) + 1
    os.system('python3 manage.py database_next')
    messages.success(request, 'Database Switched Successfully to Year ' + str(year-1) + '-' + str(year) + '.')
    return HttpResponseRedirect(reverse('home'))