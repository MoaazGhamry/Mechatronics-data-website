from django.core.management.base import BaseCommand
from hub.models import UniversityKnowledge

class Command(BaseCommand):
    help = 'Populates the University Knowledge Base with academic regulations and FAQs'

    def handle(self, *args, **kwargs):
        # Clear existing data to avoid duplicates
        UniversityKnowledge.objects.all().delete()

        # 1. General Rules (Sectioned)
        rules = [
            {
                "category": "rules",
                "question": "نظام الدراسة والتسجيل",
                "answer": """1. نظام الدراسة والتسجيل
نظام الساعات المعتمدة: تعتمد الدراسة على هذا النظام، حيث تحسب ساعة المحاضرة بساعة معتمدة، بينما تحسب تمارين الساعتين بساعة واحدة، والعملي (2-3 ساعات) بساعة واحدة.
الفصول الدراسية: تنقسم السنة إلى ثلاثة فصول: الخريف والربيع (14 أسبوعاً لكل منهما) والصيفي (7 أسابيع مكثفة).
العبء الدراسي: الطالب المنذر أكاديمياً (GPA أقل من 2.00) لا يسجل أكثر من 14 ساعة، وفي الصيفي الحد الأقصى 6 ساعات."""
            },
            {
                "category": "rules",
                "question": "متطلبات التخرج والتقديرات",
                "answer": """2. متطلبات التخرج والتقديرات
للحصول على البكالوريوس: يجب اجتياز 165 ساعة معتمدة بمتوسط تراكمي لا يقل عن 2.00، مع إتمام مشروع التخرج وتدريب صيفي لمدة 8 أسابيع.
النجاح في المقرر: يتطلب الحصول على 60% (تقدير D) على الأقل، بشرط الحصول على 30% كحد أدنى في الامتحان التحريري النهائي.
مرتبة الشرف: تمنح لمن لا يقل معدله عن 3.6 طوال فترة الدراسة، وبشرط عدم الرسوب (F) في أي مقرر."""
            },
            {
                "category": "rules",
                "question": "التقييم والامتحانات",
                "answer": """3. التقييم والامتحانات
توزيع الدرجات: تشمل أعمال الفصل، امتحان منتصف الفصل، الشفهي/العملي، والامتحان التحريري النهائي.
نسبة الحضور: يشترط حضور 75% على الأقل للسماح بدخول الامتحان النهائي.
تعديل التسجيل: متاح خلال أول أسبوعين في فصلي الخريف والربيع، وأول أسبوع في الصيفي."""
            },
            {
                "category": "rules",
                "question": "البرامج الأكاديمية ومجالات العمل",
                "answer": """4. البرامج الأكاديمية ومجالات العمل
هندسة الإنشاءات وإدارة التشييد: تركز على تحليل المنشآت، ميكانيكا التربة، وتصميم الخرسانة والمشاريع. يمكن للخريج العمل كمهندس تصميم، تنفيذ، تقدير تكاليف، أو مدير مشاريع.
هندسة الميكاترونيات: تركز على النظم الكهروميكانيكية، الروبوتات، والتحكم الآلي. تشمل مجالات العمل شركات المقاولات، المصاعد، الصناعات الدوائية والغذائية، والصيانة."""
            }
        ]

        # 2. Specific FAQs
        faqs = [
            {
                "question": "أقل مجموع للنجاح كام؟ (درجة النجاح من كام في المادة؟)",
                "answer": "يعتبر الطالب ناجحاً في المقرر بحصوله على 60% (تقدير D) من مجموع درجات المقرر، بشرط أن يحصل على 30% على الأقل من درجات الامتحان التحريري النهائي."
            },
            {
                "question": "ازاي اخد مرتبة الشرف؟ (شروط مرتبه الشرف)",
                "answer": "تمنح مرتبة الشرف للطالب الذي لا يقل معدله التراكمي عن 3.6 خلال جميع الفصول الدراسية، ويشترط ألا يكون قد حصل على تقدير (F) في أي مقرر طوال دراسته."
            },
            {
                "question": "يعني ايه تقدير W؟ (أو I أو F)",
                "answer": "• W: منسحب (Withdrawn).\n• I: غير مكتمل (Incomplete) لعذر مقبول.\n• F: راسب (Fail)."
            },
            {
                "question": "انا واقع وعلي انذار اسجل كام ساعة؟ (عدد الساعات للمنذر اكاديميا)",
                "answer": "الطالب المنذر أكاديمياً (GPA أقل من 2.00) لا يسمح له بتسجيل أكثر من 14 ساعة معتمدة أو 5 مقررات دراسية في فصلي الخريف أو الربيع."
            },
            {
                "question": "اسجل كام مادة في الصيفي؟ (الحد الاقصى للساعات في الصيف)",
                "answer": "يمكن للطالب التسجيل في الفصل الصيفي في مقررات لا تزيد ساعاتها عن 6 ساعات معتمدة أو مقررين دراسيين كحد أقصى."
            },
            {
                "question": "عايز احذف ماده (امتى اخر ميعاد للاضافة والحذف؟)",
                "answer": "يحق لك تعديل التسجيل بالحذف أو الإضافة خلال أسبوعين من بدء الدراسة في الخريف أو الربيع، وفي الأسبوع الأول فقط في الفصل الصيفي."
            },
            {
                "question": "اتخرج امتى؟ (شروط الحصول على البكالوريوس)",
                "answer": "يتطلب التخرج: اجتياز 165 ساعة معتمدة، بمتوسط تراكمي (GPA) لا يقل عن 2.00، واجتياز مشروع التخرج، والتدريب الصيفي لمدة 8 أسابيع."
            },
            {
                "question": "امتى اسجل مشروع تخرج 1؟ (شروط تسجيل البروجكت)",
                "answer": "لتسجيل مقرر مشروع (1)، يجب أن يكون الطالب قد اجتاز 120 ساعة معتمدة بنجاح."
            },
            {
                "question": "مسموح غياب كام في الميه؟ (نسبة الحضور لدخول الفاينال)",
                "answer": "يجب ألا تقل نسبة حضور الطالب عن 75% من المحاضرات والتمارين لكي يُسمح له بحضور الامتحان التحريري النهائي."
            },
            {
                "question": "المحاضرة بكام ساعة؟ (حساب ساعات الكريدت اور)",
                "answer": "• ساعة المحاضرة = 1 ساعة معتمدة.\n• ساعتان تمارين (Tutorial) = 1 ساعة معتمدة.\n• 2-3 ساعات عملي (Lab) = 1 ساعة معتمدة."
            }
        ]

        # 3. PDF Content (Engineering Perspective)
        pdf_filename = "Prof_Gamal_Eng_2023.pdf"
        try:
            import pypdf
            import os
            
            if os.path.exists(pdf_filename):
                self.stdout.write(f"Processing {pdf_filename}...")
                pdf_text = ""
                with open(pdf_filename, 'rb') as f:
                    reader = pypdf.PdfReader(f)
                    for page in reader.pages:
                        pdf_text += page.extract_text() + "\n"
                
                # Clean up text slightly (optional)
                pdf_text = pdf_text.strip()
                
                if pdf_text:
                    UniversityKnowledge.objects.create(
                        category='engineering_pdf',
                        question=None,
                        answer=pdf_text
                    )
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported PDF content ({len(pdf_text)} chars)."))
                else:
                    self.stdout.write(self.style.WARNING(f"PDF found but no text could be extracted."))
            else:
                 self.stdout.write(self.style.WARNING(f"{pdf_filename} not found in project root."))

        except ImportError:
            self.stdout.write(self.style.ERROR("pypdf is not installed. Please run 'pip install pypdf' to import the PDF context."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading PDF: {e}"))


        # Bulk Create Main Rules and FAQs
        for item in rules:
            UniversityKnowledge.objects.create(
                category=item['category'],
                question=item['question'],
                answer=item['answer']
            )
            self.stdout.write(self.style.SUCCESS(f"Added Rule: {item['question']}"))

        for item in faqs:
            UniversityKnowledge.objects.create(
                category='faq',
                question=item['question'],
                answer=item['answer']
            )
            self.stdout.write(self.style.SUCCESS(f"Added FAQ: {item['question']}"))

        self.stdout.write(self.style.SUCCESS('Successfully populated University Knowledge Base'))
