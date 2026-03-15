from datetime import datetime


def create_report(images_data: list[dict], map_html: str, timeline_html: str, analysis: dict) -> str:
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    # עיבוד התובנות לבולטים עם איקונים
    insights_html = ""
    for insight in analysis.get("insights", []):
        icon = "🔍"
        if "מרחק" in insight: icon = "🚗"
        if "ממצא מיוחד" in insight: icon = "⚠️"
        elif "מכשיר" in insight: icon = "📱"
        if "ריכוז" in insight: icon = "📍"
        insights_html += f"<li><span class='insight-icon'>{icon}</span> {insight}</li>"

    # עיבוד המכשירים לתגים מעוצבים
    cameras_html = ""
    for cam in analysis.get("unique_cameras", []):
        cameras_html += f"<span class='badge'><i class='fas fa-mobile-alt'></i> {cam}</span> "

    html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Intelligence Report | Image Intel</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            :root {{
                --primary: #0ea5e9;
                --bg: #0f172a;
                --card-bg: #1e293b;
                --text: #f8fafc;
                --accent: #38bdf8;
            }}
            body {{ 
                font-family: 'Segoe UI', system-ui, sans-serif; 
                background: var(--bg); 
                color: var(--text); 
                margin: 0; padding: 20px; 
                line-height: 1.6;
            }}
            .container {{ max-width: 1100px; margin: 0 auto; }}

            /* Header */
            .header {{ 
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                padding: 40px; border-radius: 15px; text-align: center;
                border: 1px solid #334155; margin-bottom: 30px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            }}
            .header h1 {{ margin: 0; color: var(--primary); letter-spacing: 2px; text-transform: uppercase; }}
            .header p {{ color: #94a3b8; margin-top: 10px; }}

            /* Stats Grid */
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .stat-card {{ 
                background: var(--card-bg); padding: 25px; border-radius: 12px; 
                text-align: center; border: 1px solid #334155;
                transition: transform 0.3s ease;
            }}
            .stat-card:hover {{ transform: translateY(-5px); border-color: var(--primary); }}
            .stat-number {{ font-size: 2.5em; font-weight: 800; color: var(--primary); display: block; }}
            .stat-label {{ color: #94a3b8; font-size: 0.9em; text-transform: uppercase; }}

            /* Sections */
            .section {{ 
                background: var(--card-bg); padding: 30px; margin-bottom: 30px; 
                border-radius: 12px; border: 1px solid #334155; 
            }}
            h2 {{ color: var(--accent); border-bottom: 2px solid #334155; padding-bottom: 10px; margin-top: 0; display: flex; align-items: center; gap: 10px; }}

            /* Insights List */
            ul {{ list-style: none; padding: 0; }}
            li {{ 
                background: rgba(255,255,255,0.03); margin-bottom: 10px; 
                padding: 15px; border-radius: 8px; border-right: 4px solid var(--primary);
                display: flex; align-items: center;
            }}
            .insight-icon {{ margin-left: 15px; font-size: 1.2em; }}

            /* Badges */
            .badge {{ 
                background: #0369a1; color: white; padding: 8px 16px; 
                border-radius: 20px; margin: 5px; display: inline-flex; align-items: center; gap: 8px;
                font-size: 0.9em; font-weight: 600;
            }}

            /* Map Fix */
            .map-container {{ border-radius: 10px; overflow: hidden; border: 2px solid #334155; }}

            /* Timeline Overwrite - making it look integrated */
            .timeline-box {{ color: #cbd5e1; }}
            .timeline-box .image-entry {{ border-bottom: 1px solid #334155; padding: 15px; transition: background 0.2s; }}
            .timeline-box .image-entry:hover {{ background: rgba(255,255,255,0.02); }}

            footer {{ text-align: center; color: #64748b; margin-top: 50px; font-size: 0.9em; letter-spacing: 1px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-shield-halved"></i> דו"ח עיבוד תמונות</h1>
                <p><i class="far fa-clock"></i> תאריך הפקה: {now}</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-number">{analysis.get('total_images', 0)}</span>
                    <span class="stat-label">תמונות שנסרקו</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{analysis.get('images_with_gps', 0)}</span>
                    <span class="stat-label">מיקומים מזוהים</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{len(analysis.get('unique_cameras', []))}</span>
                    <span class="stat-label">מכשירים שונים</span>
                </div>
            </div>

            <div class="section">
                <h2><i class="fas fa-lightbulb"></i> תובנות</h2>
                <ul>{insights_html}</ul>
            </div>

            <div class="section">
                <h2><i class="fas fa-map-marked-alt"></i> פריסה גיאוגרפית</h2>
                <div class="map-container">{map_html}</div>
            </div>

            <div class="section">
                <h2><i class="fas fa-stream"></i> ציר זמן</h2>
                <div class="timeline-box">{timeline_html}</div>
            </div>

            <div class="section">
                <h2><i class="fas fa-microchip"></i> מכשירים </h2>
                {cameras_html}
            </div>

            <footer>
                IMAGE INTEL SYSTEM &copy; 2026 | KODCODE HACKATHON
            </footer>
        </div>
    </body>
    </html>
    """
    return html
if __name__ == "__main__":
    from extractor import extract_all
    images_data = extract_all("../images/ready")
    from map_view import create_map
    data_map = create_map(images_data)
    from timeline import create_timeline
    data_timeline =create_timeline(images_data)
    from analyzer import analyze
    data_analyzer = analyze(images_data)
    test =create_report(images_data,data_map,data_timeline,data_analyzer)
    with open("report_for_sent.html","w",encoding="utf-8") as f:
        f.write(test)