# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

### Removed

## [0.2.0] - 2024-12-20

### Added
- **Table Generation Support**: Complete tabular data generation functionality
- **Multiple Output Formats**: Support for Markdown, CSV, HTML, and JSON table formats
- **Built-in Table Templates**: 5 pre-defined templates (user_profiles, product_catalog, sales_data, employees, financial_data)
- **TableRule Class**: Specialized rule class for defining table structures and generation rules
- **TableFormatter Utility**: Advanced formatting tools for various output formats
- **Table-specific API Methods**:
  - `generate_table()`: Main table generation method
  - `quick_table()`: Quick table generation from column names
  - `generate_table_from_template()`: Template-based table generation
  - `list_table_templates()`: List available built-in templates
  - `preview_table_template()`: Preview template structure
- **File Export Support**: Direct save to files with auto-format detection
- **Custom Table Configuration**: Support for dictionary-based table definitions

### Changed
- Extended `generate()` method to support `TableRule` objects
- Enhanced AI prompt generation for optimized table data creation
- Updated core imports to include table generation classes

### Fixed

### Removed

## [0.1.5] - 2024-12-19

### Added
- Intelligent changelog extraction for automated release notes generation
- Enhanced release workflow with dynamic content from CHANGELOG.md
- Professional release documentation with actual change details

### Changed
- Improved release.yml to automatically parse and extract version-specific changelog content
- Enhanced release notes format with better structure and documentation links
- Updated release process to eliminate generic templates in favor of actual change descriptions

### Fixed
- Replaced static release note templates with dynamic changelog-based content
- Improved release automation reliability and content accuracy

## [0.1.4] - 2024-12-19

### Added
- GitHub Actions CI/CD workflows for automated testing and releases
- Release automation script (`scripts/release.py`) for streamlined version management
- Comprehensive release documentation (`RELEASE.md`)
- Auto-formatting script (`scripts/fix_formatting.py`)
- Core rules modules: `basic_rules.py`, `combinations.py`, `packages.py`
- Built-in rule definitions for common data types (email, name, phone, etc.)
- Rule combination support for complex field generation
- Rule packages for complete object templates (person, company, product, etc.)

### Changed
- Updated development workflow to use automated releases
- Enhanced Makefile with release management commands (`make release`, `make release-check`)
- Optimized CI configuration to be non-blocking for formatting/linting issues
- Updated GitHub Actions to latest versions (v4) to resolve deprecation warnings
- Improved project structure with proper git tracking for core modules

### Fixed
- Fixed `.gitignore` that was incorrectly ignoring `lib/shadow_ai/rules/` directory
- Resolved GitHub Actions build failures due to deprecated action versions
- Fixed CI failures when no `tests/` directory exists (now skips gracefully)
- Fixed version synchronization between git tags and `pyproject.toml`
- Resolved duplicate method definitions in `Rule` class

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