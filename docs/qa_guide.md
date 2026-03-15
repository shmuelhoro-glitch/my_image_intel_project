# צוות QA - מדריך מפורט

## התפקיד שלכם

אתם שומרי האיכות של הפרויקט. בלעדיכם, הקוד לא ייבדק, באגים לא יימצאו, והאינטגרציה תיכשל. אתם רואים את כל הקוד ויש לכם את התמונה הכללית.

## המשימות שלכם

1. **כתיבת בדיקות** (pytest) לכל מודול
2. **Code Review** על כל PR
3. **בדיקות אינטגרציה** - שהכל עובד ביחד
4. **עזרה לצוותים** שנתקעים

---

## לוח זמנים מומלץ

| שעה | משימה |
|-----|-------|
| 08:00-09:00 | הכינו את סביבת הבדיקות, כתבו בדיקות ראשונות עם נתונים מזויפים |
| 09:00-11:00 | Code Review על PRs ראשונים, עדכון בדיקות |
| 11:00-13:00 | בדיקות מול קוד אמיתי, דיווח באגים |
| 13:00-14:00 | בדיקות אינטגרציה, עזרה בחיבור |
| 14:00-16:00 | בדיקה סופית מקצה לקצה |

---

## חלק 1: הכנת סביבת בדיקות

### התקנת pytest
```bash
pip install pytest
```

### מבנה תיקיית tests
```
tests/
├── test_extractor.py
├── test_map_view.py
├── test_timeline.py
├── test_analyzer.py
└── test_integration.py
```

### הרצת בדיקות
```bash
pytest tests/ -v
```

---

## חלק 2: כתיבת בדיקות

### test_extractor.py
```python
import pytest
import os

# בהתחלה, לפני שהמודול מוכן, אפשר לדלג
# pytest.importorskip("extractor")

def test_extract_metadata_returns_dict():
    from extractor import extract_metadata
    result = extract_metadata("images/sample_data/IMG_001.jpg")
    assert isinstance(result, dict)

def test_extract_metadata_has_required_fields():
    from extractor import extract_metadata
    result = extract_metadata("images/sample_data/IMG_001.jpg")
    required = ["filename", "datetime", "latitude", "longitude", 
                "camera_make", "camera_model", "has_gps"]
    for field in required:
        assert field in result, f"Missing field: {field}"

def test_extract_metadata_gps_is_float_or_none():
    from extractor import extract_metadata
    result = extract_metadata("images/sample_data/IMG_001.jpg")
    if result["has_gps"]:
        assert isinstance(result["latitude"], float)
        assert isinstance(result["longitude"], float)
    else:
        assert result["latitude"] is None
        assert result["longitude"] is None

def test_extract_all_returns_list():
    from extractor import extract_all
    result = extract_all("images/sample_data")
    assert isinstance(result, list)
    assert len(result) > 0

def test_extract_all_handles_empty_folder(tmp_path):
    from extractor import extract_all
    result = extract_all(str(tmp_path))
    assert isinstance(result, list)
    assert len(result) == 0
```

### test_map_view.py
```python
def get_fake_data():
    return [
        {"filename": "t1.jpg", "latitude": 32.0, "longitude": 34.7, 
         "has_gps": True, "camera_model": "Samsung", "datetime": "2025-01-12"},
        {"filename": "t2.jpg", "latitude": 31.7, "longitude": 35.2, 
         "has_gps": True, "camera_model": "iPhone", "datetime": "2025-01-13"},
        {"filename": "t3.jpg", "latitude": None, "longitude": None, 
         "has_gps": False, "camera_model": None, "datetime": None},
    ]

def test_create_map_returns_html():
    from map_view import create_map
    result = create_map(get_fake_data())
    assert isinstance(result, str)
    assert len(result) > 0

def test_create_map_handles_no_gps():
    from map_view import create_map
    no_gps = [{"filename": "x.jpg", "has_gps": False, "latitude": None, 
               "longitude": None, "camera_model": None, "datetime": None}]
    result = create_map(no_gps)
    assert isinstance(result, str)

def test_create_map_handles_empty_list():
    from map_view import create_map
    result = create_map([])
    assert isinstance(result, str)
```

### test_analyzer.py
```python
def get_fake_data():
    return [
        {"filename": "t1.jpg", "latitude": 32.0, "longitude": 34.7, 
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23", 
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "t2.jpg", "latitude": 31.7, "longitude": 35.2, 
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro", 
         "datetime": "2025-01-13 09:00:00"},
    ]

def test_analyze_returns_dict():
    from analyzer import analyze
    result = analyze(get_fake_data())
    assert isinstance(result, dict)

def test_analyze_has_required_fields():
    from analyzer import analyze
    result = analyze(get_fake_data())
    assert "total_images" in result
    assert "images_with_gps" in result
    assert "unique_cameras" in result
    assert "insights" in result

def test_analyze_counts_correctly():
    from analyzer import analyze
    result = analyze(get_fake_data())
    assert result["total_images"] == 2
    assert result["images_with_gps"] == 2

def test_analyze_handles_empty():
    from analyzer import analyze
    result = analyze([])
    assert result["total_images"] == 0
```

### test_integration.py
```python
def test_full_pipeline():
    """הבדיקה הכי חשובה - כל הצינור מקצה לקצה"""
    from extractor import extract_all
    from map_view import create_map
    from timeline import create_timeline
    from analyzer import analyze
    from report import create_report
    
    images_data = extract_all("images/sample_data")
    assert len(images_data) > 0
    
    map_html = create_map(images_data)
    assert isinstance(map_html, str)
    
    timeline_html = create_timeline(images_data)
    assert isinstance(timeline_html, str)
    
    analysis = analyze(images_data)
    assert isinstance(analysis, dict)
    
    report_html = create_report(images_data, map_html, timeline_html, analysis)
    assert "<html" in report_html.lower()
```

---

## חלק 3: Code Review

### מה לבדוק ב-PR
1. **הפורמט נכון?** - התוצאה תואמת ל-`api_contract.md`?
2. **טיפול בשגיאות** - מה קורה אם אין EXIF? אם התיקייה ריקה?
3. **קריאות** - שמות משתנים ברורים? יש הערות במקומות מבלבלים?
4. **לא קורס** - הריצו את הקוד בעצמכם

### איך לכתוב הערות טובות

לא טוב:
```
"זה לא טוב"
"תשנה את זה"
```

טוב:
```
"מה קורה אם latitude הוא None? כדאי להוסיף בדיקה:
if latitude is None:
    return None"
```

```
"הפורמט לא תואם ל-api_contract.md - צריך 'has_gps' (bool) במקום 'gps' (string)"
```

---

## חלק 4: עזרה לצוותים

### סימנים שמישהו צריך עזרה
- שקטים מדי (לא שואלים, לא עושים commit)
- הרבה שגיאות באותו PR
- לא מתקדמים כבר שעה

### איך לעזור נכון
- **אל תכתבו להם קוד!** תכוונו אותם
- "נסו לחפש בגוגל X"
- "תסתכלו על הדוגמה ב-api_contract.md"
- "הרצתם את הקוד? מה השגיאה?"

---

## צ'קליסט יומי

- [ ] pytest מותקן ועובד
- [ ] test_extractor.py - לפחות 3 בדיקות
- [ ] test_map_view.py - לפחות 3 בדיקות
- [ ] test_timeline.py - לפחות 3 בדיקות
- [ ] test_analyzer.py - לפחות 3 בדיקות
- [ ] test_integration.py - בדיקת צינור מלא
- [ ] עשיתם Code Review על לפחות 2 PRs
- [ ] בדיקה סופית - המערכת עובדת מקצה לקצה
