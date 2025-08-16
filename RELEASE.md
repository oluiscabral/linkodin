# Release Guide for LinkodIn CLI

This document describes how to create and publish releases for the LinkodIn CLI.

## Release Process Overview

The release process is automated using GitHub Actions and includes:
1. Testing across multiple Python versions and platforms
2. Building Python packages (wheel and source distribution)
3. Creating standalone executables for Windows, macOS, and Linux
4. Publishing to GitHub Releases
5. Optionally publishing to PyPI

## Quick Release

### Option 1: Automated Release Script (Recommended)

```bash
# Test the release process (dry run)
python scripts/release.py 1.0.0 --dry-run

# Create actual release
python scripts/release.py 1.0.0
```

### Option 2: Manual Git Tag

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

### Option 3: GitHub UI

Use the GitHub Actions "Release LinkodIn CLI" workflow with manual dispatch.

## Detailed Release Steps

### 1. Pre-Release Checklist

- [ ] All tests are passing
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated with new features/fixes
- [ ] Version is bumped in pyproject.toml
- [ ] No uncommitted changes in git

### 2. Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes
- **Minor** (1.X.0): New features, backward compatible
- **Patch** (1.0.X): Bug fixes, backward compatible

Examples:
- `v1.0.0` - Initial stable release
- `v1.1.0` - New features added
- `v1.1.1` - Bug fixes
- `v2.0.0` - Breaking changes

### 3. Release Workflows

#### Test Workflow (`.github/workflows/test.yml`)
- Runs on every push and PR
- Tests across Python 3.9-3.12
- Tests on Ubuntu, Windows, and macOS
- Includes linting and security checks

#### Release Workflow (`.github/workflows/release.yml`)
Triggers on:
- Git tags matching `v*.*.*`
- Manual workflow dispatch

Creates:
- Python wheel and source distribution
- Standalone executables for all platforms
- GitHub release with assets
- Publishes to PyPI (if token configured)

#### Build Executables Workflow (`.github/workflows/build-executables.yml`)
- Creates platform-specific standalone executables
- Includes README and installation instructions
- Uploads as GitHub release assets

### 4. Build Scripts

#### Local Build Script (`scripts/build.sh`)
```bash
# Build locally for testing
./scripts/build.sh
```

Creates:
- Python packages in `dist/`
- Standalone executable
- Release package in `release/`

#### Release Management Script (`scripts/release.py`)
```bash
# Full release automation
python scripts/release.py 1.0.0
```

Handles:
- Version updating
- Changelog management
- Git tagging and pushing
- Triggering GitHub Actions

### 5. Release Assets

Each release includes:

#### Python Packages
- `LinkodIn-X.Y.Z-py3-none-any.whl` - Wheel package
- `LinkodIn-X.Y.Z.tar.gz` - Source distribution

#### Standalone Executables
- `linkodin-linux-x64` - Linux executable
- `linkodin-windows-x64.exe` - Windows executable
- `linkodin-macos-x64` - macOS executable

#### Documentation
- README.txt with installation instructions
- Installation scripts (install.sh, install.bat)

### 6. PyPI Publishing

To publish to PyPI, add your PyPI token to GitHub Secrets:

1. Generate token at https://pypi.org/manage/account/token/
2. Add as `PYPI_TOKEN` secret in GitHub repository settings
3. The release workflow will automatically publish

### 7. Post-Release Tasks

- [ ] Verify release assets are downloadable
- [ ] Test installation from PyPI
- [ ] Test standalone executables
- [ ] Update documentation if needed
- [ ] Announce release to users

## Release Checklist Template

```markdown
## Release vX.Y.Z Checklist

### Pre-Release
- [ ] All tests passing locally
- [ ] CHANGELOG.md updated
- [ ] Version bumped in pyproject.toml
- [ ] Clean git working directory
- [ ] README.md is current

### Release
- [ ] Tag created and pushed
- [ ] GitHub Actions completed successfully
- [ ] Release assets uploaded
- [ ] PyPI package published

### Post-Release
- [ ] Installation tested from PyPI
- [ ] Standalone executables tested
- [ ] Documentation updated
- [ ] Release announced
```

## Troubleshooting

### Common Issues

1. **Tests failing in CI**
   - Check test output in GitHub Actions
   - Run tests locally: `pytest tests/ -v`

2. **Build failures**
   - Check Python version compatibility
   - Verify all dependencies are available

3. **PyPI publishing fails**
   - Verify PYPI_TOKEN is set correctly
   - Check if version already exists on PyPI

4. **Executable creation fails**
   - Check PyInstaller compatibility
   - Verify all imports are properly packaged

### Manual Recovery

If automated release fails:

```bash
# Clean up failed tag
git tag -d v1.0.0
git push origin :v1.0.0

# Fix issues and retry
python scripts/release.py 1.0.0
```

## Security

- Never commit API keys or tokens
- Use GitHub Secrets for sensitive data
- Verify release assets before publishing
- Sign releases if required by your organization

## Support

For questions about the release process:
1. Check GitHub Actions logs
2. Review this documentation
3. Create an issue in the repository