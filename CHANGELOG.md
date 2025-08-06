# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD workflows for automated testing and releases
- Release automation script (`scripts/release.py`)
- Comprehensive release documentation

### Changed
- Updated development workflow to use automated releases
- Enhanced Makefile with release management commands

### Fixed

### Removed

## [0.1.2] - 2024-01-XX

### Added
- Initial release with core functionality
- Rule-based mock data generation
- Integration with Agno framework
- Support for custom rules and combinations
- File-based rule loading (JSON/YAML)
- Quick generation methods

### Changed

### Fixed

### Removed

---

## Release Process

When preparing a new release:

1. Update the `[Unreleased]` section with the new version number and date
2. Create a new `[Unreleased]` section for future changes
3. Use the release script: `python scripts/release.py <version>`
4. The GitHub Actions workflow will handle the rest automatically

## Categories

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes 