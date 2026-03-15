"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""

import folium
from extractor import extract_all

def sort_by_time(arr):
    return sorted(arr, key=lambda x: x['datetime'])


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    gps_images = [img for img in images_data if img["has_gps"] and img["datetime"]]

    if not gps_images:
        return "<h2>No GPS data found</h2>"

    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    gps_images = sort_by_time(gps_images)
    path_coords = [(img["latitude"], img["longitude"]) for img in gps_images]
    colors = ["blue","green","red","black","gray","purple"]
    dict_color_for_camera = {}
    for i, img in enumerate(gps_images):
        if colors == []:
            colors = ["blue", "green", "red", "black", "gray", "purple","orange","lightgray","white","lightblue"]

        if img["camera_model"] in dict_color_for_camera:
            color = dict_color_for_camera[img["camera_model"]]
        else:
            color = colors.pop(0)
            dict_color_for_camera[img["camera_model"]] = color
        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=folium.Popup(
                f"<b>📷{img['filename']}</b><br>"
                 f"Photo #: {i + 1}<br>"
                f"Time: {img['datetime']}<br>"
                f"Device:{img.get('camera_model', '')}".strip() + "<br>"
                f"Coordinates:<br>{img['latitude']:.6f}, {img['longitude']:.6f}",
                max_width=200
            ),
            icon=folium.Icon(color=color,icon="camera")

        ).add_to(m)

        # 2. הוספת הקו למפה
    folium.PolyLine(
        locations=path_coords,
        color="blue",
        weight=3.5,
        opacity=0.7
    ).add_to(m)

    return m._repr_html_()



if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
    data = extract_all("../images/ready")
    html = create_map(data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")