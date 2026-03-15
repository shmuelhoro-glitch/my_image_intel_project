from collections import Counter
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from functools import lru_cache

geolocator = Nominatim(user_agent="image_intel_system")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)


@lru_cache(maxsize=512)
def get_city_offline(lat, lon):
    lat = round(lat, 3)
    lon = round(lon, 3)
    try:
        location = reverse((lat, lon), language="he")
        if location:
            address = location.raw.get("address", {})
            return (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or "מקום לא ידוע"
            )
    except Exception as e:
        print(f"שגיאת מיקום: {e}")

    return "מיקום חסר"


def detect_camera_switches(images_data):

    sorted_images = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda x: x["datetime"]
    )

    switches = []

    for i in range(1, len(sorted_images)):

        prev_cam = sorted_images[i - 1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")

        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })

    return switches


def analyze(images_data: list[dict]) -> dict:

    total_images = len(images_data)

    images_with_gps = [img for img in images_data if img["has_gps"]]
    images_with_datetime = [img for img in images_data if img["datetime"]]

    # מצלמות
    unique_cameras = []

    for img in images_data:

        make = img.get("camera_make")
        model = img.get("camera_model")

        if make and model:

            cam = f"{make} {model}"

            if cam not in unique_cameras:
                unique_cameras.append(cam)

    # טווח זמן
    if images_with_datetime:

        sorted_dates = sorted(img["datetime"] for img in images_with_datetime)

        date_range = {
            "start": sorted_dates[0],
            "end": sorted_dates[-1]
        }

    else:
        date_range = None

    # ערים
    cities = []

    for img in images_with_gps:

        city = get_city_offline(img["latitude"], img["longitude"])

        cities.append(city)

    city_counter = Counter(cities)

    switches = detect_camera_switches(images_data)

    insights = []

    if total_images == 0:
        insights.append("לא נמצאו תמונות לניתוח")

    else:

        insights.append(f"נסרקו {total_images} תמונות בסך הכול")

        if len(unique_cameras) > 1:
            insights.append(f"זוהו {len(unique_cameras)} מכשירי צילום שונים")

        if switches:
            insights.append(f"זוהו {len(switches)} החלפות מכשיר לאורך ציר הזמן")

        if city_counter:
            most_common_city, count = city_counter.most_common(1)[0]
            insights.append(f"ריכוז פעילות באזור {most_common_city} ({count} תמונות)")

        if date_range:
            insights.append(
                f"טווח הצילום נע בין {date_range['start']} לבין {date_range['end']}"
            )

    return {
        "total_images": total_images,
        "images_with_gps": len(images_with_gps),
        "images_with_datetime": len(images_with_datetime),
        "unique_cameras": unique_cameras,
        "date_range": date_range,
        "camera_switches": switches,
        "cities": dict(city_counter),
        "insights": insights
    }