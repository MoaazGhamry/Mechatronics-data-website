import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechatronics_hub.settings')
django.setup()

from hub.models import UniversityKnowledge

def test_search(user_message):
    print(f"\nUser Query: '{user_message}'")
    
    # Simulate logic from views.py
    matches = []
    
    # 1. Simple Keyword Match (Original)
    # ... logic skipped for brevity, testing the fallback mostly ...

    # 4. Fallback: Offline Keyword Search with Query Expansion
    query_terms = list(filter(lambda x: len(x)>3, user_message.lower().split()))
    
    keyword_map = {
        'credit': ['ساعات', 'معتمدة'],
        'hour': ['ساعات', 'معتمدة'],
        'hours': ['ساعات', 'معتمدة'],
        'approved': ['معتمدة'],
        'grade': ['درجات', 'تقديرات', 'نظام'],
        'grading': ['درجات', 'تقديرات'],
        'gpa': ['المعدل', 'التراكمي'],
        'exam': ['امتحان', 'اختبار'],
        'midterm': ['ميتيرم', 'الفصل'],
        'final': ['فاينل', 'النهائي'],
        'register': ['تسجيل'],
        'registration': ['تسجيل', 'الحذف', 'الاضافة'],
        'level': ['مستوى', 'المستوى'],
        'course': ['مادة', 'مقرر'],
        'subject': ['مادة', 'مقرر'],
        'fail': ['رسوب'],
        'pass': ['نجاح'],
        'attendance': ['غياب', 'حضور'],
        'rules': ['لائحة', 'قواعد'],
        'absent': ['غياب'],
    }
    
    expanded_terms = set(query_terms)
    for term in query_terms:
        if term in keyword_map:
            expanded_terms.update(keyword_map[term])
    
    print(f"Expanded Terms: {expanded_terms}")
    
    knowledge_entries = UniversityKnowledge.objects.exclude(answer__isnull=True) # exclude empty
    
    for entry in knowledge_entries:
            e_text = (entry.question or "") + " " + entry.answer
            # Check if ANY of the expanded terms match
            if any(term in e_text.lower() for term in expanded_terms):
                matches.append(entry.answer[:100] + "...")
    
    if matches:
        print(f"FOUND {len(matches)} MATCHES!")
        print(f"Top match: {matches[0]}")
    else:
        print("NO MATCHES FOUND.")

if __name__ == "__main__":
    test_search("What is the approved hour?")
    test_search("Tell me about grading")
