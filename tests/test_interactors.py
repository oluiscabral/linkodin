"""Tests for interactor classes."""
import pytest
from unittest.mock import AsyncMock, Mock
from entities.persona import Persona
from entities.post import LinkedInPost, PostGenerationRequest
from interactors.persona_interactor import PersonaInteractor
from interactors.post_generation_interactor import PostGenerationInteractor
from interactors.interfaces import PersonaRepository, PostRepository, AIService


class TestPersonaInteractor:
    """Test cases for PersonaInteractor."""
    
    @pytest.fixture
    def mock_repo(self):
        """Mock persona repository."""
        return AsyncMock(spec=PersonaRepository)
    
    @pytest.fixture
    def persona_interactor(self, mock_repo):
        """PersonaInteractor instance with mock repository."""
        return PersonaInteractor(mock_repo)
    
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
    async def test_create_persona_success(self, persona_interactor, mock_repo, sample_persona):
        """Test successful persona creation."""
        mock_repo.get_persona_by_id.return_value = None
        
        await persona_interactor.create_persona(sample_persona)
        
        mock_repo.get_persona_by_id.assert_called_once_with("test-persona")
        mock_repo.save_persona.assert_called_once_with(sample_persona)
    
    @pytest.mark.asyncio
    async def test_create_persona_already_exists(self, persona_interactor, mock_repo, sample_persona):
        """Test persona creation when persona already exists."""
        mock_repo.get_persona_by_id.return_value = sample_persona
        
        with pytest.raises(ValueError, match="Persona with ID 'test-persona' already exists"):
            await persona_interactor.create_persona(sample_persona)
        
        mock_repo.save_persona.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_persona_success(self, persona_interactor, mock_repo, sample_persona):
        """Test successful persona update."""
        mock_repo.get_persona_by_id.return_value = sample_persona
        
        await persona_interactor.update_persona(sample_persona)
        
        mock_repo.get_persona_by_id.assert_called_once_with("test-persona")
        mock_repo.save_persona.assert_called_once_with(sample_persona)
    
    @pytest.mark.asyncio
    async def test_update_persona_not_found(self, persona_interactor, mock_repo, sample_persona):
        """Test persona update when persona doesn't exist."""
        mock_repo.get_persona_by_id.return_value = None
        
        with pytest.raises(ValueError, match="Persona with ID 'test-persona' not found"):
            await persona_interactor.update_persona(sample_persona)
        
        mock_repo.save_persona.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_persona(self, persona_interactor, mock_repo, sample_persona):
        """Test getting a persona by ID."""
        mock_repo.get_persona_by_id.return_value = sample_persona
        
        result = await persona_interactor.get_persona("test-persona")
        
        assert result == sample_persona
        mock_repo.get_persona_by_id.assert_called_once_with("test-persona")
    
    @pytest.mark.asyncio
    async def test_list_personas(self, persona_interactor, mock_repo, sample_persona):
        """Test listing all personas."""
        personas = [sample_persona]
        mock_repo.get_all_personas.return_value = personas
        
        result = await persona_interactor.list_personas()
        
        assert result == personas
        mock_repo.get_all_personas.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_persona_success(self, persona_interactor, mock_repo):
        """Test successful persona deletion."""
        mock_repo.delete_persona.return_value = True
        
        result = await persona_interactor.delete_persona("test-persona")
        
        assert result is True
        mock_repo.delete_persona.assert_called_once_with("test-persona")
    
    @pytest.mark.asyncio
    async def test_delete_persona_not_found(self, persona_interactor, mock_repo):
        """Test persona deletion when persona doesn't exist."""
        mock_repo.delete_persona.return_value = False
        
        result = await persona_interactor.delete_persona("test-persona")
        
        assert result is False
        mock_repo.delete_persona.assert_called_once_with("test-persona")


class TestPostGenerationInteractor:
    """Test cases for PostGenerationInteractor."""
    
    @pytest.fixture
    def mock_persona_repo(self):
        """Mock persona repository."""
        return AsyncMock(spec=PersonaRepository)
    
    @pytest.fixture
    def mock_post_repo(self):
        """Mock post repository."""
        return AsyncMock(spec=PostRepository)
    
    @pytest.fixture
    def mock_ai_service(self):
        """Mock AI service."""
        return AsyncMock(spec=AIService)
    
    @pytest.fixture
    def post_interactor(self, mock_persona_repo, mock_post_repo, mock_ai_service):
        """PostGenerationInteractor instance with mock dependencies."""
        return PostGenerationInteractor(mock_persona_repo, mock_post_repo, mock_ai_service)
    
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
    
    @pytest.fixture
    def sample_request(self):
        """Sample post generation request."""
        return PostGenerationRequest(
            persona_id="test-persona",
            topic_hint="AI trends",
            additional_context="Focus on business impact"
        )
    
    @pytest.mark.asyncio
    async def test_generate_post_success(
        self, post_interactor, mock_persona_repo, mock_post_repo, 
        mock_ai_service, sample_persona, sample_request
    ):
        """Test successful post generation."""
        # Setup mocks
        mock_persona_repo.get_persona_by_id.return_value = sample_persona
        mock_ai_service.generate_market_analysis_and_prompt.return_value = (
            "Market analysis content", "Generation prompt content"
        )
        mock_ai_service.generate_post_content.return_value = "Generated post content"
        mock_ai_service.generate_image_prompt.return_value = "Image prompt content"
        
        # Execute
        result = await post_interactor.generate_post(sample_request)
        
        # Verify
        assert isinstance(result, LinkedInPost)
        assert result.persona_id == "test-persona"
        assert result.content == "Generated post content"
        assert result.image_prompt == "Image prompt content"
        assert result.market_analysis == "Market analysis content"
        assert result.generation_prompt == "Generation prompt content"
        
        # Verify method calls
        mock_persona_repo.get_persona_by_id.assert_called_once_with("test-persona")
        mock_ai_service.generate_market_analysis_and_prompt.assert_called_once_with(
            sample_persona, "AI trends", "Focus on business impact"
        )
        mock_ai_service.generate_post_content.assert_called_once_with(
            "Generation prompt content", sample_persona
        )
        mock_ai_service.generate_image_prompt.assert_called_once_with(
            "Generated post content", "Market analysis content", sample_persona
        )
        mock_post_repo.save_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_post_persona_not_found(
        self, post_interactor, mock_persona_repo, sample_request
    ):
        """Test post generation when persona doesn't exist."""
        mock_persona_repo.get_persona_by_id.return_value = None
        
        with pytest.raises(ValueError, match="Persona with ID 'test-persona' not found"):
            await post_interactor.generate_post(sample_request)
    
    @pytest.mark.asyncio
    async def test_get_post(self, post_interactor, mock_post_repo):
        """Test getting a post by ID."""
        sample_post = LinkedInPost(
            id="post-123",
            persona_id="persona-123",
            content="Test content"
        )
        mock_post_repo.get_post_by_id.return_value = sample_post
        
        result = await post_interactor.get_post("post-123")
        
        assert result == sample_post
        mock_post_repo.get_post_by_id.assert_called_once_with("post-123")
    
    @pytest.mark.asyncio
    async def test_get_posts_by_persona(self, post_interactor, mock_post_repo):
        """Test getting posts by persona."""
        posts = [
            LinkedInPost(id="post-1", persona_id="persona-123", content="Content 1"),
            LinkedInPost(id="post-2", persona_id="persona-123", content="Content 2")
        ]
        mock_post_repo.get_posts_by_persona.return_value = posts
        
        result = await post_interactor.get_posts_by_persona("persona-123")
        
        assert result == posts
        mock_post_repo.get_posts_by_persona.assert_called_once_with("persona-123")
    
    @pytest.mark.asyncio
    async def test_get_all_posts(self, post_interactor, mock_post_repo):
        """Test getting all posts."""
        posts = [
            LinkedInPost(id="post-1", persona_id="persona-1", content="Content 1"),
            LinkedInPost(id="post-2", persona_id="persona-2", content="Content 2")
        ]
        mock_post_repo.get_all_posts.return_value = posts
        
        result = await post_interactor.get_all_posts()
        
        assert result == posts
        mock_post_repo.get_all_posts.assert_called_once()