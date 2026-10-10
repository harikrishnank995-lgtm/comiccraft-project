# ComicCraft — AI Comic Story Creator

A beginner-friendly FastAPI web app that turns a story prompt into a five-panel comic, displays the panels, and exports them as a PDF.

## Features
- Responsive HTML/CSS interface rendered with Jinja2
- Five-panel outline and narration using the Gemini API
- Panel illustrations using Hugging Face Inference
- PDF export
- JSON API at `POST /generate-comic/json`
- Image test API at `POST /test-image`
- Demo mode so the app can be tested before API keys are configured

## Requirements
- Python 3.10 or newer (Python 3.11 is a good choice)
- VS Code
- Internet connection for installing packages and calling cloud AI services

## Setup on Windows (VS Code)

1. Extract the ZIP and open the **ComicCraft** folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Check Python:
   ```powershell
   py --version
   ```
   If `py` is not recognized, install Python from https://www.python.org/downloads/ and select **Add Python to PATH** during setup. Restart VS Code.
4. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt in VS Code and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
5. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. Create a local environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
   You can leave API keys blank for demo mode.
7. Start the server:
   ```powershell
   python -m uvicorn app.main:app --reload
   ```
8. Open:
   - Website: http://127.0.0.1:8000
   - API docs: http://127.0.0.1:8000/docs
   - Health check: http://127.0.0.1:8000/health

## Setup on macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

## Enable real AI generation

1. Create a Gemini API key in Google AI Studio: https://aistudio.google.com/app/apikey
2. Create a Hugging Face access token: https://huggingface.co/settings/tokens
3. Open `.env` and set:
   ```env
   GEMINI_API_KEY=your_real_gemini_key
   HF_API_KEY=your_real_huggingface_token
   DEMO_MODE=false
   ```
4. Stop the server with `Ctrl+C`, then restart it.

API/model availability, account access, rate limits, and provider costs can change. If a selected image model is unavailable for your account, change `HF_IMAGE_MODEL` in `.env` to a model supported by your Hugging Face Inference account. Never paste keys into source code or commit `.env` to GitHub.

## Test the app

1. Open the website and submit a story prompt of at least five characters.
2. In demo mode, it should create five sample panels and a PDF without API keys.
3. Click **Download your comic PDF**.
4. Open `/docs`, expand `POST /generate-comic/json`, and use **Try it out** with:
   ```json
   {
     "prompt": "A brave fox discovers a hidden library in an enchanted forest",
     "character_name": "Fenn",
     "setting": "enchanted forest",
     "tone": "adventurous",
     "art_style": "comic book",
     "generate_images": true
   }
   ```
5. Check `GET /health` returns `{"status":"ok", ...}`.

## Troubleshooting

- **`py` is not recognized**: install Python and select “Add Python to PATH”, then restart VS Code.
- **`pip` is not recognized**: use `python -m pip install -r requirements.txt`.
- **Module not found**: activate `.venv`, then run `python -m pip install -r requirements.txt` again.
- **Port already in use**: run `python -m uvicorn app.main:app --reload --port 8001` and open `http://127.0.0.1:8001`.
- **AI service errors**: temporarily set `DEMO_MODE=true`, restart the server, and verify the app locally. For real AI, check keys, model access, provider limits, and internet connection.
- **Do not upload `.env` to GitHub**. The included `.gitignore` excludes it.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes.py
│   └── services/
│       ├── __init__.py
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── exporters.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── panels/.gitkeep
│   └── exports/.gitkeep
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## API endpoints
- `GET /` — homepage
- `POST /generate` — form-based comic generation
- `POST /generate-comic/json` — JSON API
- `POST /test-image` — image generation test (multipart form field named `prompt`)
- `GET /download/{filename}` — download an existing generated PDF
- `GET /export-success` — export confirmation page
- `GET /health` — health check
