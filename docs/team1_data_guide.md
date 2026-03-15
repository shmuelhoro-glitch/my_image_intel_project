# רביעייה 1 - Data: מדריך מפורט

## התפקיד שלכם

אתם הבסיס של כל הפרויקט. כל הצוותים האחרים תלויים בנתונים שאתם מחלצים. בלעדיכם אין פרויקט.

## חלוקת עבודה

| זוג | מודול | מה עושים |
|-----|-------|----------|
| A | extractor.py | שליפת EXIF מתמונות - GPS, תאריך, מכשיר |
| B | map_view.py | יצירת מפה אינטראקטיבית עם כל המיקומים |

---

## זוג A - extractor.py

### המטרה
לבנות מודול שמקבל נתיב לתמונה (או תיקייה) ומחזיר מילון עם כל המידע.

### הפלט שלכם (הפורמט המדויק!)
```python
{
    "filename": "IMG_001.jpg",
    "datetime": "2025-01-12 08:30:00",
    "latitude": 32.0853,
    "longitude": 34.7818,
    "camera_make": "Samsung",
    "camera_model": "Galaxy S23",
    "has_gps": True
}
```

אם אין מידע מסוים, החזירו `None` (לא string ריק!).

### ספריות מומלצות
- `Pillow` (PIL) - הספרייה הכי נפוצה לעבודה עם תמונות
- `piexif` - ספרייה ממוקדת ל-EXIF

### אתגרים שתפגשו

**1. המרת GPS:** ה-EXIF שומר GPS בפורמט מעלות-דקות-שניות (DMS), אתם צריכים מספר עשרוני.
```python
# EXIF נותן: ((32, 1), (5, 1), (7, 1)) = 32 מעלות, 5 דקות, 7 שניות
# אתם צריכים: 32.0853

def dms_to_decimal(dms_tuple, ref):
    degrees = dms_tuple[0][0] / dms_tuple[0][1]
    minutes = dms_tuple[1][0] / dms_tuple[1][1]
    seconds = dms_tuple[2][0] / dms_tuple[2][1]
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in [b'S', b'W', 'S', 'W']:
        decimal = -decimal
    return decimal
```

**2. תמונות בלי EXIF:** לא כל תמונה מכילה מידע. תמונות מ-WhatsApp, screenshots, ותמונות מהאינטרנט בדרך כלל ריקות. הקוד שלכם חייב לטפל בזה בלי לקרוס!

**3. פורמטים שונים:** JPEG תומך ב-EXIF, PNG בדרך כלל לא. טפלו רק ב-JPEG לשלב הראשון.

### סדר עבודה מומלץ
1. כתבו `extract_metadata(image_path)` - לתמונה בודדת
2. בדקו על תמונה עם EXIF מלא
3. בדקו על תמונה בלי EXIF (לא אמור לקרוס!)
4. כתבו `extract_all(folder_path)` - לתיקייה שלמה
5. וודאו שהפורמט מתאים ל-api_contract.md

---

## זוג B - map_view.py

### המטרה
לבנות מודול שמקבל רשימת מילונים (מ-extractor) ומייצר מפה אינטראקטיבית.

### ספריות מומלצות
- `folium` - מפות אינטראקטיביות מבוססות Leaflet

### טיפ קריטי
**אל תחכו לזוג A!** התחילו מיד עם נתונים מזויפים:
```python
fake_data = [
    {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818, 
     "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
     "datetime": "2025-01-12 08:30:00"},
    {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
     "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
     "datetime": "2025-01-13 09:00:00"},
]
```

### סדר עבודה מומלץ
1. צרו מפה בסיסית עם folium ונקודה אחת
2. הוסיפו popup - כשלוחצים על נקודה רואים שם קובץ, תאריך, מכשיר
3. צבעו נקודות לפי מכשיר (כל מכשיר צבע אחר)
4. הוסיפו קו מחבר בין הנקודות לפי סדר כרונולוגי
5. החזירו את המפה כ-HTML string

### דוגמה בסיסית
```python
import folium

def create_map(images_data):
    gps_images = [img for img in images_data if img["has_gps"]]
    
    if not gps_images:
        return "<h2>No GPS data found</h2>"
    
    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    
    for img in gps_images:
        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=f"{img['filename']}<br>{img['datetime']}<br>{img['camera_model']}",
        ).add_to(m)
    
    return m._repr_html_()
```

---

## עבודה עם Git

**זוג A:**
```bash
git checkout -b feature/extractor
# עבודה על extractor.py
git add src/extractor.py
git commit -m "Add EXIF extraction"
git push origin feature/extractor
```

**זוג B:**
```bash
git checkout -b feature/map
# עבודה על map_view.py
git add src/map_view.py
git commit -m "Add interactive map"
git push origin feature/map
```

**Code Review:** זוג A עושה Review לזוג B, ולהפך.

## תקשורת בין הזוגות

- **זוג A → זוג B:** "הפלט שלנו מוכן, ככה נראה המילון" / "שינינו שדה, שימו לב"
- **זוג B → זוג A:** "אנחנו צריכים שדה נוסף: X" / "הפורמט לא תואם, בואו נסנכרן"

## צ'קליסט סיום

### זוג A:
- [ ] `extract_metadata` עובד על תמונה עם EXIF מלא
- [ ] `extract_metadata` לא קורס על תמונה בלי EXIF
- [ ] `extract_all` עובד על תיקייה
- [ ] הפורמט תואם ל-api_contract.md
- [ ] PR נפתח ונבדק

### זוג B:
- [ ] מפה מציגה נקודות
- [ ] popup עם מידע בכל נקודה
- [ ] `create_map` מחזיר HTML string
- [ ] עובד עם נתונים מזויפים
- [ ] עובד עם נתונים אמיתיים מ-extractor
- [ ] PR נפתח ונבדק
