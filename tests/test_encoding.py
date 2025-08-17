"""Test encoding for Brazilian Portuguese and other non-ASCII characters."""

import json
import os
import tempfile
import pytest
import sys
sys.path.append('src')
from entities.persona import Persona
from infrastructure.file_persona_repository import FilePersonaRepository
from infrastructure.file_post_repository import FilePostRepository
from entities.post import LinkedInPost
from datetime import datetime
import uuid
import asyncio


@pytest.mark.asyncio
async def test_persona_encoding_portuguese():
    """Test that Portuguese accents are properly saved and loaded."""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Create a persona with Portuguese accents
        persona = Persona(
            id="test-br",
            name="João Silva",
            niche="Tecnologia",
            target_audience="Desenvolvedores brasileiros",
            localization="Português (Brasil)",
            tone="amigável",
            industry="Engenharia de Software",
            experience_level="Sênior",
            content_themes=["programação", "educação"],
            engagement_style="histórias pessoais",
            personal_brand_keywords=["inovação", "tecnologia"],
            posting_frequency="diariamente",
            description="Especialista em desenvolvimento"
        )
        
        repo = FilePersonaRepository(tmp_path)
        await repo.save_persona(persona)
        
        # Verify the persona was saved correctly
        retrieved = await repo.get_persona_by_id("test-br")
        assert retrieved is not None
        assert retrieved.name == "João Silva"
        assert retrieved.localization == "Português (Brasil)"
        assert retrieved.experience_level == "Sênior"
        
        # Verify no escaped unicode in the JSON file
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "\\u00" not in content
            assert "João" in content
            assert "Português" in content
            assert "Sênior" in content
            
    finally:
        os.unlink(tmp_path)


@pytest.mark.asyncio
async def test_post_encoding_portuguese():
    """Test that Portuguese content in posts is properly saved and loaded."""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Create a post with Portuguese content
        post = LinkedInPost(
            id=str(uuid.uuid4()),
            persona_id="test-br",
            content="🚀 Programação não é apenas código.\n\nÉ criatividade e solução de problemas!\n\n#programação #tecnologia",
            image_prompt="Foto de um desenvolvedor trabalhando",
            market_analysis="Análise do mercado brasileiro de tecnologia",
            generation_prompt="Crie um post sobre programação para desenvolvedores brasileiros",
            created_at=datetime.now()
        )
        
        repo = FilePostRepository(tmp_path)
        await repo.save_post(post)
        
        # Verify the post was saved correctly
        retrieved = await repo.get_post_by_id(post.id)
        assert retrieved is not None
        assert "Programação não é" in retrieved.content
        assert "tecnologia" in retrieved.content
        assert "Análise" in retrieved.market_analysis
        
        # Verify no escaped unicode in the JSON file
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "\\u00" not in content
            assert "Programação não" in content
            assert "Análise" in content
            
    finally:
        os.unlink(tmp_path)


@pytest.mark.asyncio
async def test_various_accents_and_characters():
    """Test various international characters and accents."""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Create personas with various international characters
        personas = [
            Persona(
                id="french-test",
                name="François Müller",
                niche="Technologie",
                target_audience="Entrepreneurs français",
                localization="Français (France)",
                tone="professionnel",
                industry="Technologie",
                experience_level="Expérimenté",
                content_themes=["innovation", "développement"],
                engagement_style="récits personnels",
                personal_brand_keywords=["technologie", "créativité"],
                posting_frequency="hebdomadaire"
            ),
            Persona(
                id="spanish-test", 
                name="José María Pérez",
                niche="Tecnología",
                target_audience="Emprendedores españoles",
                localization="Español (España)",
                tone="profesional",
                industry="Tecnología",
                experience_level="Experto",
                content_themes=["innovación", "desarrollo"],
                engagement_style="narrativa personal",
                personal_brand_keywords=["tecnología", "innovación"],
                posting_frequency="semanal"
            ),
            Persona(
                id="german-test",
                name="Björn Müller",
                niche="Technologie",
                target_audience="Deutsche Unternehmer",
                localization="Deutsch (Deutschland)",
                tone="professionell",
                industry="Technologie", 
                experience_level="Erfahren",
                content_themes=["Innovation", "Entwicklung"],
                engagement_style="persönliche Geschichten",
                personal_brand_keywords=["Technologie", "Kreativität"],
                posting_frequency="wöchentlich"
            )
        ]
        
        repo = FilePersonaRepository(tmp_path)
        
        for persona in personas:
            await repo.save_persona(persona)
            retrieved = await repo.get_persona_by_id(persona.id)
            assert retrieved is not None
            assert retrieved.name == persona.name
            assert retrieved.localization == persona.localization
        
        # Verify no escaped unicode in the JSON file
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "\\u00" not in content
            # Check some specific characters are preserved
            assert "François" in content
            assert "José María" in content
            assert "Björn" in content
            assert "Expérimenté" in content
            assert "Español" in content
            assert "persönliche" in content
            
    finally:
        os.unlink(tmp_path)


def test_json_ensure_ascii_false():
    """Test that json.dump with ensure_ascii=False preserves non-ASCII characters."""
    test_data = {
        "portuguese": "Programação não é difícil",
        "french": "Français avec des accents",
        "german": "Björn Müller",
        "spanish": "José María Pérez"
    }
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Write with ensure_ascii=False
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # Read back and verify
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            loaded_data = json.loads(content)
        
        # Verify data integrity
        assert loaded_data == test_data
        
        # Verify no escaped sequences
        assert "\\u00" not in content
        assert "Programação não" in content
        assert "Français" in content
        assert "Björn" in content
        assert "José María" in content
        
    finally:
        os.unlink(tmp_path)