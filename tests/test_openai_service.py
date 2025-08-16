"""Tests for OpenAI service temperature parameter handling."""
import pytest
from unittest.mock import AsyncMock, Mock, patch
from entities.persona import Persona
from infrastructure.openai_service import OpenAIService


class TestOpenAIService:
    """Test cases for OpenAI service."""
    
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
    
    def test_gpt5_temperature_detection(self):
        """Test that GPT-5 models are detected as not supporting custom temperature."""
        service = OpenAIService(api_key="test-key", model="gpt-5")
        assert not service._supports_custom_temperature
        
        service = OpenAIService(api_key="test-key", model="gpt-5-turbo")
        assert not service._supports_custom_temperature
    
    def test_gpt4_temperature_detection(self):
        """Test that GPT-4 models are detected as supporting custom temperature."""
        service = OpenAIService(api_key="test-key", model="gpt-4")
        assert service._supports_custom_temperature
        
        service = OpenAIService(api_key="test-key", model="gpt-4-turbo")
        assert service._supports_custom_temperature
    
    @pytest.mark.asyncio
    async def test_gpt5_market_analysis_without_temperature(self, sample_persona):
        """Test that GPT-5 market analysis requests don't include temperature."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "MARKET ANALYSIS: Test analysis\n\nGENERATION PROMPT: Test prompt"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            service = OpenAIService(api_key="test-key", model="gpt-5")
            
            await service.generate_market_analysis_and_prompt(sample_persona, "test topic", None)
            
            # Verify the API call was made without temperature parameter
            call_args = mock_client.chat.completions.create.call_args
            assert 'temperature' not in call_args[1]  # temperature should not be in kwargs
            assert call_args[1]['model'] == 'gpt-5'
    
    @pytest.mark.asyncio
    async def test_gpt4_market_analysis_with_temperature(self, sample_persona):
        """Test that GPT-4 market analysis requests include temperature."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "MARKET ANALYSIS: Test analysis\n\nGENERATION PROMPT: Test prompt"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            service = OpenAIService(api_key="test-key", model="gpt-4")
            
            await service.generate_market_analysis_and_prompt(sample_persona, "test topic", None)
            
            # Verify the API call was made with temperature parameter
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['temperature'] == 0.8
            assert call_args[1]['model'] == 'gpt-4'
    
    @pytest.mark.asyncio
    async def test_gpt5_post_content_without_temperature(self, sample_persona):
        """Test that GPT-5 post content requests don't include temperature."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Test post content"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            service = OpenAIService(api_key="test-key", model="gpt-5")
            
            await service.generate_post_content("test prompt", sample_persona)
            
            # Verify the API call was made without temperature parameter
            call_args = mock_client.chat.completions.create.call_args
            assert 'temperature' not in call_args[1]  # temperature should not be in kwargs
            assert call_args[1]['model'] == 'gpt-5'
    
    @pytest.mark.asyncio
    async def test_gpt4_post_content_with_temperature(self, sample_persona):
        """Test that GPT-4 post content requests include temperature."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Test post content"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            service = OpenAIService(api_key="test-key", model="gpt-4")
            
            await service.generate_post_content("test prompt", sample_persona)
            
            # Verify the API call was made with temperature parameter
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['temperature'] == 0.9
            assert call_args[1]['model'] == 'gpt-4'
    
    @pytest.mark.asyncio
    async def test_gpt5_image_prompt_without_temperature(self, sample_persona):
        """Test that GPT-5 image prompt requests don't include temperature."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Test image prompt"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            service = OpenAIService(api_key="test-key", model="gpt-5")
            
            await service.generate_image_prompt("test content", "test analysis", sample_persona)
            
            # Verify the API call was made without temperature parameter
            call_args = mock_client.chat.completions.create.call_args
            assert 'temperature' not in call_args[1]  # temperature should not be in kwargs
            assert call_args[1]['model'] == 'gpt-5'
    
    @pytest.mark.asyncio
    async def test_gpt4_image_prompt_with_temperature(self, sample_persona):
        """Test that GPT-4 image prompt requests include temperature."""
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Test image prompt"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            service = OpenAIService(api_key="test-key", model="gpt-4")
            
            await service.generate_image_prompt("test content", "test analysis", sample_persona)
            
            # Verify the API call was made with temperature parameter
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['model'] == 'gpt-4'
    
    def test_model_from_environment_variable(self):
        """Test that model can be set via environment variable."""
        with patch.dict('os.environ', {'OPENAI_MODEL': 'gpt-4-turbo'}):
            service = OpenAIService(api_key="test-key")
            assert service.model == 'gpt-4-turbo'
            assert service._supports_custom_temperature
    
    def test_default_model_is_gpt5(self):
        """Test that default model is GPT-5."""
        service = OpenAIService(api_key="test-key")
        assert service.model == 'gpt-5'
        assert not service._supports_custom_temperature