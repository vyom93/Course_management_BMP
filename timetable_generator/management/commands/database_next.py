# myapp/management/commands/copy_database.py
import os
import shutil
from django.core.management.base import BaseCommand
from django.db import connections
from pathlib import Path


class Command(BaseCommand):
    help = 'Copy the current database and switch to the new one for the next year.'

    def handle(self, *args, **options):
        current_db_path = connections['default'].settings_dict['NAME']
        current_db_path_str = str(current_db_path)  # Convert WindowsPath to string

        # Extract the year part from the filename
        year_part = os.path.splitext(os.path.basename(current_db_path_str))[0].split('-')[1]

        try:
            current_year = int(year_part)
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Error extracting year: {e}'))
            return

        next_year = current_year + 1

        # Create a copy of the current database
        next_db_path = current_db_path_str.replace(str(current_year), str(next_year))
        
        # Check if the destination database file already exists
        if os.path.exists(next_db_path):
            self.stdout.write(self.style.WARNING(f'Destination database file {next_db_path} already exists. Skipped copying.'))
        else:
            shutil.copy2(current_db_path_str, next_db_path)

        # Update settings.py file with the new database path
        next_db_path = next_db_path
        self.update_settings(next_db_path)

        # Switch to the new database
        connections['default'].close()
        connections['default'].settings_dict['NAME'] = next_db_path
        connections['default'].connect()

        self.stdout.write(self.style.SUCCESS(f'Database copy successful. Switched to {next_db_path}'))

    def update_settings(self, next_db_path):
        relative_path = os.path.join('..','timetable_generator','timetable_generator', 'settings.py')
        settings_file = os.path.abspath(relative_path)
        # settings_file = r'/Users/vyompatel/Desktop/Timetable-Generator/Timetable-Generator/Timetable-Generator/Timetable-Generator/timetable_generator/timetable_generator/settings.py'  
        # Update this with the actual path to your settings.py file

        with open(settings_file, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if 'DATABASES' in line:
                start_index = i
                break

        for i, line in enumerate(lines[start_index:], start=start_index):
            if line.strip() == '}':
                end_index = i
                break

        # Update the 'NAME' field with the new database path
        for i in range(start_index, end_index + 1):
            if "'NAME'" in lines[i]:
                lines[i] = f"        'NAME': r'{next_db_path}',\n"

        with open(settings_file, 'w') as f:
            f.writelines(lines)
