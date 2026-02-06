import re
import difflib

# Mocking the QA data for testing
QA_DATA = [
    {
        "question": "What happens if my GPA drops below 2.00?",
        "answer": "If your GPA is below 2.00, you will be under academic warning and can only register for a maximum of 14 credit hours or 5 courses.",
        "language": "en"
    },
    {
        "question": "ما هي الساعات المعتمدة؟",
        "answer": "الساعة المعتمدة هي وحدة قياس العبء الدراسي للمقرر.",
        "language": "ar-eg"
    },
    {
        "question": "كيف يتم تسجيل المواد؟",
        "answer": "يتم تسجيل المواد خلال فترة التسجيل عبر شؤون الطلاب.",
        "language": "ar-eg"
    }
]

def normalize(text):
    if not text: return ""
    t = str(text).lower().strip()
    t = re.sub(r'[^\w\s\u0600-\u06FF]', '', t)
    # Arabic Unification
    t = re.sub(r'[أإآ]', 'ا', t)
    t = re.sub(r'ة', 'ه', t)
    t = re.sub(r'ى', 'ي', t)
    return t

def get_lang(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return 'ar-eg'
    return 'en-us'

def search(user_message, data_source):
    query_norm = normalize(user_message)
    query_words = list(query_norm.split())
    query_lang = get_lang(user_message)
    
    if not query_norm:
        return "هذا السؤال غير موجود حاليًا في دليل الكلية.", 0

    best_entry = None
    max_score = 0
    
    for entry in data_source:
        score = 0
        q_text = entry.get('question', '')
        q_norm = normalize(q_text)
        q_words = list(q_norm.split())
        
        if not q_norm: continue
        
        if query_norm in q_norm or q_norm in query_norm:
            score += 0.5
        
        if query_words and q_words:
            matches = 0
            for qw in query_words:
                best_word_sim = 0
                for target_w in q_words:
                    if qw == target_w:
                        sim = 1.0
                    else:
                        sim = difflib.SequenceMatcher(None, qw, target_w).ratio()
                    if sim > best_word_sim:
                        best_word_sim = sim
                    if best_word_sim == 1.0: break
                if best_word_sim > 0.75:
                    matches += best_word_sim
            score += (matches / max(len(query_words), len(q_words))) * 0.5
        
        phrase_sim = difflib.SequenceMatcher(None, query_norm, q_norm).ratio()
        score += phrase_sim * 0.3
        
        if entry.get('language') == query_lang:
            score += 0.05
        
        if score > max_score:
            max_score = score
            best_entry = entry
        
        if score > 1.3: break

    if best_entry and max_score >= 0.35:
        return best_entry['answer'], max_score
    else:
        return "هذا السؤال غير موجود حاليًا في دليل الكلية.", max_score

# Test Cases
test_queries = [
    "الساعات المعتدمه",       # Typo (ت -> د) and (ة -> ه)
    "الإنذار",              # Alif with Hamza
    "الانذار",              # Alif without Hamza (should normalize to same as above)
    "GPA droppps",          # Heavy typo
    "تسجيل ا لمواد",        # Extra space
]

print("--- ADVANCED TYPO CORRECTION VERIFICATION ---")
for q in test_queries:
    ans, score = search(q, QA_DATA)
    print(f"\nQuery: {q}")
    print(f"Score: {score:.2f}")
    print(f"Answer: {ans[:50]}...")
