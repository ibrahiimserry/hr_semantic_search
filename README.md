

https://github.com/user-attachments/assets/02833f25-a718-4cc1-906f-8d18d376bfd9

# محرك البحث الدلالي للموارد البشرية 🔍

نظام ذكاء اصطناعي لمطابقة المواهب في قسم الموارد البشرية. يقوم بالبحث الدلالي (Semantic Search) للعثور على أفضل المرشحين بناءً على الوصف الوظيفي.

مبني باستخدام:
- مكتبة `sentence-transformers` مع نموذج `all-MiniLM-L6-v2` لتحويل النصوص إلى متجهات (Embeddings)
- مكتبة `FAISS` من فيسبوك كقاعدة بيانات متجهية (Vector Database)
- لغة بايثون Python

---

## 📁 هيكل المشروع

```
hr_semantic_search/
│
├── hr_search.py          # السكريبت الرئيسي (شغّل الملف ده)
├── mock_resumes.json     # بيانات المرشحين الوهمية (50 سيرة ذاتية)
├── architecture.md       # تقرير تصميم النظام: التوسع وحماية البيانات
├── requirements.txt      # قائمة بكل مكتبات بايثون المطلوبة
└── README.md             # الملف ده
```

---

## ⚙️ طريقة التشغيل

### الخطوة الأولى — تفعيل البيئة الافتراضية
```powershell
.\venv\Scripts\activate
```

### الخطوة الثانية — تشغيل السكريبت
```powershell
python hr_search.py
```

### الخطوة الثالثة — اكتب الوصف الوظيفي
بعد ما يتحمل البرنامج، هيظهرلك السطر ده:
```
============================================================
  HR Semantic Search Engine - Ready!
  Available roles: Python Developer, Data Scientist,
                   Frontend Engineer, DevOps Engineer,
                   AI Engineer, Product Manager
  Type 'exit' to quit.
============================================================

Enter Job Description to search:
```

اكتب الوصف الوظيفي اللي عايزه واضغط **Enter**. البرنامج هيرجعلك **أفضل 3 مرشحين** بصيغة JSON.

عشان تقفل البرنامج، اكتب `exit` واضغط **Enter**.

---

## 💡 أمثلة على الوصف الوظيفي للتجربة

انسخ أي مثال من الأمثلة دي والصقه في البحث:

| الوظيفة المطلوبة | مثال للـ Job Description |
|---|---|
| **AI Engineer** | `Looking for AI Engineer with Python and NLP` |
| **DevOps Engineer** | `Need DevOps Engineer skilled in Docker and Kubernetes` |
| **Frontend Engineer** | `Frontend developer with React and TypeScript experience` |
| **Data Scientist** | `Data Scientist experienced in Machine Learning and Pandas` |
| **Python Developer** | `Python backend developer with Django and REST APIs experience` |
| **Product Manager** | `Product Manager with Agile and Scrum experience` |

> **ملاحظة مهمة:** البحث **دلالي (Semantic)**، يعني البرنامج بيفهم *معنى* كلامك مش بس الكلمات بالحرف.
> مثلاً لو كتبت `"AI expert who knows vectors"` هيرجع نتائج AI Engineer بدون مشكلة!

---

## 📤 مثال على النتيجة

```json
{
    "job_description": "Looking for AI Engineer with Python and NLP",
    "top_candidates": [
        {
            "candidate_id": 0,
            "name": "Ibrahim Expert",
            "role": "AI Engineer",
            "match_score": "94.8%",
            "reasoning": "Candidate matches key required skills: Python, NLP, FAISS, Vector Databases, Semantic Search. They have 5 years of experience as a AI Engineer."
        },
        {
            "candidate_id": 11,
            "name": "Fatima Ibrahim",
            "role": "AI Engineer",
            "match_score": "93.9%",
            "reasoning": "Candidate matches key required skills: FAISS, Semantic Search, NLP, Python. They have 10 years of experience as a AI Engineer."
        },
        {
            "candidate_id": 36,
            "name": "Fatima Mahmoud",
            "role": "AI Engineer",
            "match_score": "93.8%",
            "reasoning": "Candidate matches key required skills: Semantic Search, FAISS. They have 6 years of experience as a AI Engineer."
        }
    ]
}
```

---

## 🏗️ البنية التحتية والتوسع

اقرأ ملف [architecture.md](architecture.md) للاطلاع على:
- كيفية التعامل مع **حماية البيانات (Data Privacy)**: إزالة المعلومات الشخصية، التشفير، والصلاحيات
- كيفية **التوسع** لأكثر من 50,000 سيرة ذاتية باستخدام خوارزميات FAISS المتقدمة (IVF, HNSW)
