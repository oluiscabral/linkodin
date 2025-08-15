#!/bin/bash
set -e

# LinkodIn CLI Build Script
# This script builds and packages the CLI for distribution

echo "🚀 Building LinkodIn CLI..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Not in a virtual environment. Creating one..."
    python -m venv build_env
    source build_env/bin/activate
    print_success "Virtual environment created and activated"
fi

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/
rm -f linkodin linkodin.exe

# Install build dependencies
print_status "Installing build dependencies..."
pip install --upgrade pip build twine pyinstaller

# Install the package in development mode
print_status "Installing LinkodIn CLI in development mode..."
pip install -e .

# Run tests
print_status "Running tests..."
if ! pytest tests/ -v --tb=short; then
    print_error "Tests failed! Please fix them before building."
    exit 1
fi
print_success "All tests passed!"

# Test CLI functionality
print_status "Testing CLI functionality..."
if ! linkodin --help > /dev/null; then
    print_error "CLI installation test failed!"
    exit 1
fi
print_success "CLI functionality test passed!"

# Build wheel and source distribution
print_status "Building Python packages..."
python -m build
print_success "Python packages built successfully!"

# Create standalone executable
print_status "Creating standalone executable..."
pyinstaller --onefile --name linkodin --add-data "src:src" --console src/cli/main.py

# Test the executable
if [[ -f "dist/linkodin" ]]; then
    print_status "Testing standalone executable..."
    if ! ./dist/linkodin --help > /dev/null; then
        print_error "Standalone executable test failed!"
        exit 1
    fi
    print_success "Standalone executable created and tested!"
    
    # Make it executable
    chmod +x dist/linkodin
else
    print_error "Failed to create standalone executable!"
    exit 1
fi

# Create distribution directory
print_status "Organizing distribution files..."
mkdir -p release/

# Copy built files
cp dist/*.whl release/
cp dist/*.tar.gz release/
cp dist/linkodin release/

# Create installation scripts
cat > release/install.sh << 'EOF'
#!/bin/bash
# LinkodIn CLI Installation Script

echo "🚀 Installing LinkodIn CLI..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Install the wheel package
WHEEL_FILE=$(ls LinkodIn-*.whl 2>/dev/null | head -n1)
if [ -f "$WHEEL_FILE" ]; then
    echo "📦 Installing from wheel: $WHEEL_FILE"
    pip install "$WHEEL_FILE"
    echo "✅ Installation complete!"
    echo ""
    echo "Try it out:"
    echo "  linkodin --help"
    echo "  linkodin persona create --help"
else
    echo "❌ No wheel file found. Please download the complete release package."
    exit 1
fi
EOF

chmod +x release/install.sh

# Create Windows installation script
cat > release/install.bat << 'EOF'
@echo off
echo 🚀 Installing LinkodIn CLI...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Install the wheel package
for %%f in (LinkodIn-*.whl) do (
    echo 📦 Installing from wheel: %%f
    pip install "%%f"
    echo ✅ Installation complete!
    echo.
    echo Try it out:
    echo   linkodin --help
    echo   linkodin persona create --help
    goto :end
)

echo ❌ No wheel file found. Please download the complete release package.
pause
exit /b 1

:end
pause
EOF

# Create README for release
cat > release/README.md << 'EOF'
# LinkodIn CLI Release Package

This package contains the LinkodIn CLI - an AI-powered LinkedIn post generator.

## Installation Options

### Option 1: Python Package (Recommended)
Run the installation script:
- **Linux/Mac**: `./install.sh`
- **Windows**: `install.bat`

Or install manually:
```bash
pip install LinkodIn-*.whl
```

### Option 2: Standalone Executable
Use the `linkodin` executable directly (Linux/Mac):
```bash
chmod +x linkodin
./linkodin --help
```

## Quick Start

1. Create a persona:
```bash
linkodin persona create --id "my-persona" --name "My Name" \
  --niche "My Field" --target-audience "My Audience" \
  --industry "My Industry" --content-themes "theme1,theme2" \
  --brand-keywords "keyword1,keyword2" --tone "professional"
```

2. Generate a post (demo mode):
```bash
linkodin post generate my-persona --topic "My Topic" --mock
```

3. For real AI generation, set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-key-here'
linkodin post generate my-persona --topic "My Topic"
```

## Support

For issues and feature requests, visit: https://github.com/oluiscabral/linkodin/issues
EOF

print_success "Build completed successfully!"
echo ""
echo "📦 Distribution files are in the 'release/' directory:"
ls -la release/
echo ""
echo "🎉 Ready for distribution!"
echo ""
echo "Next steps:"
echo "1. Test the release package: cd release && ./install.sh"
echo "2. Create a GitHub release with these files"
echo "3. Optionally publish to PyPI: twine upload release/*.whl"