from pydantic import BaseModel, Field, field_validator

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=1000)
    character_name: str = Field(default="Alex", min_length=1, max_length=60)
    setting: str = Field(default="enchanted forest", min_length=1, max_length=120)
    tone: str = Field(default="adventurous", max_length=50)
    art_style: str = Field(default="comic book", max_length=50)
    generate_images: bool = True

    @field_validator("prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def trim_text(cls, value: str) -> str:
        return value.strip()
