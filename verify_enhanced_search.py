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
    return t

def get_lang(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return 'ar-eg'
    return 'en-us'

def search(user_message, data_source):
    query_norm = normalize(user_message)
    query_words = set(query_norm.split())
    query_lang = get_lang(user_message)
    
    if not query_norm:
        return "هذا السؤال غير موجود حاليًا في دليل الكلية.", 0

    best_entry = None
    max_score = 0
    
    for entry in data_source:
        score = 0
        q_text = entry.get('question', '')
        q_norm = normalize(q_text)
        q_words = set(q_norm.split())
        
        if not q_norm: continue
        
        # 1. Substring Match Bonus
        if query_norm in q_norm or q_norm in query_norm:
            score += 0.5
        
        # 2. Word Overlap
        overlap = query_words & q_words
        if overlap:
            word_sim = len(overlap) / len(query_words | q_words)
            score += word_sim * 0.4
        
        # 3. Fuzzy Character Similarity
        fuzzy_ratio = difflib.SequenceMatcher(None, query_norm, q_norm).ratio()
        score += fuzzy_ratio * 0.2
        
        # 4. Language weighting
        if entry.get('language') == query_lang:
            score += 0.05
        
        if score > max_score:
            max_score = score
            best_entry = entry
        
        if score > 1.2: break

    if best_entry and max_score >= 0.3:
        return best_entry['answer'], max_score
    else:
        return "هذا السؤال غير موجود حاليًا في دليل الكلية.", max_score

# Test Cases
test_queries = [
    "ساعات معتمدة",          # Partial Arabic
    "تسجيل المواد",          # Partial Arabic
    "GPA drops",            # Partial English
    "GPA drps",             # Typo English
    "الساعات المعتدمة",       # Typo Arabic
]

print("--- ENHANCED SEARCH VERIFICATION ---")
for q in test_queries:
    ans, score = search(q, QA_DATA)
    print(f"\nQuery: {q}")
    print(f"Score: {score:.2f}")
    print(f"Answer: {ans}")
