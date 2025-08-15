"""In-memory implementation of PersonaRepository for development/testing."""
from typing import Dict, List, Optional
from entities.persona import Persona
from interactors.interfaces import PersonaRepository


class InMemoryPersonaRepository(PersonaRepository):
    """In-memory storage for personas - suitable for development and testing."""
    
    def __init__(self):
        self._personas: Dict[str, Persona] = {}
    
    async def save_persona(self, persona: Persona) -> None:
        """Save a persona to in-memory storage."""
        self._personas[persona.id] = persona
    
    async def get_persona_by_id(self, persona_id: str) -> Optional[Persona]:
        """Retrieve a persona by its ID."""
        return self._personas.get(persona_id)
    
    async def get_all_personas(self) -> List[Persona]:
        """Retrieve all personas."""
        return list(self._personas.values())
    
    async def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona by ID. Returns True if deleted, False if not found."""
        if persona_id in self._personas:
            del self._personas[persona_id]
            return True
        return False