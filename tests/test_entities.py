"""Tests for entity classes."""
import pytest
from datetime import datetime
from entities.persona import Persona
from entities.post import LinkedInPost, PostGenerationRequest


class TestPersona:
    """Test cases for Persona entity."""
    
    def test_persona_creation_valid(self):
        """Test creating a valid persona."""
        persona = Persona(
            id="test-id",
            name="Test Persona",
            niche="Technology",
            target_audience="Developers",
            language="English",
            tone="professional",
            industry="Tech",
            experience_level="senior",
            content_themes=["AI", "Development"],
            engagement_style="storytelling",
            personal_brand_keywords=["innovation", "leadership"],
            posting_frequency="weekly"
        )
        
        assert persona.id == "test-id"
        assert persona.name == "Test Persona"
        assert persona.niche == "Technology"
        assert len(persona.content_themes) == 2
        assert len(persona.personal_brand_keywords) == 2
    
    def test_persona_creation_empty_id(self):
        """Test that empty ID raises ValueError."""
        with pytest.raises(ValueError, match="Persona ID cannot be empty"):
            Persona(
                id="",
                name="Test Persona",
                niche="Technology",
                target_audience="Developers",
                language="English",
                tone="professional",
                industry="Tech",
                experience_level="senior",
                content_themes=["AI"],
                engagement_style="storytelling",
                personal_brand_keywords=["innovation"],
                posting_frequency="weekly"
            )
    
    def test_persona_creation_empty_name(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Persona name cannot be empty"):
            Persona(
                id="test-id",
                name="",
                niche="Technology",
                target_audience="Developers",
                language="English",
                tone="professional",
                industry="Tech",
                experience_level="senior",
                content_themes=["AI"],
                engagement_style="storytelling",
                personal_brand_keywords=["innovation"],
                posting_frequency="weekly"
            )


class TestLinkedInPost:
    """Test cases for LinkedInPost entity."""
    
    def test_post_creation_valid(self):
        """Test creating a valid post."""
        post = LinkedInPost(
            id="post-123",
            persona_id="persona-123",
            content="This is a test post"
        )
        
        assert post.id == "post-123"
        assert post.persona_id == "persona-123"
        assert post.content == "This is a test post"
        assert post.created_at is not None
        assert isinstance(post.created_at, datetime)
    
    def test_post_creation_with_custom_datetime(self):
        """Test creating post with custom datetime."""
        custom_time = datetime(2024, 1, 1, 12, 0, 0)
        post = LinkedInPost(
            id="post-123",
            persona_id="persona-123",
            content="Test content",
            created_at=custom_time
        )
        
        assert post.created_at == custom_time
    
    def test_post_creation_empty_id(self):
        """Test that empty ID raises ValueError."""
        with pytest.raises(ValueError, match="Post ID cannot be empty"):
            LinkedInPost(
                id="",
                persona_id="persona-123",
                content="Test content"
            )
    
    def test_post_creation_empty_persona_id(self):
        """Test that empty persona ID raises ValueError."""
        with pytest.raises(ValueError, match="Persona ID cannot be empty"):
            LinkedInPost(
                id="post-123",
                persona_id="",
                content="Test content"
            )
    
    def test_post_creation_empty_content(self):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="Post content cannot be empty"):
            LinkedInPost(
                id="post-123",
                persona_id="persona-123",
                content=""
            )


class TestPostGenerationRequest:
    """Test cases for PostGenerationRequest entity."""
    
    def test_request_creation_valid(self):
        """Test creating a valid request."""
        request = PostGenerationRequest(
            persona_id="persona-123",
            topic_hint="AI trends",
            additional_context="Focus on business impact"
        )
        
        assert request.persona_id == "persona-123"
        assert request.topic_hint == "AI trends"
        assert request.additional_context == "Focus on business impact"
    
    def test_request_creation_minimal(self):
        """Test creating request with minimal data."""
        request = PostGenerationRequest(persona_id="persona-123")
        
        assert request.persona_id == "persona-123"
        assert request.topic_hint is None
        assert request.additional_context is None
    
    def test_request_creation_empty_persona_id(self):
        """Test that empty persona ID raises ValueError."""
        with pytest.raises(ValueError, match="Persona ID is required"):
            PostGenerationRequest(persona_id="")