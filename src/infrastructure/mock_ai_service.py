"""Mock AI service for testing and demo purposes."""
from typing import Optional, Tuple
from entities.persona import Persona
from interactors.interfaces import AIService


class MockAIService(AIService):
    """Mock AI service that generates sample content without calling external APIs."""
    
    async def generate_market_analysis_and_prompt(
        self, 
        persona: Persona, 
        topic_hint: Optional[str], 
        additional_context: Optional[str]
    ) -> Tuple[str, str]:
        """Generate mock market analysis and prompt."""
        topic = topic_hint or "industry insights"
        
        market_analysis = f"""
MOCK MARKET ANALYSIS for {persona.name}:

Current LinkedIn Algorithm Preferences:
• {persona.engagement_style} content performs 47% better in {persona.niche}
• Posts with {persona.tone} tone get 3x more engagement from {persona.target_audience}
• {persona.industry} professionals are 2.1x more likely to engage with content about {topic}
• Optimal posting time: Based on {persona.posting_frequency} schedule
• Key trending hashtags in {persona.niche}: #{persona.personal_brand_keywords[0].replace(' ', '')}

Viral Content Triggers:
• Personal stories with business lessons (68% higher engagement)
• Contrarian viewpoints that spark healthy debate
• Data-driven insights with actionable takeaways
• Behind-the-scenes entrepreneurial moments

Current Market Sentiment:
The {persona.industry} space is hungry for authentic, {persona.tone} content that combines personal experience with practical insights.
        """.strip()
        
        generation_prompt = f"""
You are {persona.name}, a respected voice in {persona.niche}. Your audience consists of {persona.target_audience}.

Create a LinkedIn post about "{topic}" that:
- Reflects your {persona.tone} tone and {persona.engagement_style} style
- Incorporates themes from: {', '.join(persona.content_themes)}
- Uses your brand keywords naturally: {', '.join(persona.personal_brand_keywords)}
- Targets professionals in {persona.industry}
- Written for {persona.localization} audience

The post should:
1. Start with a compelling hook that stops scrolling
2. Tell a personal story or share a controversial insight
3. Include 2-3 actionable takeaways
4. End with a question that drives comments
5. Be 150-200 words for optimal engagement
6. Feel completely authentic and human-written

Additional context: {additional_context or 'Focus on practical lessons that resonate with your audience'}

Write in first person as {persona.name}. Make it viral-worthy while staying true to your authentic voice.
        """.strip()
        
        return market_analysis, generation_prompt
    
    async def generate_post_content(self, generation_prompt: str, persona: Persona) -> str:
        """Generate mock LinkedIn post content."""
        topic_words = ["innovation", "growth", "lessons", "insights", "strategy"]
        
        # Extract topic from prompt for more realistic content
        topic = "professional growth"
        if "startup" in generation_prompt.lower():
            topic = "startup lessons"
        elif "marketing" in generation_prompt.lower():
            topic = "marketing strategy"
        elif "AI" in generation_prompt.lower() or "artificial intelligence" in generation_prompt.lower():
            topic = "AI innovation"
        
        sample_posts = {
            "startup lessons": f"""🚀 Three years ago, I made the biggest mistake of my entrepreneurial career.

I spent 6 months building a product nobody wanted. Sound familiar?

Here's what I learned from that $50k lesson:

✅ Talk to customers BEFORE writing code
✅ Validate demand with pre-orders, not surveys  
✅ Build an MVP in 2 weeks, not 2 months

The hardest part? Admitting I was wrong and pivoting.

But that "failed" startup taught me more than any success ever could. It led to my next venture, which hit $1M ARR in 18 months.

Sometimes our biggest failures become our greatest teachers.

What's the most valuable lesson you've learned from a setback? 👇

#entrepreneurship #{persona.personal_brand_keywords[0].replace(' ', '')} #startups #growth""",
            
            "marketing strategy": f"""📈 I just analyzed 1,000 top-performing LinkedIn posts.

The results will surprise you.

It's not about fancy graphics or perfect copy.

It's about this one thing: AUTHENTICITY.

The posts that went viral had:
• Personal stories (not stock photos)
• Vulnerable moments (not just wins)
• Real data (not vague claims)
• Questions that actually matter

Stop trying to sound like everyone else.

Your unique perspective is your competitive advantage.

What's one authentic story you could share that would help your audience?

Drop it in the comments. Let's get real. 👇

#marketing #{persona.personal_brand_keywords[0].replace(' ', '')} #authenticity #growth""",
            
            "AI innovation": f"""🤖 AI won't replace humans.

Humans using AI will replace humans not using AI.

I've been experimenting with AI tools for 6 months, and here's what I've learned:

The magic isn't in the technology.
It's in asking better questions.

Best AI prompts I use daily:
• "Act as a [role] and help me [specific task]"
• "Challenge my assumptions about [topic]"
• "Create 10 variations of [idea] for [audience]"

The key? Treating AI as a thinking partner, not a replacement.

It amplifies your creativity but can't replace your judgment.

How are you using AI to level up your work? Share your best prompts below! 👇

#AI #{persona.personal_brand_keywords[0].replace(' ', '')} #innovation #futureofwork""",
        }
        
        # Use topic-specific post or create a generic one
        if topic in sample_posts:
            return sample_posts[topic]
        
        # Generic fallback post
        return f"""💡 Here's something I wish someone told me earlier in my {persona.niche.lower()} journey:

{persona.tone.title()} isn't just about attitude—it's a strategic advantage.

When you approach {persona.industry.lower()} with genuine {persona.tone} energy, three things happen:

1️⃣ You attract the right opportunities
2️⃣ You build stronger relationships  
3️⃣ You create solutions others miss

I learned this the hard way after years of taking the "safe" approach.

The moment I embraced being authentically {persona.tone}, everything changed.

My advice? Stop playing small. Your {persona.target_audience.lower()} need what you bring to the table.

What's one area where you could be more {persona.tone} in your approach?

#{persona.personal_brand_keywords[0].replace(' ', '')} #{persona.niche.lower().replace(' ', '')} #growth #authenticity"""
    
    async def generate_image_prompt(
        self, 
        post_content: str, 
        market_analysis: str, 
        persona: Persona
    ) -> str:
        """Generate mock image prompt."""
        
        # Analyze post content for image themes
        if "startup" in post_content.lower() or "entrepreneur" in post_content.lower():
            theme = "entrepreneurship"
        elif "marketing" in post_content.lower():
            theme = "marketing"
        elif "AI" in post_content.lower() or "technology" in post_content.lower():
            theme = "technology"
        else:
            theme = "professional"
        
        image_prompts = {
            "entrepreneurship": f"""Professional lifestyle photo showing a confident entrepreneur in a modern workspace. Clean, minimalist office setup with natural lighting. Person looking thoughtfully at a laptop screen with notebooks and coffee nearby. Warm, inspiring atmosphere that conveys {persona.tone} energy. Colors: navy blue, gold accents, clean whites. Professional but approachable aesthetic that resonates with {persona.target_audience}. High-quality, authentic feel - no stock photo vibes.""",
            
            "marketing": f"""Clean, modern graphic design showing marketing analytics dashboard or growth charts. Bright, energetic color scheme with blues and greens indicating upward trends. Include subtle elements like social media icons, engagement metrics, or conversion funnels. Professional but dynamic visual that appeals to {persona.target_audience}. Style should be {persona.tone} and data-driven, matching the analytical nature of marketing content.""",
            
            "technology": f"""Futuristic but approachable tech workspace scene. Modern computer setup with multiple monitors displaying code or AI interfaces. Clean, well-lit environment with subtle tech elements like circuit board patterns or digital overlays. Color palette: blues, purples, and whites with neon accents. Should feel cutting-edge but not intimidating, appealing to {persona.target_audience} in the {persona.industry} space.""",
            
            "professional": f"""Clean, professional headshot-style image or office environment that reflects {persona.industry} expertise. Person in business casual attire, looking confident and {persona.tone}. Background should be clean and uncluttered, perhaps a modern office or co-working space. Lighting should be bright and professional. Colors should align with {persona.tone} personality - warm and approachable. Image should inspire trust and authority in {persona.niche}."""
        }
        
        return image_prompts.get(theme, image_prompts["professional"])