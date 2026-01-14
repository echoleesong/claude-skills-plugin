# Changelog

All notable changes to the Claude Skills Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

- **1.0.0** (2026-01-14): Initial release as a general-purpose skills repository with 8 skills (7 n8n + 1 meta)
