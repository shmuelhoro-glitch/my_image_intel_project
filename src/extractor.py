from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""

def dms_to_decimal(dms_tuple, ref):
    degrees = dms_tuple[0][0] / dms_tuple[0][1]
    minutes = dms_tuple[1][0] / dms_tuple[1][1]
    seconds = dms_tuple[2][0] / dms_tuple[2][1]
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in [b'S', b'W', 'S', 'W']:
        decimal = -decimal
    return f"{decimal:.4f}"




def has_gps(data: dict):
    if "GPSInfo" in data:
        gps_info = data["GPSInfo"]
        return 2 in gps_info and 4 in gps_info
    return False



def latitude(data: dict):
    try:
        gps_info = data["GPSInfo"]
        lat_tuple = tuple((float(x),1) for x in gps_info[2])
        lat_ref = gps_info[1]
        return float(dms_to_decimal(lat_tuple,lat_ref))
    except:
        return None

def longitude(data: dict):
    try:
        gps_info = data["GPSInfo"]
        lon_tuple = tuple((float(x),1) for x in gps_info[4])
        lon_ref = gps_info[3]
        return float(dms_to_decimal(lon_tuple, lon_ref))
    except:
        return None

def datatime(data: dict):
    try:
        return data["DateTimeOriginal"].replace(":", "-", 2)
    except KeyError:
        return None


def camera_make(data: dict):
    try:
        return data["Make"].strip("\x00")
    except KeyError:
        return None


def camera_model(data: dict):
    try:
        return data["Model"].strip("\x00")
    except KeyError:
        return None


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    path = Path(folder_path)
    all_results = []
    for file_path in path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in [".jpg",".jpeg",".png",".tiff"]:
            metadata = extract_metadata(str(file_path))
            all_results.append(metadata)
    return all_results