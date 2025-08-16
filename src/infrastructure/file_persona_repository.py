"""File-based implementation of PersonaRepository for persistent storage."""
import json
import os
from typing import Dict, List, Optional
from entities.persona import Persona
from interactors.interfaces import PersonaRepository


class FilePersonaRepository(PersonaRepository):
    """File-based storage for personas - persistent across sessions."""
    
    def __init__(self, file_path: str = "personas.json"):
        self.file_path = file_path
    
    def _load_personas(self) -> Dict[str, dict]:
        """Load personas from file."""
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_personas(self, personas: Dict[str, dict]) -> None:
        """Save personas to file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(personas, f, indent=2)
        except IOError:
            pass  # Fail silently for now
    
    def _persona_to_dict(self, persona: Persona) -> dict:
        """Convert Persona to dictionary."""
        return {
            'id': persona.id,
            'name': persona.name,
            'niche': persona.niche,
            'target_audience': persona.target_audience,
            'localization': persona.localization,
            'tone': persona.tone,
            'industry': persona.industry,
            'experience_level': persona.experience_level,
            'content_themes': persona.content_themes,
            'engagement_style': persona.engagement_style,
            'personal_brand_keywords': persona.personal_brand_keywords,
            'posting_frequency': persona.posting_frequency,
            'description': persona.description
        }
    
    def _dict_to_persona(self, data: dict) -> Persona:
        """Convert dictionary to Persona."""
        return Persona(**data)
    
    async def save_persona(self, persona: Persona) -> None:
        """Save a persona to file storage."""
        personas = self._load_personas()
        personas[persona.id] = self._persona_to_dict(persona)
        self._save_personas(personas)
    
    async def get_persona_by_id(self, persona_id: str) -> Optional[Persona]:
        """Retrieve a persona by its ID."""
        personas = self._load_personas()
        if persona_id not in personas:
            return None
        return self._dict_to_persona(personas[persona_id])
    
    async def get_all_personas(self) -> List[Persona]:
        """Retrieve all personas."""
        personas = self._load_personas()
        return [self._dict_to_persona(data) for data in personas.values()]
    
    async def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona by ID. Returns True if deleted, False if not found."""
        personas = self._load_personas()
        if persona_id not in personas:
            return False
        
        del personas[persona_id]
        self._save_personas(personas)
        return True