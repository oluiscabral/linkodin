"""Post entity representing a generated LinkedIn post."""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class LinkedInPost:
    """Represents a generated LinkedIn post with its content and metadata."""
    
    id: str
    persona_id: str
    content: str
    image_prompt: Optional[str] = None
    image_url: Optional[str] = None
    hashtags: Optional[str] = None
    created_at: Optional[datetime] = None
    market_analysis: Optional[str] = None  # First agent's analysis
    generation_prompt: Optional[str] = None  # First agent's generated prompt
    
    def __post_init__(self):
        """Validate post data after initialization."""
        if not self.id:
            raise ValueError("Post ID cannot be empty")
        if not self.persona_id:
            raise ValueError("Persona ID cannot be empty")
        if not self.content:
            raise ValueError("Post content cannot be empty")
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PostGenerationRequest:
    """Request data for generating a new LinkedIn post."""
    
    persona_id: str
    topic_hint: Optional[str] = None  # Optional topic guidance
    additional_context: Optional[str] = None  # Any additional context for generation
    
    def __post_init__(self):
        """Validate request data after initialization."""
        if not self.persona_id:
            raise ValueError("Persona ID is required for post generation")