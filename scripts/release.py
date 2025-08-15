#!/usr/bin/env python3
"""
LinkodIn CLI Release Script

This script automates the release process:
1. Updates version numbers
2. Creates git tag
3. Triggers GitHub Actions release workflow
4. Generates release notes
"""

import os
import re
import sys
import subprocess
import argparse
from datetime import datetime
from typing import Optional


class ReleaseManager:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.project_root = self._find_project_root()
        
    def _find_project_root(self) -> str:
        """Find the project root directory."""
        current = os.path.abspath(os.path.dirname(__file__))
        while current != "/":
            if os.path.exists(os.path.join(current, "pyproject.toml")):
                return current
            current = os.path.dirname(current)
        raise RuntimeError("Could not find project root (no pyproject.toml found)")
    
    def _run_command(self, cmd: str, capture_output: bool = False) -> Optional[str]:
        """Run a shell command."""
        print(f"🔧 Running: {cmd}")
        if self.dry_run:
            print("   (DRY RUN - command not executed)")
            return None
            
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=self.project_root,
            capture_output=capture_output,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            if capture_output:
                print(f"Error: {result.stderr}")
            sys.exit(1)
            
        return result.stdout.strip() if capture_output else None
    
    def _update_version_in_file(self, filepath: str, new_version: str) -> None:
        """Update version in a file."""
        full_path = os.path.join(self.project_root, filepath)
        
        if not os.path.exists(full_path):
            print(f"⚠️  File not found: {filepath}")
            return
            
        with open(full_path, 'r') as f:
            content = f.read()
        
        # Update version in pyproject.toml
        if filepath == "pyproject.toml":
            content = re.sub(
                r'version = "[^"]*"',
                f'version = "{new_version}"',
                content
            )
        
        print(f"📝 Updating version in {filepath} to {new_version}")
        if not self.dry_run:
            with open(full_path, 'w') as f:
                f.write(content)
    
    def _get_current_version(self) -> str:
        """Get current version from pyproject.toml."""
        pyproject_path = os.path.join(self.project_root, "pyproject.toml")
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        match = re.search(r'version = "([^"]*)"', content)
        if match:
            return match.group(1)
        
        raise RuntimeError("Could not find version in pyproject.toml")
    
    def _validate_version(self, version: str) -> str:
        """Validate and normalize version string."""
        # Remove 'v' prefix if present
        version = version.lstrip('v')
        
        # Check if it's a valid semantic version
        if not re.match(r'^\d+\.\d+\.\d+(-\w+)?$', version):
            raise ValueError(f"Invalid version format: {version}. Use semantic versioning (e.g., 1.0.0)")
        
        return version
    
    def _update_changelog(self, version: str) -> None:
        """Update CHANGELOG.md with new version."""
        changelog_path = os.path.join(self.project_root, "CHANGELOG.md")
        
        if not os.path.exists(changelog_path):
            print("⚠️  CHANGELOG.md not found, skipping changelog update")
            return
        
        with open(changelog_path, 'r') as f:
            content = f.read()
        
        # Replace [Unreleased] with version and date
        today = datetime.now().strftime('%Y-%m-%d')
        content = content.replace(
            "## [Unreleased]",
            f"## [Unreleased]\n\n### Added\n- Preparation for next release\n\n## [{version}] - {today}"
        )
        
        print(f"📝 Updating CHANGELOG.md for version {version}")
        if not self.dry_run:
            with open(changelog_path, 'w') as f:
                f.write(content)
    
    def _run_tests(self) -> None:
        """Run the test suite."""
        print("🧪 Running tests...")
        if not self.dry_run:
            self._run_command("python -m pytest tests/ -v")
        print("✅ Tests passed!")
    
    def _check_git_status(self) -> None:
        """Check if git working directory is clean."""
        if self.dry_run:
            print("🔍 Checking git status (dry run)")
            return
            
        result = self._run_command("git status --porcelain", capture_output=True)
        if result:
            print("❌ Git working directory is not clean. Please commit or stash changes.")
            print("Uncommitted changes:")
            print(result)
            sys.exit(1)
        print("✅ Git working directory is clean")
    
    def _create_git_tag(self, version: str) -> None:
        """Create and push git tag."""
        tag = f"v{version}"
        print(f"🏷️  Creating git tag: {tag}")
        
        # Create tag
        self._run_command(f"git tag -a {tag} -m 'Release {tag}'")
        
        # Push tag
        self._run_command(f"git push origin {tag}")
    
    def _commit_version_changes(self, version: str) -> None:
        """Commit version update changes."""
        print(f"💾 Committing version changes for {version}")
        
        self._run_command("git add pyproject.toml CHANGELOG.md")
        self._run_command(f"git commit -m 'chore: bump version to {version}'")
        self._run_command("git push origin main")
    
    def release(self, version: str, skip_tests: bool = False) -> None:
        """Execute the full release process."""
        print(f"🚀 Starting release process for version {version}")
        print(f"   Dry run: {self.dry_run}")
        print()
        
        # Validate version
        version = self._validate_version(version)
        current_version = self._get_current_version()
        
        print(f"📊 Current version: {current_version}")
        print(f"📊 New version: {version}")
        
        if version <= current_version:
            print("❌ New version must be greater than current version")
            sys.exit(1)
        
        # Pre-release checks
        if not skip_tests:
            self._run_tests()
        
        self._check_git_status()
        
        # Update version files
        self._update_version_in_file("pyproject.toml", version)
        self._update_changelog(version)
        
        # Commit changes
        if not self.dry_run:
            self._commit_version_changes(version)
        
        # Create and push tag (this will trigger GitHub Actions)
        if not self.dry_run:
            self._create_git_tag(version)
        
        print()
        print("🎉 Release process completed!")
        print()
        print("Next steps:")
        print(f"1. Check GitHub Actions: https://github.com/oluiscabral/linkodin/actions")
        print(f"2. Review the release: https://github.com/oluiscabral/linkodin/releases/tag/v{version}")
        print("3. Announce the release to users")
        
        if self.dry_run:
            print()
            print("🔍 This was a dry run. To actually release, run without --dry-run")


def main():
    parser = argparse.ArgumentParser(description="LinkodIn CLI Release Manager")
    parser.add_argument("version", help="Version to release (e.g., 1.0.0 or v1.0.0)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    
    args = parser.parse_args()
    
    release_manager = ReleaseManager(dry_run=args.dry_run)
    
    try:
        release_manager.release(args.version, skip_tests=args.skip_tests)
    except KeyboardInterrupt:
        print("\n❌ Release cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Release failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()