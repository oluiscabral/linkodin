# LinkodIn

AI-powered LinkedIn post generator using advanced multi-agent system for creating viral, engaging content.

## Overview

LinkodIn is a sophisticated AI system that generates tailored LinkedIn posts using OpenAI's GPT models. It employs a three-agent approach:

1. **Market Analysis Agent**: Analyzes current market trends and crafts optimal prompts
2. **Content Generation Agent**: Creates viral LinkedIn posts based on the first agent's analysis
3. **Image Prompt Agent**: Generates compelling image descriptions to accompany posts

## Architecture

The project follows Clean Architecture principles:

- **Entities**: Business objects (Persona, Post)
- **Interactors**: Business logic and use cases
- **Infrastructure**: Concrete implementations (repositories, AI services)
- **CLI**: Command-line interface for user interaction

## Features

- **Persona Management**: Create and manage detailed LinkedIn personas
- **AI-Powered Generation**: Three-agent system for optimal content creation
- **Market Analysis**: Deep analysis of trends and algorithm preferences
- **Viral Content Focus**: Optimized for LinkedIn engagement and algorithm success
- **Multi-language Support**: Generate posts in different languages
- **Customizable Tones**: Professional, casual, inspirational, and more

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -e .
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

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

### List Personas

```bash
linkodin persona list
```

### Generate a Post

```bash
linkodin post generate tech-ceo --topic "AI transformation in B"
```

### View Generated Posts

```bash
linkodin post list
linkodin post show <post-id>
```

## Development

### Running Tests

```bash
pytest
```

### Project Structure

```
src/
├── entities/          # Business entities
│   ├── persona.py     # Persona entity
│   └── post.py        # Post entities
├── interactors/       # Business logic
│   ├── interfaces.py  # Repository and service interfaces
│   ├── persona_interactor.py
│   └── post_generation_interactor.py
├── infrastructure/    # Concrete implementations
│   ├── in_memory_persona_repository.py
│   ├── in_memory_post_repository.py
│   └── openai_service.py
└── cli/              # Command-line interface
    └── main.py
```

## Configuration

The system uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: gpt-5)

## Contributing

1. Follow Clean Architecture principles
2. Write tests for new features
3. Use type hints throughout
4. Follow PEP 8 style guidelines

## License

MIT License