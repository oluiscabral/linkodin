"""File-based implementation of PostRepository for persistent storage."""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from entities.post import LinkedInPost
from interactors.interfaces import PostRepository


class FilePostRepository(PostRepository):
    """File-based storage for posts - persistent across sessions."""
    
    def __init__(self, file_path: str = "posts.json"):
        self.file_path = file_path
    
    def _load_posts(self) -> Dict[str, dict]:
        """Load posts from file."""
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_posts(self, posts: Dict[str, dict]) -> None:
        """Save posts to file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(posts, f, indent=2, default=str)
        except IOError:
            pass  # Fail silently for now
    
    def _post_to_dict(self, post: LinkedInPost) -> dict:
        """Convert LinkedInPost to dictionary."""
        return {
            'id': post.id,
            'persona_id': post.persona_id,
            'content': post.content,
            'image_prompt': post.image_prompt,
            'image_url': post.image_url,
            'hashtags': post.hashtags,
            'created_at': post.created_at.isoformat() if post.created_at else None,
            'market_analysis': post.market_analysis,
            'generation_prompt': post.generation_prompt
        }
    
    def _dict_to_post(self, data: dict) -> LinkedInPost:
        """Convert dictionary to LinkedInPost."""
        if data['created_at']:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return LinkedInPost(**data)
    
    async def save_post(self, post: LinkedInPost) -> None:
        """Save a post to file storage."""
        posts = self._load_posts()
        posts[post.id] = self._post_to_dict(post)
        self._save_posts(posts)
    
    async def get_post_by_id(self, post_id: str) -> Optional[LinkedInPost]:
        """Retrieve a post by its ID."""
        posts = self._load_posts()
        if post_id not in posts:
            return None
        return self._dict_to_post(posts[post_id])
    
    async def get_posts_by_persona(self, persona_id: str) -> List[LinkedInPost]:
        """Retrieve all posts for a specific persona."""
        posts = self._load_posts()
        return [
            self._dict_to_post(data) 
            for data in posts.values() 
            if data['persona_id'] == persona_id
        ]
    
    async def get_all_posts(self) -> List[LinkedInPost]:
        """Retrieve all posts."""
        posts = self._load_posts()
        return [self._dict_to_post(data) for data in posts.values()]