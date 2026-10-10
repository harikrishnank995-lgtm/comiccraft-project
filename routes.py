from pathlib import Path
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.schemas import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf
from app.config import BASE_DIR, DEMO_MODE

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def create_comic(data: PromptRequest) -> dict:
    outline = generate_outline(data.prompt, data.character_name, data.setting, data.tone, data.art_style)
    story = generate_story(outline, data.character_name, data.tone)
    image_paths = []
    for panel in story:
        if data.generate_images:
            image_paths.append(generate_image(panel.get("image_prompt", data.prompt), panel["title"], panel["panel_number"]))
        else:
            image_paths.append("")
    layout = build_comic_layout(story, image_paths)
    title = f"{data.character_name}'s Comic"
    pdf_url = save_pdf(layout, title)
    return {"layout": layout, "pdf_url": pdf_url, "title": title, "demo_mode": DEMO_MODE}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"demo_mode": DEMO_MODE})

@router.post("/generate", response_class=HTMLResponse)
async def generate_form(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form("Alex"),
    setting: str = Form("enchanted forest"),
    tone: str = Form("adventurous"),
    art_style: str = Form("comic book"),
    generate_images: str = Form("yes"),
):
    try:
        data = PromptRequest(
            prompt=prompt, character_name=character_name, setting=setting,
            tone=tone, art_style=art_style, generate_images=(generate_images == "yes")
        )
        result = create_comic(data)
        return templates.TemplateResponse(request=request, name="comic_preview.html", context=result)
    except Exception as exc:
        return templates.TemplateResponse(
            request=request, name="index.html",
            context={"demo_mode": DEMO_MODE, "error": str(exc), "form": {
                "prompt": prompt, "character_name": character_name, "setting": setting,
                "tone": tone, "art_style": art_style
            }},
            status_code=500
        )

@router.post("/generate-comic/json")
async def generate_json(data: PromptRequest):
    try:
        result = create_comic(data)
        return {
            "title": result["title"], "layout": result["layout"],
            "pdf_url": result["pdf_url"], "demo_mode": result["demo_mode"]
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    try:
        image_url = generate_image(prompt, "Image Test", 0)
        return {"success": True, "image_url": image_url, "demo_mode": DEMO_MODE}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_url: str = ""):
    return templates.TemplateResponse(request=request, name="export_success.html", context={"pdf_url": pdf_url})

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    # Restrict downloads to generated PDFs in the exports directory.
    if Path(filename).name != filename or not filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid filename.")
    path = BASE_DIR / "static" / "exports" / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(path, media_type="application/pdf", filename=filename)

@router.get("/health")
async def health():
    return {"status": "ok", "app": "ComicCraft", "demo_mode": DEMO_MODE}
