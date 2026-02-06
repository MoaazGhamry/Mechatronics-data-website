import pandas as pd
import re
import os
from django.core.management.base import BaseCommand
from hub.models import Level, Subject, Resource

class Command(BaseCommand):
    help = 'Import subjects from subjects.xlsx into Django database'

    def handle(self, *args, **options):
        excel_file = 'subjects.xlsx'
        if not os.path.exists(excel_file):
            self.stderr.write(self.style.ERROR(f'File {excel_file} not found'))
            return

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Resource.objects.all().delete()
        Subject.objects.all().delete()
        Level.objects.all().delete()

        df = pd.read_excel(excel_file, header=None)
        
        current_level_obj = None
        sem1_col = None
        sem2_col = None
        res_types = ["Explanation", "Lectures", "Sheets", "Midterm", "Final", "Revision"]
        
        # Pre-defined Levels info map
        levels_map = {
            "000": {"title": "Foundation Level", "icon_name": "Brick"},
            "100": {"title": "Mechanical Fundamentals", "icon_name": "Gear"},
            "200": {"title": "Electrical & Electronics", "icon_name": "Bulb"},
            "300": {"title": "Robotics & Control", "icon_name": "Robot"},
            "400": {"title": "Space & Advanced Systems", "icon_name": "Rocket"},
        }

        self.stdout.write('Parsing Excel...')
        for i, row in df.iterrows():
            row_list = row.tolist()
            
            # Check for Level Header
            for j, cell in enumerate(row_list):
                cell_str = str(cell).lower()
                if "level" in cell_str:
                    match = re.search(r'(\d+)', cell_str)
                    if match:
                        lid = match.group(1).zfill(3)
                        info = levels_map.get(lid, {"title": f"Level {lid}", "icon_name": "Brick"})
                        current_level_obj, created = Level.objects.get_or_create(
                            level_id=lid,
                            defaults={'title': info['title'], 'icon_name': info['icon_name']}
                        )
                        sem1_col = None
                        sem2_col = None
                        self.stdout.write(self.style.SUCCESS(f'Found Level {lid}'))

            if current_level_obj:
                # Check for Semester Headers
                for j, cell in enumerate(row_list):
                    cell_str = str(cell).lower()
                    if "semester" in cell_str:
                        if "(1)" in cell_str:
                            sem1_col = j
                        elif "(2)" in cell_str:
                            sem2_col = j
                
                # Parse Subjects
                # Semester 1
                if sem1_col is not None:
                    subj_name = str(row_list[sem1_col]) if len(row_list) > sem1_col else ""
                    if subj_name and subj_name.lower() != 'nan' and "semester" not in subj_name.lower() and "level" not in subj_name.lower():
                        subject = Subject.objects.create(name=subj_name, level=current_level_obj, semester=1)
                        for k, rtype in enumerate(res_types):
                            url = str(row_list[sem1_col + 1 + k]) if len(row_list) > (sem1_col + 1 + k) else '#'
                            if str(url).lower() == 'nan' or not url: url = '#'
                            Resource.objects.create(subject=subject, resource_type=rtype, url=url)

                # Semester 2
                if sem2_col is not None:
                    subj_name = str(row_list[sem2_col]) if len(row_list) > sem2_col else ""
                    if subj_name and subj_name.lower() != 'nan' and "semester" not in subj_name.lower() and "level" not in subj_name.lower():
                        subject = Subject.objects.create(name=subj_name, level=current_level_obj, semester=2)
                        for k, rtype in enumerate(res_types):
                            url = str(row_list[sem2_col + 1 + k]) if len(row_list) > (sem2_col + 1 + k) else '#'
                            if str(url).lower() == 'nan' or not url: url = '#'
                            Resource.objects.create(subject=subject, resource_type=rtype, url=url)

        self.stdout.write(self.style.SUCCESS('Data import complete!'))
