"""Persona entity representing a LinkedIn persona configuration."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Persona:
    """Represents a LinkedIn persona with detailed settings for AI post generation."""
    
    id: str
    name: str
    niche: str
    target_audience: str
    localization: str  # Language and regional localization (e.g., "English (US)", "Spanish (Mexico)", "French (Paris)")
    tone: str  # professional, casual, inspirational, etc.
    industry: str
    experience_level: str  # entry, mid, senior, executive
    content_themes: List[str]  # topics they usually post about
    engagement_style: str  # storytelling, data-driven, question-based, etc.
    personal_brand_keywords: List[str]
    posting_frequency: str  # daily, weekly, etc.
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validate persona data after initialization."""
        if not self.id:
            raise ValueError("Persona ID cannot be empty")
        if not self.name:
            raise ValueError("Persona name cannot be empty")
        if not self.niche:
            raise ValueError("Persona niche cannot be empty")
        if not self.target_audience:
            raise ValueError("Target audience cannot be empty")
        if not self.localization:
            raise ValueError("Localization cannot be empty")
