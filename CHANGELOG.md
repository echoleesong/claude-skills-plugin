# Changelog

All notable changes to the Claude Skills Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-23

### Added

#### Skill Lifecycle Management System (NEW)
A complete lifecycle management system for Skills, inspired by modern DevOps practices:

- **skill-factory**: Automated Skill Factory
  - Convert any GitHub repository into a standardized Skill
  - Lightweight version check via `git ls-remote` (no full clone needed)
  - Auto-generate SKILL.md with extended metadata
  - Scripts: `fetch_github_info.py`, `create_skill.py`

- **skill-manager**: Skill Lifecycle Manager
  - Concurrent update checking for all Skills
  - Status reporting (outdated/current/unmanaged/error)
  - Inventory management (list, delete)
  - Scripts: `scan_and_check.py`, `list_skills.py`, `delete_skill.py`

- **skill-evolution**: Skill Evolution Manager
  - Persist lessons learned to `evolution.json`
  - Smart stitching: auto-inject experience into SKILL.md
  - Cross-version preservation: experience survives Skill updates
  - Scripts: `merge_evolution.py`, `smart_stitch.py`, `align_all.py`

#### Extended Metadata Specification
- New optional fields in SKILL.md frontmatter:
  - `source_url`: Source repository URL
  - `source_hash`: Commit hash for version tracking
  - `version`: Semantic version number
  - `created_at`, `updated_at`: Timestamps
  - `evolution_enabled`: Enable/disable experience evolution
- Full backward compatibility with existing Skills
- Documented in `docs/references/metadata-spec.md`

#### Standalone CLI Scripts
New `scripts/` directory with independent Python scripts for CI/CD:
- `check_updates.py`: Batch check update status (exit code 1 if outdated)
- `validate_all.py`: Batch validate metadata (supports strict mode)
- `batch_evolve.py`: Batch align evolution.json to SKILL.md

#### Documentation
- `docs/skill-lifecycle-development-plan.md`: Complete development plan
- `docs/references/metadata-spec.md`: Extended metadata specification v1.0
- Updated README.md and README_CN.md with new features

### Changed
- Plugin now contains 14 skills (was 10)
- Updated plugin structure documentation

## [1.0.0] - 2026-01-14

### Added

#### Plugin Infrastructure
- Created `.claude-plugin/plugin.json` with complete metadata
- Created `.claude-plugin/marketplace.json` for GitHub distribution
- Comprehensive bilingual README (English and Chinese)
- MIT License
- Structured changelog
- Designed as a general-purpose, extensible skills repository

#### n8n Development Skills (7 skills)
- **n8n-workflow-patterns**: Comprehensive workflow architectural patterns
  - 5 core patterns: Webhook Processing, HTTP API Integration, Database Operations, AI Agent Workflows, Scheduled Tasks
  - Pattern selection guide and workflow creation checklist
  - Real-world examples and best practices
  - Detailed pattern files for each workflow type

- **n8n-code-javascript**: Expert JavaScript Code node guidance
  - Data access patterns ($input.all(), $input.first(), $input.item)
  - Built-in functions reference ($helpers, DateTime, $jmespath)
  - 10 production-tested common patterns
  - Error prevention guide with top 5 mistakes
  - Loop processing patterns (critical for Split in Batches)

- **n8n-code-python**: Python Code node development
  - Python-specific data access patterns
  - Library integration (pandas, numpy, requests)
  - Error handling and debugging
  - Performance optimization tips

- **n8n-expression-syntax**: Expression language mastery
  - Expression syntax and data referencing
  - Built-in functions and methods
  - Date/time manipulation with Luxon
  - Common patterns and troubleshooting

- **n8n-node-configuration**: Node configuration expertise
  - Node-specific operation patterns
  - Operation dependencies and requirements
  - Authentication and credentials setup
  - Configuration validation

- **n8n-validation-expert**: Workflow validation
  - Workflow structure validation
  - Node configuration validation
  - Error detection and reporting
  - Auto-fix suggestions for common issues

- **n8n-mcp-tools-expert**: MCP tools integration
  - Node search and discovery
  - Template browsing and usage
  - Workflow creation via API
  - Operation validation

#### General Development Skills (1 skill)
- **skill-creator**: Skill development guide
  - Skill design principles and best practices
  - Progressive disclosure patterns
  - Bundled resources (scripts, references, assets)
  - 6-step skill creation process
  - Validation and packaging guidelines

### Documentation
- Bilingual README (English and Chinese) with language switcher
- Detailed skill descriptions and usage examples
- Installation methods (GitHub, local, plugin directory)
- Plugin philosophy: general-purpose, extensible, community-driven
- Contributing guidelines with suggested skill domains
- Plugin structure documentation

## [Unreleased]

### Planned
- Additional skills for other development domains:
  - API development and testing
  - DevOps and CI/CD
  - Data processing and analysis
  - Frontend/Backend frameworks
  - Testing frameworks
  - Documentation generation
- Integration examples and tutorials
- Community contributions

---

## Version History

- **1.1.0** (2026-01-23): Skill Lifecycle Management System - 3 new skills, CLI tools, extended metadata
- **1.0.0** (2026-01-14): Initial release as a general-purpose skills repository with 8 skills (7 n8n + 1 meta)
