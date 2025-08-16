"""Interfaces for data access and external services."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from entities.persona import Persona
from entities.post import LinkedInPost


class PersonaRepository(ABC):
    """Interface for persona data access."""
    
    @abstractmethod
    async def save_persona(self, persona: Persona) -> None:
        """Save a persona to storage."""
        pass
    
    @abstractmethod
    async def get_persona_by_id(self, persona_id: str) -> Optional[Persona]:
        """Retrieve a persona by its ID."""
        pass
    
    @abstractmethod
    async def get_all_personas(self) -> List[Persona]:
        """Retrieve all personas."""
        pass
    
    @abstractmethod
    async def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona by ID. Returns True if deleted, False if not found."""
        pass


class PostRepository(ABC):
    """Interface for post data access."""
    
    @abstractmethod
    async def save_post(self, post: LinkedInPost) -> None:
        """Save a post to storage."""
        pass
    
    @abstractmethod
    async def get_post_by_id(self, post_id: str) -> Optional[LinkedInPost]:
        """Retrieve a post by its ID."""
        pass
    
    @abstractmethod
    async def get_posts_by_persona(self, persona_id: str) -> List[LinkedInPost]:
        """Retrieve all posts for a specific persona."""
        pass
    
    @abstractmethod
    async def get_all_posts(self) -> List[LinkedInPost]:
        """Retrieve all posts."""
        pass


class AIService(ABC):
    """Interface for AI service interactions."""
    
    @abstractmethod
    async def generate_market_analysis_and_prompt(self, persona: Persona, topic_hint: Optional[str], additional_context: Optional[str]) -> Tuple[str, str]:
        """
        First agent: Generate market analysis and crafted prompt.
        Returns: (market_analysis, generation_prompt)
        """
        pass
    
    @abstractmethod
    async def generate_post_content(self, generation_prompt: str, persona: Persona) -> str:
        """
        Second agent: Generate LinkedIn post content based on the first agent's prompt.
        Returns: post_content
        """
        pass
    
    @abstractmethod
    async def generate_image_prompt(self, post_content: str, market_analysis: str, persona: Persona) -> str:
        """
        Third agent: Generate image prompt based on post content and analysis.
        Returns: image_prompt
        """
        pass