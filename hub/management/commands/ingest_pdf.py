import os
from django.core.management.base import BaseCommand
from hub.models import UniversityKnowledge
import pypdf

class Command(BaseCommand):
    help = 'Ingests specific PDF content into the UniversityKnowledge database for the AI Assistant'

    def handle(self, *args, **kwargs):
        # Specific file path
        pdf_path = 'Prof_Gamal_Eng_2023.pdf'
        
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f'File not found: {pdf_path}'))
            return

        self.stdout.write(f'Reading {pdf_path}...')
        
        try:
            # Clear old entries from this source to avoid duplicates
            # We assume anything with category='rules' might be from here, 
            # OR we can just delete all non-FAQ entries to be safe/clean.
            deleted_count, _ = UniversityKnowledge.objects.filter(question__startswith='Handbook Page').delete()
            self.stdout.write(f'Removed {deleted_count} old handbook entries.')

            reader = pypdf.PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            created_count = 0
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text.strip():
                    continue
                
                # Basic cleaning
                text = text.replace('\x00', '') # Remove null bytes if any
                
                # Create entry
                UniversityKnowledge.objects.create(
                    category='rules',
                    question=f'Handbook Page {i+1}',
                    answer=text
                )
                created_count += 1
                self.stdout.write(f'Processed Page {i+1}/{total_pages}')

            self.stdout.write(self.style.SUCCESS(f'Successfully ingested {created_count} pages from {pdf_path}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading PDF: {e}'))
