"""Persona management use cases."""
from typing import List, Optional
from entities.persona import Persona
from interactors.interfaces import PersonaRepository


class PersonaInteractor:
    """Business logic for persona management."""
    
    def __init__(self, persona_repository: PersonaRepository):
        self._persona_repository = persona_repository
    
    async def create_persona(self, persona: Persona) -> None:
        """Create a new persona."""
        # Check if persona with same ID already exists
        existing = await self._persona_repository.get_persona_by_id(persona.id)
        if existing:
            raise ValueError(f"Persona with ID '{persona.id}' already exists")
        
        await self._persona_repository.save_persona(persona)
    
    async def update_persona(self, persona: Persona) -> None:
        """Update an existing persona."""
        existing = await self._persona_repository.get_persona_by_id(persona.id)
        if not existing:
            raise ValueError(f"Persona with ID '{persona.id}' not found")
        
        await self._persona_repository.save_persona(persona)
    
    async def get_persona(self, persona_id: str) -> Optional[Persona]:
        """Get a persona by ID."""
        return await self._persona_repository.get_persona_by_id(persona_id)
    
    async def list_personas(self) -> List[Persona]:
        """List all personas."""
        return await self._persona_repository.get_all_personas()
    
    async def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona by ID."""
        return await self._persona_repository.delete_persona(persona_id)