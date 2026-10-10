from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from PIL import Image
from app.config import BASE_DIR

EXPORTS_DIR = BASE_DIR / "static" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def save_pdf(layout: list[dict], story_title: str = "ComicCraft Story") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c.lower() if c.isalnum() else "_" for c in story_title).strip("_")[:32] or "comic"
    filename = f"{safe_title}_{timestamp}.pdf"
    output = EXPORTS_DIR / filename
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        title = str(panel.get("title", "Comic Panel")).encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 10, f"Panel {panel.get('panel_number', '')}: {title}")
        image_url = panel.get("image_url", "")
        image_path = BASE_DIR / image_url.lstrip("/") if image_url.startswith("/") else Path(image_url)
        if image_path.exists():
            try:
                with Image.open(image_path) as img:
                    iw, ih = img.size
                max_w, max_h = 180, 105
                scale = min(max_w / iw, max_h / ih)
                w, h = iw * scale, ih * scale
                x = (210 - w) / 2
                pdf.image(str(image_path), x=x, w=w, h=h)
                pdf.ln(4)
            except Exception:
                pdf.ln(4)
        for heading, key in [("Scene", "scene_description"), ("Caption", "caption"), ("Narration", "narration"), ("Dialogue", "dialogue")]:
            value = str(panel.get(key, "")).encode("latin-1", "replace").decode("latin-1")
            if value:
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 7, heading, new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 6, value)
                pdf.ln(1)
    pdf.output(str(output))
    return f"/static/exports/{filename}"
