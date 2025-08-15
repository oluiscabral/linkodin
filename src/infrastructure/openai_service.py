"""OpenAI GPT-5 implementation of AIService."""
import os
from typing import Optional
import openai
from entities.persona import Persona
from interactors.interfaces import AIService


class OpenAIService(AIService):
    """OpenAI GPT implementation for AI-powered post generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize OpenAI service with API key and model."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        self._has_real_key = bool(self.api_key)
    
    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if self.client is None:
            if not self._has_real_key:
                raise ValueError("OpenAI API key is required for post generation. Please set OPENAI_API_KEY environment variable.")
            self.client = openai.OpenAI(api_key=self.api_key)
        return self.client
    
    async def generate_market_analysis_and_prompt(
        self, 
        persona: Persona, 
        topic_hint: Optional[str], 
        additional_context: Optional[str]
    ) -> tuple[str, str]:
        """
        First agent: Generate deep market analysis and crafted prompt for viral LinkedIn posts.
        """
        system_prompt = """You are a LinkedIn marketing genius and viral content strategist. Your expertise lies in understanding what makes LinkedIn posts go viral and generate massive engagement.

Your task is to:
1. Conduct a deep current market analysis for the given persona's niche
2. Craft the perfect prompt that will generate viral LinkedIn posts

Focus on:
- Latest LinkedIn algorithm preferences and trends
- What drives engagement, discussions, debates, comments, and shares
- Storytelling techniques, psychological triggers, and marketing psychology
- Current market dynamics in the persona's niche
- Authenticity markers that avoid AI detection
- Viral content patterns and structures

Be creative and think outside the box. The prompt you create should consistently generate viral posts."""

        user_content = f"""
Persona Details:
- Name: {persona.name}
- Niche: {persona.niche}
- Target Audience: {persona.target_audience}
- Language: {persona.language}
- Tone: {persona.tone}
- Industry: {persona.industry}
- Experience Level: {persona.experience_level}
- Content Themes: {', '.join(persona.content_themes)}
- Engagement Style: {persona.engagement_style}
- Brand Keywords: {', '.join(persona.personal_brand_keywords)}
- Posting Frequency: {persona.posting_frequency}
"""

        if topic_hint:
            user_content += f"\nTopic Hint: {topic_hint}"
        
        if additional_context:
            user_content += f"\nAdditional Context: {additional_context}"

        user_content += """

Please provide:
1. MARKET ANALYSIS: Deep analysis of current market trends, LinkedIn algorithm preferences, and what makes posts viral in this niche
2. GENERATION PROMPT: A detailed, strategic prompt that will consistently generate viral LinkedIn posts for this persona"""

        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.8
        )
        
        content = response.choices[0].message.content
        
        # Parse the response to extract market analysis and generation prompt
        if "GENERATION PROMPT:" in content:
            parts = content.split("GENERATION PROMPT:")
            market_analysis = parts[0].replace("MARKET ANALYSIS:", "").strip()
            generation_prompt = parts[1].strip()
        else:
            # Fallback if the format is different
            market_analysis = content[:len(content)//2]
            generation_prompt = content[len(content)//2:]
        
        return market_analysis, generation_prompt
    
    async def generate_post_content(self, generation_prompt: str, persona: Persona) -> str:
        """
        Second agent: Generate viral LinkedIn post content using the first agent's prompt.
        """
        system_prompt = """You are an elite LinkedIn content creator who writes viral posts that generate massive engagement. You create authentic, attention-grabbing content that the LinkedIn algorithm loves and promotes widely.

Your posts should:
- Hook readers from the first line
- Use proven viral content structures
- Include psychological triggers for engagement
- Feel completely authentic and human-written
- Generate discussions, debates, comments, and shares
- Match the persona's authentic voice perfectly
- Use the latest engagement techniques and trends

Never mention AI, automation, or give any hint that this is AI-generated content."""

        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": generation_prompt}
            ],
            temperature=0.9
        )
        
        return response.choices[0].message.content.strip()
    
    async def generate_image_prompt(
        self, 
        post_content: str, 
        market_analysis: str, 
        persona: Persona
    ) -> str:
        """
        Third agent: Generate attention-grabbing image prompt for the post.
        """
        system_prompt = """You are a visual content strategist who creates compelling image prompts for LinkedIn posts. Your image prompts should generate visuals that:

- Grab attention in the LinkedIn feed
- Complement and enhance the post content
- Match the persona's brand and niche
- Follow current visual trends on LinkedIn
- Are professional yet engaging
- Support the post's viral potential

Create a detailed image generation prompt that will produce a high-quality, attention-grabbing visual."""

        user_content = f"""
Post Content:
{post_content}

Market Analysis Context:
{market_analysis}

Persona:
- Niche: {persona.niche}
- Industry: {persona.industry}
- Brand Keywords: {', '.join(persona.personal_brand_keywords)}
- Engagement Style: {persona.engagement_style}

Generate a detailed image prompt that will create the perfect visual companion for this LinkedIn post."""

        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()