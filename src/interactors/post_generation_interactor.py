"""Post generation use cases."""
import uuid
from typing import Optional, List
from entities.persona import Persona
from entities.post import LinkedInPost, PostGenerationRequest
from interactors.interfaces import PersonaRepository, PostRepository, AIService


class PostGenerationInteractor:
    """Business logic for LinkedIn post generation using AI agents."""
    
    def __init__(
        self, 
        persona_repository: PersonaRepository, 
        post_repository: PostRepository,
        ai_service: AIService
    ):
        self._persona_repository = persona_repository
        self._post_repository = post_repository
        self._ai_service = ai_service
    
    async def generate_post(self, request: PostGenerationRequest) -> LinkedInPost:
        """
        Generate a LinkedIn post using the three-agent AI system.
        
        1. First agent: Market analysis and prompt generation
        2. Second agent: Post content generation
        3. Third agent: Image prompt generation
        """
        # Get the persona
        persona = await self._persona_repository.get_persona_by_id(request.persona_id)
        if not persona:
            raise ValueError(f"Persona with ID '{request.persona_id}' not found")
        
        # Step 1: First agent - Market analysis and prompt generation
        market_analysis, generation_prompt = await self._ai_service.generate_market_analysis_and_prompt(
            persona, 
            request.topic_hint, 
            request.additional_context
        )
        
        # Step 2: Second agent - Generate post content
        post_content = await self._ai_service.generate_post_content(
            generation_prompt, 
            persona
        )
        
        # Step 3: Third agent - Generate image prompt
        image_prompt = await self._ai_service.generate_image_prompt(
            post_content, 
            market_analysis, 
            persona
        )
        
        # Create the post entity
        post = LinkedInPost(
            id=str(uuid.uuid4()),
            persona_id=request.persona_id,
            content=post_content,
            image_prompt=image_prompt,
            market_analysis=market_analysis,
            generation_prompt=generation_prompt
        )
        
        # Save the post
        await self._post_repository.save_post(post)
        
        return post
    
    async def get_post(self, post_id: str) -> Optional[LinkedInPost]:
        """Get a post by ID."""
        return await self._post_repository.get_post_by_id(post_id)
    
    async def get_posts_by_persona(self, persona_id: str) -> List[LinkedInPost]:
        """Get all posts for a specific persona."""
        return await self._post_repository.get_posts_by_persona(persona_id)
    
    async def get_all_posts(self) -> List[LinkedInPost]:
        """Get all posts."""
        return await self._post_repository.get_all_posts()