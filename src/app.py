import os
import uuid
import shutil
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# ייבוא המודולים של המערכת
from extractor import extract_all
from map_view import create_map
from timeline import create_timeline
from analyzer import analyze
from report import create_report

app = Flask(__name__)

# הגדרת נתיב התיקייה: images/uploads (תיקייה אחות ל-src)
# os.path.dirname(__file__) נותן לנו את המיקום של app.py (בתוך src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_BASE = os.path.join(BASE_DIR, '..', 'images', 'uploads')

# יצירת תיקיית הבסיס אם היא לא קיימת
os.makedirs(UPLOAD_BASE, exist_ok=True)


@app.route('/')
def index():
    """דף הבית - טופס להעלאת תמונות"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_images():
    """מקבל תמונות, שומר אותן בתיקייה ייעודית ומריץ ניתוח"""

    # 1. יצירת תיקייה ייחודית לסשן הנוכחי (למניעת ערבוב בין משתמשים)
    session_id = str(uuid.uuid4())
    temp_folder = os.path.join(UPLOAD_BASE, session_id)
    os.makedirs(temp_folder, exist_ok=True)

    # 2. קבלת הקבצים מהשדה 'photos' שב-HTML
    uploaded_files = request.files.getlist("photos")

    if not uploaded_files or uploaded_files[0].filename == '':
        return "לא נבחרו תמונות לניתוח", 400

    # 3. שמירת הקבצים בתיקייה הזמנית
    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(temp_folder, filename))

    try:
        # שלב 1: שליפת נתונים מהתיקייה שנוצרה
        images_data = extract_all(temp_folder)

        if not images_data:
            return "לא נמצאו נתונים בתמונות שהועלו", 400

        # שלב 2: יצירת מפה
        map_html = create_map(images_data)

        # שלב 3: ציר זמן
        timeline_html = create_timeline(images_data)

        # שלב 4: ניתוח תובנות
        analysis = analyze(images_data)

        # שלב 5: הרכבת דו"ח HTML סופי
        report_html = create_report(images_data, map_html, timeline_html, analysis)

        return report_html

    finally:
        # אופציונלי: מחיקת התיקייה הזמנית מהשרת לאחר יצירת הדו"ח
        shutil.rmtree(temp_folder)
        pass


if __name__ == '__main__':
    app.run(debug=True)