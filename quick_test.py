#!/usr/bin/env python3
"""Quick test script to verify CLI functionality."""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and show the output."""
    print(f"\n🔹 {description}")
    print(f"Command: {cmd}")
    print("-" * 50)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=os.environ)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    return result.returncode == 0

def main():
    """Test the CLI functionality."""
    print("🚀 LinkodIn CLI Quick Test")
    print("=" * 50)
    
    # Activate virtual environment for all commands
    venv_prefix = "source venv/bin/activate && "
    
    # Test CLI help
    run_command(f"{venv_prefix}linkodin --help", "Testing CLI help")
    
    # Test persona help
    run_command(f"{venv_prefix}linkodin persona --help", "Testing persona help")
    
    # Create a test persona
    create_cmd = f"""{venv_prefix}linkodin persona create \\
  --id "test-persona" \\
  --name "Test Persona" \\
  --niche "Software Development" \\
  --target-audience "Developers, Tech leads" \\
  --industry "Technology" \\
  --content-themes "coding,best practices,career growth" \\
  --brand-keywords "clean code,software engineering,growth" \\
  --tone "professional" \\
  --description "A test persona for development"""
    
    if run_command(create_cmd, "Creating a test persona"):
        # List personas
        run_command(f"{venv_prefix}linkodin persona list", "Listing all personas")
        
        # Show persona details
        run_command(f"{venv_prefix}linkodin persona show test-persona", "Showing persona details")
        
        # Test post generation (will show API key requirement)
        run_command(f"{venv_prefix}linkodin post generate test-persona --topic 'Clean Code'", 
                   "Testing post generation (expected to require API key)")
        
        # List posts (should be empty)
        run_command(f"{venv_prefix}linkodin post list", "Listing posts")
        
        # Clean up - delete test persona
        run_command(f"{venv_prefix}linkodin persona delete test-persona --yes", "Cleaning up test persona")
    
    print("\n✅ CLI test completed!")
    print("\nTo enable post generation, set your OpenAI API key:")
    print("export OPENAI_API_KEY='your-api-key-here'")

if __name__ == "__main__":
    main()