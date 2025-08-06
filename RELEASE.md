# Release Process

This document describes the release process for ShadowAI.

## Automated Release Workflow

ShadowAI uses GitHub Actions for automated releases. The process is triggered when you push a tag to the repository.

### Quick Release Steps

1. **Update version** (if not already done):
   ```bash
   # Option 1: Use the release script
   python scripts/release.py 0.1.3
   
   # Option 2: Manual process
   # Update version in pyproject.toml
   # Commit changes: git commit -am "Bump version to 0.1.3"
   # Create tag: git tag -a v0.1.3 -m "Release v0.1.3"
   # Push: git push origin main && git push origin v0.1.3
   ```

2. **Monitor the release**:
   - Check [GitHub Actions](https://github.com/KevinZhang19870314/shadowai/actions)
   - Verify PyPI publication
   - Check GitHub release creation

## GitHub Actions Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)
- **Trigger**: Push to main/develop, Pull requests
- **Purpose**: Run tests, linting, type checking across Python versions
- **Features**:
  - Matrix testing (Python 3.8-3.12)
  - Code quality checks (black, isort, flake8, mypy)
  - Test coverage reporting

### 2. Release Workflow (`.github/workflows/release.yml`)
- **Trigger**: Push tags matching `v*` (e.g., `v0.1.3`)
- **Purpose**: Build, publish to PyPI, create GitHub release
- **Features**:
  - Automated PyPI publishing using trusted publishing
  - GitHub release creation with auto-generated notes
  - Includes both source and wheel distributions

### 3. Test PyPI Workflow (`.github/workflows/publish-test.yml`)
- **Trigger**: Push to develop branch, manual dispatch
- **Purpose**: Publish to Test PyPI for testing
- **Features**:
  - Test releases before main PyPI
  - Skip existing versions

## Prerequisites

### GitHub Repository Setup

1. **Secrets Configuration**:
   - No PyPI token needed (using trusted publishing)
   - Optional: `TEST_PYPI_API_TOKEN` for test publishing

2. **PyPI Trusted Publishing**:
   - Configure at https://pypi.org/manage/project/shadowai/settings/
   - Add GitHub as trusted publisher:
     - Owner: `KevinZhang19870314`
     - Repository: `shadowai`
     - Workflow: `release.yml`
     - Environment: (leave empty)

### Local Development Setup

1. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **Pre-commit hooks** (optional):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Version Management

### Version Format
- Use semantic versioning: `MAJOR.MINOR.PATCH`
- Pre-releases: `MAJOR.MINOR.PATCH-alpha.N`, `MAJOR.MINOR.PATCH-beta.N`

### Updating Version
1. **In pyproject.toml**:
   ```toml
   version = "0.1.3"
   ```

2. **Using release script**:
   ```bash
   python scripts/release.py 0.1.3
   ```

## Release Types

### Regular Release
```bash
git tag -a v0.1.3 -m "Release v0.1.3"
git push origin v0.1.3
```

### Pre-release
```bash
git tag -a v0.1.3-beta.1 -m "Release v0.1.3-beta.1"
git push origin v0.1.3-beta.1
```
*Note: Pre-releases are automatically marked as "pre-release" on GitHub*

## Troubleshooting

### Failed Release
1. Check GitHub Actions logs
2. Verify tag format matches `v*`
3. Ensure version in pyproject.toml is correct
4. Check PyPI trusted publishing configuration

### Rollback Release
1. Delete the tag locally and remotely:
   ```bash
   git tag -d v0.1.3
   git push origin :refs/tags/v0.1.3
   ```
2. Delete the GitHub release (if created)
3. Contact PyPI to remove the package version (if necessary)

## Manual Release (Emergency)

If automated release fails:

1. **Build locally**:
   ```bash
   python -m build
   ```

2. **Publish to PyPI**:
   ```bash
   twine upload dist/*
   ```

3. **Create GitHub release manually** using the web interface

## Post-Release

1. **Verify installation**:
   ```bash
   pip install shadowai==0.1.3
   ```

2. **Update documentation** if needed

3. **Announce release** in relevant channels

4. **Plan next release** based on roadmap 