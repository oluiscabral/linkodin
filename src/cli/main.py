"""Main CLI entry point for LinkodIn."""
import asyncio
import os
from typing import Optional
import click
from dotenv import load_dotenv

from entities.persona import Persona
from entities.post import PostGenerationRequest
from interactors.persona_interactor import PersonaInteractor
from interactors.post_generation_interactor import PostGenerationInteractor
from infrastructure.file_persona_repository import FilePersonaRepository
from infrastructure.file_post_repository import FilePostRepository
from infrastructure.openai_service import OpenAIService
from infrastructure.mock_ai_service import MockAIService

# Load environment variables
load_dotenv()

# Global dependencies - shared across all commands
_dependencies = None

def get_dependencies():
    """Lazy initialization of shared dependencies."""
    global _dependencies
    
    if _dependencies is None:
        persona_repo = FilePersonaRepository()
        post_repo = FilePostRepository()
        ai_service = OpenAIService()
        persona_interactor = PersonaInteractor(persona_repo)
        post_interactor = PostGenerationInteractor(persona_repo, post_repo, ai_service)
        
        _dependencies = {
            'persona_interactor': persona_interactor,
            'post_interactor': post_interactor
        }
    
    return _dependencies['persona_interactor'], _dependencies['post_interactor']


@click.group()
def cli():
    """LinkodIn - AI-powered LinkedIn post generator."""
    pass


@cli.group()
def persona():
    """Persona management commands."""
    pass


@persona.command("create")
@click.option("--id", required=True, help="Unique persona identifier")
@click.option("--name", required=True, help="Persona name")
@click.option("--niche", required=True, help="Persona niche/expertise area")
@click.option("--target-audience", required=True, help="Target audience description")
@click.option("--localization", default="English (US)", help="Language and regional localization for posts")
@click.option("--tone", default="professional", help="Tone of voice")
@click.option("--industry", required=True, help="Industry/sector")
@click.option("--experience-level", default="senior", help="Experience level")
@click.option("--content-themes", required=True, help="Content themes (comma-separated)")
@click.option("--engagement-style", default="storytelling", help="Engagement style")
@click.option("--brand-keywords", required=True, help="Personal brand keywords (comma-separated)")
@click.option("--posting-frequency", default="weekly", help="Posting frequency")
@click.option("--description", help="Optional description")
def create_persona(
    id: str, name: str, niche: str, target_audience: str, localization: str,
    tone: str, industry: str, experience_level: str, content_themes: str,
    engagement_style: str, brand_keywords: str, posting_frequency: str,
    description: Optional[str]
):
    """Create a new persona."""
    async def _create():
        persona_int, _ = get_dependencies()
        
        persona = Persona(
            id=id,
            name=name,
            niche=niche,
            target_audience=target_audience,
            localization=localization,
            tone=tone,
            industry=industry,
            experience_level=experience_level,
            content_themes=[theme.strip() for theme in content_themes.split(",")],
            engagement_style=engagement_style,
            personal_brand_keywords=[kw.strip() for kw in brand_keywords.split(",")],
            posting_frequency=posting_frequency,
            description=description
        )
        
        try:
            await persona_int.create_persona(persona)
            click.echo(f"[+] Persona '{name}' created successfully!")
        except ValueError as e:
            click.echo(f"[!] Error: {e}", err=True)
    
    asyncio.run(_create())


@persona.command("list")
def list_personas():
    """List all personas."""
    async def _list():
        persona_int, _ = get_dependencies()
        
        personas = await persona_int.list_personas()
        if not personas:
            click.echo("No personas found.")
            return
        
        click.echo("\n[*] Available Personas:")
        for p in personas:
            click.echo(f"  - {p.id}: {p.name} ({p.niche})")
    
    asyncio.run(_list())


@persona.command("show")
@click.argument("persona_id")
def show_persona(persona_id: str):
    """Show detailed information about a persona."""
    async def _show():
        persona_int, _ = get_dependencies()
        
        persona = await persona_int.get_persona(persona_id)
        if not persona:
            click.echo(f"[!] Persona '{persona_id}' not found.", err=True)
            return
        
        click.echo(f"\n[*] Persona: {persona.name}")
        click.echo(f"ID: {persona.id}")
        click.echo(f"Niche: {persona.niche}")
        click.echo(f"Target Audience: {persona.target_audience}")
        click.echo(f"Localization: {persona.localization}")
        click.echo(f"Tone: {persona.tone}")
        click.echo(f"Industry: {persona.industry}")
        click.echo(f"Experience Level: {persona.experience_level}")
        click.echo(f"Content Themes: {', '.join(persona.content_themes)}")
        click.echo(f"Engagement Style: {persona.engagement_style}")
        click.echo(f"Brand Keywords: {', '.join(persona.personal_brand_keywords)}")
        click.echo(f"Posting Frequency: {persona.posting_frequency}")
        if persona.description:
            click.echo(f"Description: {persona.description}")
    
    asyncio.run(_show())


@persona.command("delete")
@click.argument("persona_id")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
def delete_persona(persona_id: str, yes: bool):
    """Delete a persona."""
    async def _delete():
        persona_int, _ = get_dependencies()
        
        if not yes:
            if not click.confirm(f"Are you sure you want to delete persona '{persona_id}'?"):
                click.echo("Delete cancelled.")
                return
        
        deleted = await persona_int.delete_persona(persona_id)
        if deleted:
            click.echo(f"[+] Persona '{persona_id}' deleted successfully!")
        else:
            click.echo(f"[!] Persona '{persona_id}' not found.", err=True)
    
    asyncio.run(_delete())


@cli.group()
def post():
    """Post generation and management commands."""
    pass


@post.command("generate")
@click.argument("persona_id")
@click.option("--topic", help="Optional topic hint for the post")
@click.option("--context", help="Additional context for generation")
@click.option("--mock", is_flag=True, help="Use mock AI service (no API key required)")
def generate_post(persona_id: str, topic: Optional[str], context: Optional[str], mock: bool):
    """Generate a new LinkedIn post for the specified persona."""
    async def _generate():
        # Check if using mock or real AI service
        if mock:
            # Use mock AI service
            persona_repo = FilePersonaRepository()
            post_repo = FilePostRepository()
            ai_service = MockAIService()
            persona_interactor = PersonaInteractor(persona_repo)
            post_interactor = PostGenerationInteractor(persona_repo, post_repo, ai_service)
        else:
            # Check if OpenAI API key is available
            if not os.getenv("OPENAI_API_KEY"):
                click.echo("[!] Error: OPENAI_API_KEY environment variable is not set.", err=True)
                click.echo("Please set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
                click.echo("Or use --mock flag to generate sample content: linkodin post generate persona-id --mock")
                return
            
            _, post_interactor = get_dependencies()
        
        request = PostGenerationRequest(
            persona_id=persona_id,
            topic_hint=topic,
            additional_context=context
        )
        
        try:
            if mock:
                click.echo("[AI] Generating post with Mock AI agents (demo mode)...")
            else:
                click.echo("[AI] Generating post with AI agents...")
            click.echo("[1] Market analysis and prompt crafting...")
            
            post = await post_interactor.generate_post(request)
            
            click.echo("[2] Post content generation...")
            click.echo("[3] Image prompt generation...")
            
            if mock:
                click.echo("\n[+] Demo post generated successfully!")
            else:
                click.echo("\n[+] Post generated successfully!")
            
            click.echo(f"Post ID: {post.id}")
            click.echo(f"\n[*] Content:\n{post.content}")
            
            if post.image_prompt:
                click.echo(f"\n[*] Image Prompt:\n{post.image_prompt}")
            
        except ValueError as e:
            click.echo(f"[!] Error: {e}", err=True)
        except Exception as e:
            click.echo(f"[!] Unexpected error: {e}", err=True)
    
    asyncio.run(_generate())


@post.command("list")
@click.option("--persona", help="Filter by persona ID")
def list_posts(persona: Optional[str]):
    """List generated posts."""
    async def _list():
        _, post_int = get_dependencies()
        
        if persona:
            posts = await post_int.get_posts_by_persona(persona)
            click.echo(f"\n[*] Posts for persona '{persona}':")
        else:
            posts = await post_int.get_all_posts()
            click.echo("\n[*] All Posts:")
        
        if not posts:
            click.echo("No posts found.")
            return
        
        for p in posts:
            click.echo(f"  - {p.id} (Persona: {p.persona_id}) - {p.created_at}")
    
    asyncio.run(_list())


@post.command("show")
@click.argument("post_id")
def show_post(post_id: str):
    """Show detailed information about a post."""
    async def _show():
        _, post_int = get_dependencies()
        
        post = await post_int.get_post(post_id)
        if not post:
            click.echo(f"[!] Post '{post_id}' not found.", err=True)
            return
        
        click.echo(f"\n[*] Post: {post.id}")
        click.echo(f"Persona ID: {post.persona_id}")
        click.echo(f"Created: {post.created_at}")
        click.echo(f"\nContent:\n{post.content}")
        
        if post.image_prompt:
            click.echo(f"\n[*] Image Prompt:\n{post.image_prompt}")
        
        if post.market_analysis:
            click.echo(f"\n[*] Market Analysis:\n{post.market_analysis}")
    
    asyncio.run(_show())


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()