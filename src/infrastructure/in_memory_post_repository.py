"""In-memory implementation of PostRepository for development/testing."""
from typing import Dict, List, Optional
from entities.post import LinkedInPost
from interactors.interfaces import PostRepository


class InMemoryPostRepository(PostRepository):
    """In-memory storage for posts - suitable for development and testing."""
    
    def __init__(self):
        self._posts: Dict[str, LinkedInPost] = {}
    
    async def save_post(self, post: LinkedInPost) -> None:
        """Save a post to in-memory storage."""
        self._posts[post.id] = post
    
    async def get_post_by_id(self, post_id: str) -> Optional[LinkedInPost]:
        """Retrieve a post by its ID."""
        return self._posts.get(post_id)
    
    async def get_posts_by_persona(self, persona_id: str) -> List[LinkedInPost]:
        """Retrieve all posts for a specific persona."""
        return [post for post in self._posts.values() if post.persona_id == persona_id]
    
    async def get_all_posts(self) -> List[LinkedInPost]:
        """Retrieve all posts."""
        return list(self._posts.values())