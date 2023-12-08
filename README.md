# Course management and Timetable-Generator

Course management and Timetable-Generator is a web application developed using Django, HTML, CSS, and JavaScript. It provides an easy-to-use interface for administrators to manage programs, batches, courses, and faculties, and generates a timetable based on the provided information.

## Features

* User-friendly interface for managing programs, batches, courses, and faculties.
* Automatic timetable generation based on the specified constraints.
* Admin dashboard for easy management of data.
* Responsive design for optimal viewing on different devices.
* Uses SQLite database for data storage.

## Prerequisites

* Python
* Django
* SQLite

## Installation

1. Clone the repository:
git clone https://github.com/vyom93/Course_management_BMP.git
2. Change into the project directory:
cd timetable_generator
3. Install Dependencies:
pip install django
4. Apply the database migrations:
python manage.py migrate
5. Create a superuser to access the admin dashboard:
python manage.py createsuperuser
6. Start the server:
python manage.py runserver

## Usage

* Login to the admin dashboard using the superuser credentials created during installation.
* Manage Programs, Batches, Courses, and Faculties by adding, editing, or deleting them as needed.
* Configure any additional constraints or preferences related to the timetable generation.
* Click on the "Generate Timetable" button to automatically generate a timetable based on the provided information.
* The generated timetable will be displayed, showing the schedule for each program, batch, course, and faculty.
