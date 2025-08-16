"""Tests for repository implementations."""
import pytest
from entities.persona import Persona
from entities.post import LinkedInPost
from infrastructure.in_memory_persona_repository import InMemoryPersonaRepository
from infrastructure.in_memory_post_repository import InMemoryPostRepository


class TestInMemoryPersonaRepository:
    """Test cases for InMemoryPersonaRepository."""
    
    @pytest.fixture
    def repository(self):
        """Fresh repository instance for each test."""
        return InMemoryPersonaRepository()
    
    @pytest.fixture
    def sample_persona(self):
        """Sample persona for testing."""
        return Persona(
            id="test-persona",
            name="Test Persona",
            niche="Technology",
            target_audience="Developers",
            localization="English (US)",
            tone="professional",
            industry="Tech",
            experience_level="senior",
            content_themes=["AI", "Development"],
            engagement_style="storytelling",
            personal_brand_keywords=["innovation", "leadership"],
            posting_frequency="weekly"
        )
    
    @pytest.mark.asyncio
    async def test_save_and_get_persona(self, repository, sample_persona):
        """Test saving and retrieving a persona."""
        # Save persona
        await repository.save_persona(sample_persona)
        
        # Retrieve persona
        result = await repository.get_persona_by_id("test-persona")
        
        assert result == sample_persona
        assert result.name == "Test Persona"
        assert result.niche == "Technology"
    
    @pytest.mark.asyncio
    async def test_get_persona_not_found(self, repository):
        """Test getting a persona that doesn't exist."""
        result = await repository.get_persona_by_id("non-existent")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_all_personas_empty(self, repository):
        """Test getting all personas when repository is empty."""
        result = await repository.get_all_personas()
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_all_personas_multiple(self, repository):
        """Test getting all personas with multiple personas."""
        persona1 = Persona(
            id="persona-1", name="Persona 1", niche="Tech", target_audience="Developers",
            localization="English (US)", tone="professional", industry="Tech", experience_level="senior",
            content_themes=["AI"], engagement_style="storytelling", 
            personal_brand_keywords=["innovation"], posting_frequency="weekly"
        )
        persona2 = Persona(
            id="persona-2", name="Persona 2", niche="Marketing", target_audience="Marketers",
            localization="English (US)", tone="casual", industry="Marketing", experience_level="mid",
            content_themes=["Growth"], engagement_style="data-driven", 
            personal_brand_keywords=["growth"], posting_frequency="daily"
        )
        
        await repository.save_persona(persona1)
        await repository.save_persona(persona2)
        
        result = await repository.get_all_personas()
        
        assert len(result) == 2
        assert persona1 in result
        assert persona2 in result
    
    @pytest.mark.asyncio
    async def test_update_persona(self, repository, sample_persona):
        """Test updating an existing persona."""
        # Save initial persona
        await repository.save_persona(sample_persona)
        
        # Update persona
        sample_persona.name = "Updated Name"
        await repository.save_persona(sample_persona)
        
        # Verify update
        result = await repository.get_persona_by_id("test-persona")
        assert result.name == "Updated Name"
    
    @pytest.mark.asyncio
    async def test_delete_persona_success(self, repository, sample_persona):
        """Test successful persona deletion."""
        # Save persona
        await repository.save_persona(sample_persona)
        
        # Delete persona
        result = await repository.delete_persona("test-persona")
        
        assert result is True
        
        # Verify deletion
        persona = await repository.get_persona_by_id("test-persona")
        assert persona is None
    
    @pytest.mark.asyncio
    async def test_delete_persona_not_found(self, repository):
        """Test deleting a persona that doesn't exist."""
        result = await repository.delete_persona("non-existent")
        assert result is False


class TestInMemoryPostRepository:
    """Test cases for InMemoryPostRepository."""
    
    @pytest.fixture
    def repository(self):
        """Fresh repository instance for each test."""
        return InMemoryPostRepository()
    
    @pytest.fixture
    def sample_post(self):
        """Sample post for testing."""
        return LinkedInPost(
            id="test-post",
            persona_id="test-persona",
            content="This is a test post content",
            image_prompt="Test image prompt"
        )
    
    @pytest.mark.asyncio
    async def test_save_and_get_post(self, repository, sample_post):
        """Test saving and retrieving a post."""
        # Save post
        await repository.save_post(sample_post)
        
        # Retrieve post
        result = await repository.get_post_by_id("test-post")
        
        assert result == sample_post
        assert result.content == "This is a test post content"
        assert result.persona_id == "test-persona"
    
    @pytest.mark.asyncio
    async def test_get_post_not_found(self, repository):
        """Test getting a post that doesn't exist."""
        result = await repository.get_post_by_id("non-existent")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_posts_by_persona(self, repository):
        """Test getting posts by persona."""
        post1 = LinkedInPost(id="post-1", persona_id="persona-1", content="Content 1")
        post2 = LinkedInPost(id="post-2", persona_id="persona-1", content="Content 2")
        post3 = LinkedInPost(id="post-3", persona_id="persona-2", content="Content 3")
        
        await repository.save_post(post1)
        await repository.save_post(post2)
        await repository.save_post(post3)
        
        # Get posts for persona-1
        result = await repository.get_posts_by_persona("persona-1")
        
        assert len(result) == 2
        assert post1 in result
        assert post2 in result
        assert post3 not in result
    
    @pytest.mark.asyncio
    async def test_get_posts_by_persona_empty(self, repository):
        """Test getting posts by persona when none exist."""
        result = await repository.get_posts_by_persona("non-existent")
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_all_posts_empty(self, repository):
        """Test getting all posts when repository is empty."""
        result = await repository.get_all_posts()
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_all_posts_multiple(self, repository):
        """Test getting all posts with multiple posts."""
        post1 = LinkedInPost(id="post-1", persona_id="persona-1", content="Content 1")
        post2 = LinkedInPost(id="post-2", persona_id="persona-2", content="Content 2")
        
        await repository.save_post(post1)
        await repository.save_post(post2)
        
        result = await repository.get_all_posts()
        
        assert len(result) == 2
        assert post1 in result
        assert post2 in result
    
    @pytest.mark.asyncio
    async def test_update_post(self, repository, sample_post):
        """Test updating an existing post."""
        # Save initial post
        await repository.save_post(sample_post)
        
        # Update post
        sample_post.content = "Updated content"
        await repository.save_post(sample_post)
        
        # Verify update
        result = await repository.get_post_by_id("test-post")
        assert result.content == "Updated content"