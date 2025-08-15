#!/usr/bin/env python3
"""Demo script to showcase LinkodIn functionality."""
import asyncio
import os
import sys

sys.path.insert(0, 'src')

from entities.persona import Persona
from entities.post import PostGenerationRequest
from interactors.persona_interactor import PersonaInteractor
from interactors.post_generation_interactor import PostGenerationInteractor
from infrastructure.in_memory_persona_repository import InMemoryPersonaRepository
from infrastructure.in_memory_post_repository import InMemoryPostRepository
from infrastructure.openai_service import OpenAIService


async def setup_demo_personas(persona_interactor):
    """Set up some demo personas."""
    personas = [
        Persona(
            id="tech-ceo",
            name="Tech CEO",
            niche="Technology Leadership",
            target_audience="Tech professionals, entrepreneurs, investors",
            language="English",
            tone="inspirational",
            industry="Technology",
            experience_level="executive",
            content_themes=["leadership", "innovation", "startup insights", "tech trends"],
            engagement_style="storytelling",
            personal_brand_keywords=["innovation", "leadership", "growth", "technology"],
            posting_frequency="weekly",
            description="Experienced tech CEO passionate about innovation and leadership"
        ),
        Persona(
            id="marketing-guru",
            name="Marketing Guru",
            niche="Digital Marketing",
            target_audience="Small business owners, marketing professionals, entrepreneurs",
            language="English",
            tone="enthusiastic",
            industry="Marketing",
            experience_level="senior",
            content_themes=["growth marketing", "social media", "content strategy", "digital transformation"],
            engagement_style="data-driven",
            personal_brand_keywords=["growth", "marketing", "results", "ROI"],
            posting_frequency="daily",
            description="Results-driven marketing expert helping businesses grow online"
        ),
        Persona(
            id="ai-researcher",
            name="AI Researcher",
            niche="Artificial Intelligence",
            target_audience="Tech professionals, researchers, AI enthusiasts",
            language="English",
            tone="professional",
            industry="Technology",
            experience_level="senior",
            content_themes=["machine learning", "AI ethics", "research insights", "future of AI"],
            engagement_style="educational",
            personal_brand_keywords=["AI", "machine learning", "research", "innovation"],
            posting_frequency="weekly",
            description="AI researcher sharing insights on the latest developments in artificial intelligence"
        )
    ]
    
    for persona in personas:
        await persona_interactor.create_persona(persona)
    
    return personas


async def demo_persona_management():
    """Demonstrate persona management functionality."""
    print("🎭 === PERSONA MANAGEMENT DEMO ===\n")
    
    # Initialize dependencies
    persona_repo = InMemoryPersonaRepository()
    persona_interactor = PersonaInteractor(persona_repo)
    
    # Set up demo personas
    print("📝 Creating demo personas...")
    personas = await setup_demo_personas(persona_interactor)
    print(f"✅ Created {len(personas)} personas\n")
    
    # List all personas
    print("📋 Available Personas:")
    all_personas = await persona_interactor.list_personas()
    for p in all_personas:
        print(f"  • {p.id}: {p.name} ({p.niche})")
    
    print()
    
    # Show detailed persona information
    print("👤 Detailed Persona Information:")
    for persona_id in ["tech-ceo", "marketing-guru"]:
        persona = await persona_interactor.get_persona(persona_id)
        print(f"\n--- {persona.name} ---")
        print(f"ID: {persona.id}")
        print(f"Niche: {persona.niche}")
        print(f"Target Audience: {persona.target_audience}")
        print(f"Content Themes: {', '.join(persona.content_themes)}")
        print(f"Brand Keywords: {', '.join(persona.personal_brand_keywords)}")
        print(f"Engagement Style: {persona.engagement_style}")
    
    return persona_interactor


async def demo_post_generation():
    """Demonstrate post generation (without OpenAI)."""
    print("\n\n🤖 === POST GENERATION DEMO ===\n")
    
    # Initialize dependencies
    persona_repo = InMemoryPersonaRepository()
    post_repo = InMemoryPostRepository()
    ai_service = OpenAIService()  # Will fail gracefully without API key
    
    persona_interactor = PersonaInteractor(persona_repo)
    post_interactor = PostGenerationInteractor(persona_repo, post_repo, ai_service)
    
    # Set up personas
    await setup_demo_personas(persona_interactor)
    
    # Try to generate a post (will show API key requirement)
    print("🔄 Attempting to generate post...")
    request = PostGenerationRequest(
        persona_id="tech-ceo",
        topic_hint="AI transformation in business",
        additional_context="Focus on practical benefits for companies"
    )
    
    try:
        post = await post_interactor.generate_post(request)
        print(f"✅ Post generated successfully!")
        print(f"Post ID: {post.id}")
        print(f"Content preview: {post.content[:100]}...")
    except ValueError as e:
        print(f"⚠️  {e}")
        print("💡 To generate posts, set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
    
    print()
    
    # Show existing posts (will be empty since generation failed)
    posts = await post_interactor.get_all_posts()
    print(f"📄 Total posts in storage: {len(posts)}")


async def demo_cli_usage():
    """Show CLI usage examples."""
    print("\n\n🖥️  === CLI USAGE EXAMPLES ===\n")
    
    print("🔧 Setup:")
    print("  pip install -e .")
    print("  export OPENAI_API_KEY='your-api-key-here'")
    print()
    
    print("👤 Persona Management:")
    print("  linkodin persona create --id 'tech-ceo' --name 'Tech CEO' \\")
    print("    --niche 'Technology Leadership' \\")
    print("    --target-audience 'Tech professionals, entrepreneurs' \\")
    print("    --industry 'Technology' \\")
    print("    --content-themes 'leadership,innovation' \\")
    print("    --brand-keywords 'innovation,leadership'")
    print()
    print("  linkodin persona list")
    print("  linkodin persona show tech-ceo")
    print()
    
    print("📝 Post Generation:")
    print("  linkodin post generate tech-ceo --topic 'AI trends'")
    print("  linkodin post list")
    print("  linkodin post show <post-id>")
    print()


async def main():
    """Run the complete demo."""
    print("🚀 LinkodIn - AI-Powered LinkedIn Post Generator")
    print("=" * 60)
    
    # Demo persona management
    await demo_persona_management()
    
    # Demo post generation
    await demo_post_generation()
    
    # Show CLI usage
    await demo_cli_usage()
    
    print("\n🎉 Demo completed!")
    print("\n📚 Key Features:")
    print("  ✅ Clean Architecture with separate entities, interactors, and infrastructure")
    print("  ✅ Three-agent AI system for viral LinkedIn post generation")
    print("  ✅ Comprehensive persona management")
    print("  ✅ CLI interface for easy interaction")
    print("  ✅ Extensible design with repository and service patterns")
    print("  ✅ Full test suite with 38 passing tests")
    
    print("\n🔗 Next Steps:")
    print("  1. Set up your OpenAI API key")
    print("  2. Create your personas using the CLI")
    print("  3. Generate viral LinkedIn posts!")


if __name__ == "__main__":
    asyncio.run(main())