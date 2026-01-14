# Claude Skills Plugin

[English](README.md) | [简体中文](README_CN.md) | [Quick Start](QUICKSTART.md)

A comprehensive and extensible Claude Code plugin providing expert-level skills for various development tasks and workflows. Currently focused on n8n workflow development, automation, and integration, with plans to expand to other domains.

> **🚀 Quick Install**: `/plugin marketplace add echoleesong/claude-skills-plugin` → `/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin`

## 📦 What's Included

This plugin currently contains 9 specialized skills, primarily focused on n8n workflow development:

### n8n Development Skills (7 skills)

1. **n8n-workflow-patterns** - Proven architectural patterns for building n8n workflows
   - 5 core patterns: Webhook Processing, HTTP API Integration, Database Operations, AI Agent Workflows, Scheduled Tasks
   - Pattern selection guide and workflow creation checklist
   - Real-world examples and best practices

2. **n8n-code-javascript** - Expert guidance for JavaScript Code nodes
   - Data access patterns ($input.all(), $input.first(), $input.item)
   - Built-in functions ($helpers, DateTime, $jmespath)
   - Common patterns and error prevention

3. **n8n-code-python** - Python Code node development
   - Python-specific patterns and best practices
   - Data manipulation and transformation
   - Integration with Python libraries

4. **n8n-expression-syntax** - Master n8n's expression language
   - Expression syntax and data referencing
   - Built-in functions and methods
   - Common patterns and troubleshooting

5. **n8n-node-configuration** - Configure nodes correctly
   - Node-specific configuration patterns
   - Operation dependencies and requirements
   - Authentication and credentials setup

6. **n8n-validation-expert** - Validate workflows before deployment
   - Workflow structure validation
   - Node configuration validation
   - Error detection and auto-fix suggestions

7. **n8n-mcp-tools-expert** - Use n8n MCP tools effectively
   - Search nodes and templates
   - Create and update workflows via API
   - Validate node operations

### General Development Skills (2 skills)

8. **skill-creator** - Guide for creating effective Claude Code skills
   - Skill design principles and best practices
   - Progressive disclosure patterns
   - Bundled resources (scripts, references, assets)

9. **More skills coming soon** - This plugin is designed to be extensible
   - Future skills may cover: API development, testing, DevOps, data processing, etc.
   - Community contributions welcome

## 🎯 Plugin Philosophy

This plugin is designed as a **general-purpose skills repository** that can accommodate skills from any domain:

- **Currently**: Primarily n8n workflow development skills (7 skills)
- **Future**: Will expand to include skills for other development areas
- **Extensible**: Easy to add new skills following the skill-creator guidelines
- **Community-driven**: Open to contributions from the community

## 🚀 Installation

### Method 1: Install from GitHub

```bash
# Add the marketplace
/plugin marketplace add echoleesong/claude-skills-plugin

# Install the plugin
/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin
```

### Method 2: Install from Local Path

```bash
# Clone the repository
git clone https://github.com/echoleesong/claude-skills-plugin.git

# Add local marketplace
/plugin marketplace add ./claude-skills-plugin

# Install the plugin
/plugin install claude-skills-plugin
```

### Method 3: Use Plugin Directory

```bash
# Clone the repository
git clone https://github.com/echoleesong/claude-skills-plugin.git

# Run Claude Code with plugin directory
claude --plugin-dir ./claude-skills-plugin
```

## 📖 Usage

Once installed, the skills will automatically activate when relevant tasks are detected.

### Current Skills Activation

**n8n Development:**
- **Building workflows**: `n8n-workflow-patterns` activates
- **Writing JavaScript code**: `n8n-code-javascript` activates
- **Writing Python code**: `n8n-code-python` activates
- **Using expressions**: `n8n-expression-syntax` activates
- **Configuring nodes**: `n8n-node-configuration` activates
- **Validating workflows**: `n8n-validation-expert` activates
- **Using MCP tools**: `n8n-mcp-tools-expert` activates

**General Development:**
- **Creating skills**: `skill-creator` activates

### Example Prompts

**n8n Development:**
```
"Help me build a webhook workflow that processes form submissions"
→ Activates: n8n-workflow-patterns, n8n-node-configuration

"Write JavaScript code to aggregate data from multiple API responses"
→ Activates: n8n-code-javascript

"Validate my workflow before deployment"
→ Activates: n8n-validation-expert
```

**General Development:**
```
"Create a new skill for PDF processing"
→ Activates: skill-creator

"Help me design a skill for API testing"
→ Activates: skill-creator
```

## 🎯 Skill Descriptions

### n8n Development Skills

#### n8n-workflow-patterns
Proven workflow architectural patterns from real n8n workflows. Use when building new workflows, designing workflow structure, choosing workflow patterns, planning workflow architecture, or asking about webhook processing, HTTP API integration, database operations, AI agent workflows, or scheduled tasks.

### n8n-code-javascript
Write JavaScript code in n8n Code nodes. Use when writing JavaScript in n8n, using $input/$json/$node syntax, making HTTP requests with $helpers, working with dates using DateTime, troubleshooting Code node errors, or choosing between Code node modes.

### n8n-code-python
Write Python code in n8n Code nodes. Use when writing Python in n8n, using item access patterns, working with pandas/numpy, making HTTP requests, handling data transformations, or troubleshooting Python Code node errors.

### n8n-expression-syntax
Master n8n's expression language for data transformation and manipulation. Use when writing expressions in n8n nodes, accessing data from previous nodes, using built-in functions, formatting dates/strings, or troubleshooting expression errors.

### n8n-node-configuration
Configure n8n nodes correctly with proper operations and parameters. Use when configuring specific node operations, understanding node requirements, setting up authentication, or troubleshooting node configuration errors.

### n8n-validation-expert
Validate n8n workflows and node configurations before deployment. Use when validating workflow structure, checking node configurations, detecting errors, or getting auto-fix suggestions for common issues.

### n8n-mcp-tools-expert
Expert guidance for using n8n MCP (Model Context Protocol) tools. Use when searching for nodes, getting node documentation, creating workflows via API, validating operations, or working with n8n programmatically.

### General Development Skills

#### skill-creator
Guide for creating effective Claude Code skills. Use when creating new skills, updating existing skills, designing skill structure, writing skill documentation, or learning skill best practices.

## 📁 Plugin Structure

```
claude-skills-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata
│   └── marketplace.json     # Marketplace configuration
├── skills/
│   ├── n8n-workflow-patterns/
│   ├── n8n-code-javascript/
│   ├── n8n-code-python/
│   ├── n8n-expression-syntax/
│   ├── n8n-node-configuration/
│   ├── n8n-validation-expert/
│   ├── n8n-mcp-tools-expert/
│   └── skill-creator/
├── LICENSE
├── README.md
└── CHANGELOG.md
```

## 🤝 Contributing

Contributions are welcome! This plugin is designed to be a community-driven skills repository.

### How to Contribute

1. **Add new skills**: Use the `skill-creator` skill to design and implement new skills
2. **Improve existing skills**: Submit PRs to enhance current skills
3. **Report issues**: Help us identify bugs or areas for improvement
4. **Suggest new skill domains**: Propose new areas where skills would be valuable

### Skill Domains We're Interested In

- API development and testing
- DevOps and CI/CD
- Data processing and analysis
- Frontend/Backend frameworks
- Testing frameworks
- Documentation generation
- And more!

Please feel free to submit issues or pull requests.

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- **Repository**: https://github.com/echoleesong/claude-skills-plugin
- **Issues**: https://github.com/echoleesong/claude-skills-plugin/issues
- **n8n Documentation**: https://docs.n8n.io

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## 🙏 Acknowledgments

- n8n skills are built based on real-world workflow development experience and best practices from the n8n community
- skill-creator is inspired by Claude Code's official skill development guidelines
- Thanks to all contributors and the Claude Code community

---

**Made with ❤️ for the Claude Code community**
