import os
from django.core.management.base import BaseCommand
from hub.models import Level, Subject, SubjectResource
from django.conf import settings

class Command(BaseCommand):
    help = 'Import organized resources from media/resources/Level000'

    def handle(self, *args, **options):
        level_map = {
            "Level000": "000",
            "Level100": "100",
            "Level200": "200"
        }
        
        term_map = {
            "Level 000 First Term": 1,
            "Level 000 Second Term": 2,
            "Level 100 First Term": 1,
            "LEVEL 100 Secend Term": 2,
            "Level 200 First Term": 1
        }
        
        # Subject mapping by Level (Level ID -> Semester -> Folder Name -> DB Name)
        subject_map = {
            "000": {
                1: {
                    "drawing and projection": "Drawing and Projection",
                    "english": "English",
                    "math 1": "Math 1",
                    "mechanice": "Mechanics",
                    "chemistry": "Chemistry",
                    "physics": "Physics",
                },
                2: {
                    "drawing and projection": "Drawing and Projection",
                    "math": "Math 2",
                    "mechanics": "Mechanics 2",
                    "physics": "Physics 2",
                    "production technology": "Production Technology",
                    "program": "Program",
                    "تاريخ هندسي": "Engineering History"
                }
            },
            "100": {
                1: {
                    "c++": "C++",
                    "circuit theory": "Circuit Theory",
                    "engineering materials": "Engineering Material",
                    "machine mechanics": "Mechanics Of Machine",
                    "math 3": "Math 3",
                    "thermodynamics": "Thermodynamics"
                },
                2: {
                    "electrical systems": "Electrical Systems",
                    "human resource": "Human Resource",
                    "introduction to law": "Introduction To Law",
                    "introduction to mechatronics": "Intro to Mechatronics",
                    "machine drawing": "Machine Drawing",
                    "numerical techniques": "Numerical Techniques",
                    "stress analysis": "Stress Analysis"
                }
            },
            "200": {
                1: {
                    "electronics": "Engineering Electronics",
                    "fluid mechanics": "Fluid Mechanics",
                    "machine theory": "Machine Theory",
                    "manufacturing processes": "Manufacturing Processes",
                    "project management": "Project Management",
                    "seminar_": "Seminar",
                    "statistics": "Statistics"
                }
            }
        }
        
        # Category mapping (Lower Case Folder Name -> RESOURCE_TYPES Choice)
        category_map = {
            "lecture": "Lectures",
            "lectures": "Lectures",
            "practical": "Lectures",
            "projection": "Lectures",
            "drawing book": "Lectures", # Mapping book as lectures/explanation
            "sheet": "Sheets",
            "sheets": "Sheets",
            "assignment": "Sheets",
            "workshop": "Sheets",
            "solution sheet_": "Sheets",
            "solution drawing book": "Sheets",
            "mid term": "Midterm",
            "midterm": "Midterm",
            "final": "Final",
            "revision": "Revision",
            "reviews": "Revision",
            "review": "Revision",
            "review 2024": "Revision",
            "explanation": "Explanation",
            "lab": "Explanation",
            "practical mechanics": "Explanation",
            "quiz": "Midterm",
            "midtrem": "Midterm",
            "midterm-20260124t111155z-3-001": "Midterm",
            "lap": "Explanation",
            "labs": "Explanation",
            "midterm solution": "Midterm",
            "mid": "Midterm",
            "exams": "Final",
            "exam": "Final",
            "quizzes": "Midterm",
            "quizzes_": "Midterm",
            "report": "Sheets",
            "projects": "Sheets",
            "sheet solution": "Sheets",
            "sheet_": "Sheets",
            "revsion": "Revision",
            "mid and final": "Final",
            "midterm and final": "Final",
            "assignment_": "Sheets",
        }

        resources_base = os.path.join(settings.MEDIA_ROOT, 'resources')
        
        if not os.path.exists(resources_base):
            self.stdout.write(self.style.ERROR(f'Directory {resources_base} does not exist.'))
            return

        imported_count = 0
        skipped_count = 0
        
        # Process Level000, Level100, Level200
        for level_folder in ["Level000", "Level100", "Level200"]:
            level_id = level_map.get(level_folder)
            level_obj = Level.objects.filter(level_id=level_id).first()
            
            if not level_obj:
                self.stdout.write(self.style.ERROR(f'Level {level_id} not found in database.'))
                continue
                
            level_path = os.path.join(resources_base, level_folder)
            if not os.path.isdir(level_path):
                continue
                
            for term_folder in os.listdir(level_path):
                semester = term_map.get(term_folder)
                if not semester:
                    continue
                    
                term_path = os.path.join(level_path, term_folder)
                if not os.path.isdir(term_path):
                    continue
                    
                for sub_folder in os.listdir(term_path):
                    # Use lower() for normalized matching from level+semester-specific map
                    level_subjects = subject_map.get(level_id, {})
                    term_map_data = level_subjects.get(semester, {})
                    db_subject_name = term_map_data.get(sub_folder.lower(), sub_folder)
                    subject_obj = Subject.objects.filter(level=level_obj, name=db_subject_name, semester=semester).first()
                    
                    if not subject_obj:
                        self.stdout.write(self.style.WARNING(f'Subject {sub_folder} -> {db_subject_name} (Sem {semester}) not found in DB.'))
                        continue
                        
                    sub_path = os.path.join(term_path, sub_folder)
                    if not os.path.isdir(sub_path):
                        continue
                        
                    for cat_folder in os.listdir(sub_path):
                        category = category_map.get(cat_folder.lower())
                        if not category:
                            self.stdout.write(self.style.WARNING(f'Category {cat_folder} not mapped. Skipping.'))
                            continue
                            
                        cat_path = os.path.join(sub_path, cat_folder)
                        if not os.path.isdir(cat_path):
                            continue
                            
                        for filename in os.listdir(cat_path):
                            file_path = os.path.join(cat_path, filename)
                            if not os.path.isfile(file_path):
                                continue
                                
                            # Save path relative to MEDIA_ROOT
                            relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                            # Standardize to forward slashes for DB consistency
                            relative_path = relative_path.replace('\\', '/')
                            
                            # Check if record already exists
                            if SubjectResource.objects.filter(file=relative_path).exists():
                                skipped_count += 1
                                continue
                                
                            SubjectResource.objects.create(
                                subject=subject_obj,
                                category=category,
                                file=relative_path
                            )
                            imported_count += 1
                            self.stdout.write(self.style.SUCCESS(f'Imported: {filename}'))

        self.stdout.write(self.style.SUCCESS(f'Done! Imported {imported_count}, Skipped {skipped_count}'))
