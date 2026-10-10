import os, re, uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.config import BASE_DIR, HF_API_KEY, HF_IMAGE_MODEL, DEMO_MODE

PANELS_DIR = BASE_DIR / "static" / "panels"
PANELS_DIR.mkdir(parents=True, exist_ok=True)

def _make_demo_image(title: str, number: int, destination: Path) -> None:
    """Create a local placeholder illustration so the full app can be tested without a paid AI service."""
    width, height = 900, 620
    image = Image.new("RGB", (width, height), (20 + number * 10, 35 + number * 8, 70 + number * 12))
    draw = ImageDraw.Draw(image)
    # Comic-style sun/moon, hills, and stars
    draw.ellipse((650, 55, 790, 195), fill=(255, 205, 90), outline=(255, 245, 190), width=6)
    for x, y in [(100, 90), (210, 145), (450, 80), (530, 180), (780, 280)]:
        draw.ellipse((x, y, x+9, y+9), fill="white")
    draw.polygon([(0, 430), (180, 260), (370, 440), (560, 280), (900, 440), (900, 620), (0, 620)], fill=(40, 115, 105))
    draw.polygon([(0, 510), (250, 390), (470, 530), (720, 400), (900, 500), (900, 620), (0, 620)], fill=(25, 75, 82))
    draw.rounded_rectangle((35, 35, 330, 100), radius=18, fill=(255, 255, 255), outline=(20, 20, 35), width=4)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except OSError:
        font = ImageFont.load_default()
    draw.text((55, 52), f"COMIC PANEL {number}", fill=(25, 25, 45), font=font)
    draw.text((45, 555), title[:48], fill="white", font=font, stroke_width=2, stroke_fill=(10, 10, 20))
    image.save(destination, "JPEG", quality=88)

def generate_image(image_prompt: str, title: str, panel_number: int) -> str:
    filename = f"panel_{panel_number}_{uuid.uuid4().hex[:8]}.jpg"
    destination = PANELS_DIR / filename
    if HF_API_KEY:
        try:
            from huggingface_hub import InferenceClient
            client = InferenceClient(model=HF_IMAGE_MODEL, token=HF_API_KEY)
            result = client.text_to_image(image_prompt)
            result.save(destination)
            return f"/static/panels/{filename}"
        except Exception as exc:
            if not DEMO_MODE:
                raise RuntimeError(f"Image generation failed: {exc}") from exc
    elif not DEMO_MODE:
        raise RuntimeError("HF_API_KEY is missing. Add it to your .env file.")
    _make_demo_image(title, panel_number, destination)
    return f"/static/panels/{filename}"
