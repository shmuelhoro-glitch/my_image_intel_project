"""
timeline.py - מודול ציר זמן ויזואלי עם מספור, חלונות צפים בעברית וזיהוי יום/לילה
"""
from datetime import datetime

def create_timeline(images_data: list) -> str:
    if not images_data:
        return _render_empty_state()

    dated = [img for img in images_data if img.get("datetime")]
    undated = [img for img in images_data if not img.get("datetime")]
    dated.sort(key=lambda x: x["datetime"])

    camera_switches = _detect_camera_switches(dated)
    switch_indices = {s["index"] for s in camera_switches}
    time_gaps = _detect_time_gaps(dated, threshold_hours=12)
    gap_indices = {g["after_index"] for g in time_gaps}

    return _render_html(dated, undated, switch_indices, gap_indices, time_gaps)

# ──────────────────────────────────────────
# פונקציות עזר
# ──────────────────────────────────────────

def _parse_dt(dt_str: str | None) -> datetime | None:
    if not dt_str: return None
    formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y:%m:%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(dt_str.split(".")[0], fmt)
        except (ValueError, TypeError):
            continue
    return None

def _day_color(dt_str: str | None) -> str:
    palette = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6", "#f97316"]
    dt = _parse_dt(dt_str)
    return palette[dt.toordinal() % len(palette)] if dt else "#6b7280"

def _detect_camera_switches(sorted_images: list) -> list:
    switches = []
    for i in range(1, len(sorted_images)):
        prev, curr = sorted_images[i - 1].get("camera_model"), sorted_images[i].get("camera_model")
        if prev and curr and prev != curr:
            switches.append({"index": i})
    return switches

def _detect_time_gaps(sorted_images: list, threshold_hours: float = 6) -> list:
    gaps = []
    for i in range(1, len(sorted_images)):
        t1, t2 = _parse_dt(sorted_images[i - 1]["datetime"]), _parse_dt(sorted_images[i]["datetime"])
        if t1 and t2:
            diff_hours = (t2 - t1).total_seconds() / 3600
            if diff_hours >= threshold_hours:
                gaps.append({"after_index": i - 1, "hours": round(diff_hours, 1)})
    return gaps

# ──────────────────────────────────────────
# רינדור HTML
# ──────────────────────────────────────────

def _device_icon(camera_model: str | None) -> str:
    if not camera_model: return "📷"
    m = camera_model.lower()
    if any(x in m for x in ["iphone", "apple", "samsung", "galaxy"]): return "📱"
    if any(x in m for x in ["canon", "nikon", "sony"]): return "📸"
    return "🎥" if "gopro" in m else "📷"

def _render_card(img: dict, index: int, is_switch: bool, is_gap_after: bool, gap_hours: float | None) -> str:
    dt_raw = img.get("datetime")
    dt_obj = _parse_dt(dt_raw)
    time_icon = "🌞" if dt_obj and 6 <= dt_obj.hour < 18 else "🌙"

    filename = img.get("filename", f"image_{index + 1}")
    camera = " ".join(filter(None, [img.get("camera_make"), img.get("camera_model")])) or "מכשיר לא ידוע"
    color = _day_color(dt_raw)
    icon = _device_icon(img.get("camera_model"))

    # בניית שורות הנתונים לחלון הצף
    tooltip_rows = [f"<div>{time_icon} שעה: {dt_obj.strftime('%H:%M') if dt_obj else '--:--'}</div>"]

    gps = img.get("gps")
    if gps:
        tooltip_rows.append(f"<div>📍 קווי רוחב: {gps['lat']:.4f}</div>")
        tooltip_rows.append(f"<div>📍 קווי אורך: {gps['lon']:.4f}</div>")

    excluded = ["filename", "datetime", "camera_model", "camera_make", "gps"]
    for k, v in img.items():
        if k not in excluded and v:
            tooltip_rows.append(f"<div>• {k}: {v}</div>")

    side = "left" if index % 2 == 0 else "right"
    align, text_align = ("flex-end", "right") if side == "left" else ("flex-start", "left")

    return f'''
        <div class="timeline-row" style="justify-content:{align};">
            <div class="timeline-card" style="border-color:{color}; text-align:{text_align};">
                <div class="tooltip">
                    <strong>תמונה מס' {index + 1}</strong>
                    <div style="margin-top:5px;">{" ".join(tooltip_rows)}</div>
                </div>
                <div style="font-size:0.7rem; color:{color}; opacity:0.7; margin-bottom:2px;">#{index + 1}</div>
                <div class="card-header" style="color:{color};">
                    <span class="dt-str">📅 {dt_raw.replace("T", " ").split(".")[0] if dt_raw else "תאריך לא ידוע"} {time_icon}</span>
                </div>
                <div class="filename">🖼️ {filename}</div>
                <div class="camera">{icon} {camera}</div>
                {f'<span class="badge">🔄 החלפת מכשיר</span>' if is_switch else ''}
            </div>
        </div>
        {f'<div class="gap-marker"><span>⏳ פער של {gap_hours} שעות</span></div>' if is_gap_after else ""}
    '''

def _render_undated_section(undated: list) -> str:
    if not undated: return ""
    items = "".join(f'<li>🖼️ {img.get("filename", "unknown")}</li>' for img in undated)
    return f'<div class="undated-section"><h3>⚠️ ללא תאריך ({len(undated)})</h3><ul>{items}</ul></div>'

def _render_empty_state() -> str:
    return '<div style="text-align:center; padding:60px; color:#6b7280; font-family:sans-serif;"><h3>אין תמונות</h3></div>'

def _render_html(dated, undated, switch_indices, gap_indices, time_gaps) -> str:
    gap_map = {g["after_index"]: g["hours"] for g in time_gaps}
    cards_html = "".join(_render_card(img, i, i in switch_indices, i in gap_indices, gap_map.get(i)) for i, img in enumerate(dated))

    cameras = list({img.get("camera_model") for img in dated if img.get("camera_model")})
    camera_legend = "".join(f'<span class="legend-item">{_device_icon(c)} {c}</span>' for c in cameras)

    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
  :root {{ --bg: #0f1117; --surface: #1a1d27; --border: #2d3148; --text: #e2e8f0; --muted: #6b7280; }}
  body {{ background: var(--bg); color: var(--text); font-family: sans-serif; margin: 0; padding: 20px; }}
  .camera-legend {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
  .legend-item {{ border: 1px solid var(--border); border-radius: 15px; padding: 2px 10px; font-size: 0.8rem; }}
  .timeline-container {{ position: relative; max-width: 800px; margin: 0 auto; }}
  .timeline-container::before {{ content: ''; position: absolute; right: 50%; top: 0; bottom: 0; width: 2px; background: var(--border); transform: translateX(50%); }}
  .timeline-row {{ display: flex; margin-bottom: 15px; position: relative; }}
  .timeline-card {{ background: var(--surface); border: 2px solid; border-radius: 10px; padding: 12px 15px; width: 45%; position: relative; cursor: help; }}
  .tooltip {{ 
    visibility: hidden; position: absolute; z-index: 100; background: #2d3148; color: #fff; 
    padding: 10px; border-radius: 8px; width: 220px; font-size: 0.75rem; bottom: 105%; left: 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.5); opacity: 0; transition: opacity 0.2s; pointer-events: none;
    border: 1px solid var(--border); text-align: right; line-height: 1.4;
  }}
  .timeline-card:hover .tooltip {{ visibility: visible; opacity: 1; }}
  .timeline-card::after {{ content: ''; position: absolute; top: 20px; width: 12px; height: 12px; border-radius: 50%; background: currentColor; border: 2px solid var(--bg); }}
  .timeline-row:nth-child(odd) .timeline-card::after {{ left: -34px; }}
  .timeline-row:nth-child(even) .timeline-card::after {{ right: -34px; }}
  .card-header {{ font-weight: bold; margin-bottom: 5px; font-size: 0.85rem; }}
  .filename {{ font-size: 0.82rem; margin-bottom: 4px; }}
  .camera {{ font-size: 0.75rem; color: var(--muted); }}
  .badge {{ font-size: 0.7rem; background: rgba(245,158,11,0.1); color: #f59e0b; padding: 2px 5px; border-radius: 4px; display: inline-block; margin-top: 5px; }}
  .gap-marker {{ text-align: center; color: #ef4444; font-size: 0.8rem; margin: 20px 0; }}
  @media (max-width: 600px) {{ .timeline-container::before, .timeline-card::after {{ display: none; }} .timeline-row {{ justify-content: center !important; }} .timeline-card {{ width: 100%; }} }}
</style>
</head>
<body>
  <div class="camera-legend">{camera_legend}</div>
  <div class="timeline-container">{cards_html}</div>
  {_render_undated_section(undated)}
</body>
</html>'''