# LinkodIn - Demo & Usage Guide

## 🚀 Quick Start

### Installation
```bash
# Clone or extract the project
cd linkodin

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Set up OpenAI API key (required for post generation)
export OPENAI_API_KEY='your-openai-api-key-here'
```

### Run the Demo
```bash
python demo.py
```

## 🎭 Persona Management

### Create a Persona
```bash
linkodin persona create \
  --id "tech-ceo" \
  --name "Tech CEO" \
  --niche "Technology Leadership" \
  --target-audience "Tech professionals, entrepreneurs, investors" \
  --industry "Technology" \
  --content-themes "leadership,innovation,startup insights,tech trends" \
  --brand-keywords "innovation,leadership,growth,technology" \
  --tone "inspirational"
```

### List All Personas
```bash
linkodin persona list
```

### Show Persona Details
```bash
linkodin persona show tech-ceo
```

### Delete a Persona
```bash
linkodin persona delete tech-ceo
```

## 📝 Post Generation

### Generate a Post
```bash
linkodin post generate tech-ceo --topic "AI transformation in business"
```

### Generate with Additional Context
```bash
linkodin post generate tech-ceo \
  --topic "Remote work trends" \
  --context "Focus on productivity and team collaboration"
```

### List All Posts
```bash
linkodin post list
```

### List Posts by Persona
```bash
linkodin post list --persona tech-ceo
```

### Show Post Details
```bash
linkodin post show <post-id>
```

## 🤖 AI Agent System

The system uses three AI agents for optimal post generation:

1. **Market Analysis Agent**: Analyzes current LinkedIn trends and crafts optimal prompts
2. **Content Generation Agent**: Creates viral posts based on the analysis
3. **Image Prompt Agent**: Generates compelling image descriptions

## 🧪 Testing

Run the complete test suite:
```bash
pytest tests/ -v
```

All 38 tests should pass ✅

## 📁 Project Structure

```
src/
├── entities/           # Business entities
│   ├── persona.py     # Persona entity with validation
│   └── post.py        # Post entities and requests
├── interactors/       # Business logic layer
│   ├── interfaces.py  # Repository and service interfaces
│   ├── persona_interactor.py
│   └── post_generation_interactor.py
├── infrastructure/    # Concrete implementations
│   ├── in_memory_persona_repository.py
│   ├── in_memory_post_repository.py
│   └── openai_service.py  # OpenAI GPT integration
└── cli/              # Command-line interface
    └── main.py
```

## 🏗️ Architecture Highlights

- **Clean Architecture**: Separation of concerns with entities, interactors, and infrastructure
- **Dependency Injection**: Interfaces allow for easy testing and extension
- **Repository Pattern**: Abstract data storage from business logic
- **Command Pattern**: CLI commands are organized and testable
- **Error Handling**: Comprehensive validation and error messages

## 🔧 Extensibility

### Adding New Repositories
Implement the `PersonaRepository` or `PostRepository` interfaces:
```python
class DatabasePersonaRepository(PersonaRepository):
    async def save_persona(self, persona: Persona) -> None:
        # Your database implementation
        pass
```

### Adding New AI Services
Implement the `AIService` interface:
```python
class CustomAIService(AIService):
    async def generate_market_analysis_and_prompt(self, ...):
        # Your AI implementation
        pass
```

## 💡 Example Personas

### Tech CEO
- **Niche**: Technology Leadership
- **Tone**: Inspirational
- **Themes**: Leadership, Innovation, Startup Insights

### Marketing Guru
- **Niche**: Digital Marketing
- **Tone**: Enthusiastic
- **Themes**: Growth Marketing, Social Media, ROI

### AI Researcher
- **Niche**: Artificial Intelligence
- **Tone**: Professional
- **Themes**: Machine Learning, AI Ethics, Research

## 🎯 Key Features

✅ **Three-Agent AI System**: Market analysis → Content generation → Image prompts  
✅ **Viral Content Focus**: Optimized for LinkedIn engagement and algorithm success  
✅ **Multi-Persona Support**: Create unlimited personas with detailed configurations  
✅ **CLI Interface**: Easy-to-use command-line tools  
✅ **Clean Architecture**: Maintainable and testable codebase  
✅ **Comprehensive Testing**: 38 tests covering all major functionality  
✅ **Extensible Design**: Repository and service patterns for easy extension  

## 🚀 Next Steps

1. **Set up your OpenAI API key** to enable post generation
2. **Create your first persona** using the CLI
3. **Generate viral LinkedIn posts** with AI-powered content
4. **Extend the system** with additional repositories or services as needed

Happy posting! 🎉