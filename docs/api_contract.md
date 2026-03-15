# API Contract - הגדרת ממשקים בין המודולים

מסמך זה מגדיר מה כל פונקציה מקבלת ומחזירה.
**כל הצוותים חייבים לעבוד לפי ההגדרות האלה.**

---

## extractor.py (צוות 1, זוג A)

```python
def extract_metadata(image_path: str) -> dict:
    """
    שולף EXIF מתמונה בודדת.
    
    מקבל: נתיב לקובץ תמונה
    מחזיר: מילון עם המידע, לדוגמה:
    {
        "filename": "IMG_001.jpg",
        "datetime": "2025-01-12 08:30:00",    # str או None אם אין
        "latitude": 32.0853,                   # float או None אם אין GPS
        "longitude": 34.7818,                  # float או None אם אין GPS
        "camera_make": "Samsung",              # str או None
        "camera_model": "Galaxy S23",          # str או None
        "has_gps": True                        # bool
    }
    """

def extract_all(folder_path: str) -> list[dict]:
    """
    שולף EXIF מכל התמונות בתיקייה.
    
    מקבל: נתיב לתיקייה
    מחזיר: רשימה של מילונים (כמו extract_metadata)
    """
```

---

## map_view.py (צוות 1, זוג B)

```python
def create_map(images_data: list[dict]) -> str:
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.
    
    מקבל: רשימת מילונים מ-extract_all (מסנן בעצמו רק תמונות עם GPS)
    מחזיר: string של HTML (המפה כ-HTML)
    """
```

---

## timeline.py (צוות 2, זוג A)

```python
def create_timeline(images_data: list[dict]) -> str:
    """
    יוצר ציר זמן ויזואלי של התמונות.
    
    מקבל: רשימת מילונים מ-extract_all (מסנן בעצמו רק תמונות עם datetime)
    מחזיר: string של HTML (ציר הזמן כ-HTML)
    """
```

---

## analyzer.py (צוות 2, זוג B)

```python
def analyze(images_data: list[dict]) -> dict:
    """
    מנתח את הנתונים ומוצא דפוסים.
    
    מקבל: רשימת מילונים מ-extract_all
    מחזיר: מילון עם תובנות, לדוגמה:
    {
        "total_images": 12,
        "images_with_gps": 10,
        "unique_cameras": ["Samsung Galaxy S23", "Apple iPhone 15 Pro"],
        "date_range": {"start": "2025-01-12", "end": "2025-01-16"},
        "insights": [
            "נמצאו 3 מכשירים שונים",
            "הסוכן החליף מכשיר ב-13/01",
            "ריכוז תמונות באזור תל אביב"
        ]
    }
    """
```

---

## report.py (צוות 3, זוג B)

```python
def create_report(images_data: list[dict], map_html: str, 
                  timeline_html: str, analysis: dict) -> str:
    """
    מרכיב את כל החלקים לדו"ח HTML אחד.
    
    מקבל:
        - images_data: רשימת מילונים מ-extract_all
        - map_html: HTML של המפה מ-create_map
        - timeline_html: HTML של ציר הזמן מ-create_timeline
        - analysis: מילון התובנות מ-analyze
    מחזיר: string של HTML מלא (הדו"ח הסופי)
    """
```

---

## app.py (צוות 3, זוג A)

```python
# Flask routes:

# GET /          -> דף הבית עם אפשרות בחירת תיקייה
# POST /analyze  -> מקבל נתיב תיקייה, מריץ את כל המודולים, מחזיר דו"ח
```

---

## איך לעבוד עם הממשקים

1. **התחילו עם נתונים מזויפים!** אל תחכו שצוות אחר יסיים. צרו רשימת מילונים ידנית לבדיקה:

```python
fake_data = [
    {
        "filename": "test1.jpg",
        "datetime": "2025-01-12 08:30:00",
        "latitude": 32.0853,
        "longitude": 34.7818,
        "camera_make": "Samsung",
        "camera_model": "Galaxy S23",
        "has_gps": True
    },
    {
        "filename": "test2.jpg",
        "datetime": "2025-01-13 09:00:00",
        "latitude": 31.7683,
        "longitude": 35.2137,
        "camera_make": "Apple",
        "camera_model": "iPhone 15 Pro",
        "has_gps": True
    },
    {
        "filename": "test3.jpg",
        "datetime": None,
        "latitude": None,
        "longitude": None,
        "camera_make": None,
        "camera_model": None,
        "has_gps": False
    }
]
```

2. **כשהמודול האמיתי מוכן** - פשוט החליפו את fake_data בקריאה לפונקציה האמיתית.
