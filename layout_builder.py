def build_comic_layout(story_panels: list[dict], image_paths: list[str]) -> list[dict]:
    layout = []
    for index, panel in enumerate(story_panels):
        layout.append({
            "panel_number": index + 1,
            "title": str(panel.get("title", f"Panel {index+1}")),
            "image_url": image_paths[index] if index < len(image_paths) else "",
            "scene_description": str(panel.get("scene_description", "")),
            "caption": str(panel.get("caption", "")),
            "narration": str(panel.get("narration", "")),
            "dialogue": str(panel.get("dialogue", "")),
            "image_prompt": str(panel.get("image_prompt", "")),
        })
    return layout
