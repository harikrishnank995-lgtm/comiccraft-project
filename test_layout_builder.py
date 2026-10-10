from app.services.layout_builder import build_comic_layout

def test_layout_builder_matches_panels_and_images():
    source = [
        {"title": "Start", "scene_description": "A beginning", "caption": "Morning", "narration": "Go", "dialogue": "Hello"},
        {"title": "Finish", "scene_description": "The end", "caption": "Evening", "narration": "Done", "dialogue": "Bye"},
    ]
    layout = build_comic_layout(source, ["/static/panels/a.jpg", "/static/panels/b.jpg"])
    assert len(layout) == 2
    assert layout[0]["panel_number"] == 1
    assert layout[1]["image_url"] == "/static/panels/b.jpg"
