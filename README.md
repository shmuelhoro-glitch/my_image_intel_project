# Image Intel - מערכת חילוץ מודיעין מתמונות

## מה זה?

מערכת שמקבלת תמונות ומייצרת דו"ח מודיעיני: מיקומים על מפה, ציר זמן, זיהוי דפוסים וקשרים.

## יצירת Fork
יצירה של עותק בgithub האישי של *ראש הצוות*. שאר אנשי הצוות יעבדו על העותק הזה.
הגשת הפרויקט תעשה מהfork הזה.
<img width="1418" height="240" alt="image" src="https://github.com/user-attachments/assets/7f192c20-bc8c-47a3-9bab-b4aa53f9a9e0" />


## התקנה

```bash
git clone <repo-url>
cd image_intel
pip install -r requirements.txt
```

## הרצה

```bash
python src/app.py
```

גשו ל-`http://localhost:5000` בדפדפן.

## מבנה הפרויקט

```
image_intel/
├── README.md
├── requirements.txt
├── docs/                          # מסמכים ומדריכים
│   ├── briefing.md                # תדריך כללי
│   ├── team1_data_guide.md        # מדריך רביעייה 1
│   ├── team2_visual_guide.md      # מדריך רביעייה 2
│   ├── team3_app_guide.md         # מדריך רביעייה 3
│   ├── qa_guide.md                # מדריך צוות QA
│   ├── schedule.md                # לוח זמנים
│   └── api_contract.md            # הגדרת ממשקים בין המודולים
├── images/
│   └── sample_data/               # תמונות לבדיקה (יתווספו)
├── src/
│   ├── app.py                     # Flask app - צוות 3 זוג A
│   ├── extractor.py               # שליפת EXIF - צוות 1 זוג A
│   ├── map_view.py                # מפה - צוות 1 זוג B
│   ├── timeline.py                # ציר זמן - צוות 2 זוג A
│   ├── analyzer.py                # ניתוח דפוסים - צוות 2 זוג B
│   ├── report.py                  # הרכבת דו"ח - צוות 3 זוג B
│   ├── templates/
│   │   └── index.html             # דף הבית
│   └── static/                    # קבצים סטטיים
├── tests/
│   ├── test_extractor.py          # צוות QA
│   ├── test_map_view.py
│   ├── test_timeline.py
│   ├── test_analyzer.py
│   └── test_integration.py
└── tools/
    └── inject_exif.py             # כלי להכנת תמונות (למדריך בלבד)
```

## צוותים

| רביעייה | זוג A | זוג B |
|---------|-------|-------|
| 1 - Data | extractor.py | map_view.py |
| 2 - Visual | timeline.py | analyzer.py |
| 3 - App | app.py (Flask) | report.py (HTML) |
| QA | בדיקות + Code Review (2 תלמידים) |

## עבודה עם Git

כל זוג עובד על branch נפרד:
```bash
git checkout -b feature/extractor
# עבודה...
git add .
git commit -m "Add GPS extraction"
git push origin feature/extractor
# פתחו PR ב-GitHub
```
