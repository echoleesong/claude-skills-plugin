# Claude Skills Plugin

[English](README.md) | [简体中文](README_CN.md) | [Quick Start](QUICKSTART.md)

A comprehensive and extensible Claude Code plugin providing expert-level skills for various development tasks and workflows. Currently focused on n8n workflow development, automation, and integration, with plans to expand to other domains.

> **🚀 Quick Install (Recommended)**: Clone skills directly to `~/.claude/skills/` for **highest priority**

## 📦 What's Included

This plugin currently contains **14 specialized skills**, covering n8n workflow development and **Skill lifecycle management**:

### Skill Lifecycle Management (3 skills) - **NEW**

11. **skill-factory** - Automated Skill Factory
    - Convert any GitHub repository into a standardized Skill with one command
    - Automatically fetch repository metadata (commit hash, README)
    - Generate compliant directory structure with extended metadata

12. **skill-manager** - Skill Lifecycle Manager
    - Concurrently check update status for all Skills
    - Support batch scan, update, and delete operations
    - Generate status reports (outdated/current/unmanaged)

13. **skill-evolution** - Skill Evolution Manager
    - Persist lessons learned from conversations to `evolution.json`
    - Smart stitching: automatically write experience to SKILL.md
    - Cross-version preservation: experience survives Skill updates

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

### General Development Skills (4 skills)

8. **skill-creator** - Guide for creating effective Claude Code skills
   - Skill design principles and best practices
   - Progressive disclosure patterns
   - Bundled resources (scripts, references, assets)

9. **md-to-pptx** - Convert Markdown to PowerPoint presentations
   - Convert existing Markdown files to PPTX
   - Generate presentations from scratch with AI assistance
   - Multiple themes (business, tech_dark, education, neumorphism)
   - Custom template support

10. **skill-lookup** - Skill discovery and installation tool
    - Search and discover available Skills
    - Install and manage Skills

14. **More skills coming soon** - This plugin is designed to be extensible
   - Future skills may cover: API development, testing, DevOps, data processing, etc.
   - Community contributions welcome

## 🎯 Plugin Philosophy

This plugin is designed as a **general-purpose skills repository** that can accommodate skills from any domain:

- **Currently**: Primarily n8n workflow development skills (7 skills)
- **Future**: Will expand to include skills for other development areas
- **Extensible**: Easy to add new skills following the skill-creator guidelines
- **Community-driven**: Open to contributions from the community

## 🚀 Installation

### Understanding Skills Priority

Claude Code Skills are loaded with different priorities (highest to lowest):

| Priority | Level | Location | Scope |
|:--------:|:------|:---------|:------|
| **1** (Highest) | Enterprise | Managed settings | Organization-wide |
| **2** | Personal | `~/.claude/skills/` | All your projects |
| **3** | Project | `.claude/skills/` | Current project |
| **4** (Lowest) | Plugin | Plugin `skills/` directory | Plugin users |

**We recommend Method 1** for the best experience, as it gives your Skills the highest non-enterprise priority.

---

### ⭐ Method 1: Personal Skills Directory (Recommended)

Install directly to your personal skills folder for **highest priority**:

#### macOS / Linux

```bash
# Clone to personal skills repository directory
git clone https://github.com/echoleesong/claude-skills-plugin.git ~/.claude/skills-repo

# Run automatic install script (creates symlinks)
cd ~/.claude/skills-repo && ./install.sh
```

#### Windows (PowerShell, requires Administrator)

```powershell
# Clone to personal skills repository directory
git clone https://github.com/echoleesong/claude-skills-plugin.git "$env:USERPROFILE\.claude\skills-repo"

# Run automatic install script (requires Administrator for symlinks)
cd "$env:USERPROFILE\.claude\skills-repo"
.\install.ps1
```

#### Update Skills

```bash
# macOS / Linux
cd ~/.claude/skills-repo && git pull && ./install.sh

# Windows (PowerShell)
cd "$env:USERPROFILE\.claude\skills-repo"; git pull; .\install.ps1
```

#### 🔄 Setup Auto-Sync (Optional)

Automatically sync new skills after `git pull`:

```bash
# macOS / Linux
cd ~/.claude/skills-repo && ./setup-hooks.sh

# After setup, git pull will automatically run install.sh
```

✅ **Advantages**: Highest priority (Personal level), takes precedence over all plugins, easy to update with `git pull`, supports auto-sync.

<details>
<summary>📌 Manual Installation (without scripts)</summary>

If you prefer not to use the install scripts, you can manually create symlinks:

**macOS / Linux:**
```bash
mkdir -p ~/.claude/skills && \
ln -sf ~/.claude/skills-repo/skills/* ~/.claude/skills/
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
Get-ChildItem "$env:USERPROFILE\.claude\skills-repo\skills" -Directory | ForEach-Object {
    New-Item -ItemType SymbolicLink -Force -Path "$env:USERPROFILE\.claude\skills\$($_.Name)" -Target $_.FullName
}
```

</details>

---

### Method 2: Plugin Marketplace (Standard)

Install as a plugin via Claude Code marketplace:

```bash
# Add the marketplace
/plugin marketplace add echoleesong/claude-skills-plugin

# Install the plugin
/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin
```

⚠️ **Note**: Plugin Skills have the **lowest priority**. If you need higher priority, use Method 1 or upgrade after installation:

<details>
<summary>📌 Upgrade Plugin to Personal Priority</summary>

```bash
# macOS / Linux: Link plugin skills to personal directory
mkdir -p ~/.claude/skills && \
ln -sf ~/.claude/plugins/cache/claude-skills-plugin-marketplace/claude-skills-plugin/*/skills/* ~/.claude/skills/
```

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
$pluginPath = Get-ChildItem "$env:USERPROFILE\.claude\plugins\cache\claude-skills-plugin-marketplace\claude-skills-plugin\*\skills" | Select-Object -First 1
Get-ChildItem $pluginPath -Directory | ForEach-Object {
    New-Item -ItemType SymbolicLink -Force -Path "$env:USERPROFILE\.claude\skills\$($_.Name)" -Target $_.FullName
}
```

</details>

---

### Method 3: Project-Level Installation

Install for a specific project only:

```bash
# In your project directory
git clone https://github.com/echoleesong/claude-skills-plugin.git .claude/skills-repo

# Link skills to project directory
mkdir -p .claude/skills && \
ln -sf .claude/skills-repo/skills/* .claude/skills/
```

✅ **Use case**: When you only need these skills for a specific project.

---

### Verify Installation

Restart Claude Code and ask: "What Skills are available?"

You should see this plugin's Skills listed. If you used Method 1, they will have Personal-level priority.

## 📖 Usage

Once installed, the skills will automatically activate when relevant tasks are detected.

### Current Skills Activation

**Skill Lifecycle Management:**
- **Create Skill from GitHub**: `/skill-factory <url>` or "Package this repo into a skill"
- **Check updates**: `/skill-manager check` or "Check my Skills for updates"
- **List Skills**: `/skill-manager list` or "List my Skills"
- **Record experience**: `/skill-evolution` or "Review the conversation and save lessons"

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
- **Creating presentations**: `md-to-pptx` activates

### Example Prompts

**Skill Lifecycle Management:**
```
"Package https://github.com/yt-dlp/yt-dlp into a Skill"
→ Activates: skill-factory

"Check my Skills for updates"
→ Activates: skill-manager

"Save the lessons from this conversation"
→ Activates: skill-evolution
```

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

"Help me create a presentation about machine learning"
→ Activates: md-to-pptx

"Convert this markdown file to PowerPoint"
→ Activates: md-to-pptx
```

## 🎯 Skill Descriptions

### Skill Lifecycle Management Skills

#### skill-factory
Automated factory for converting GitHub repositories into standardized AI skills. Use when user provides a GitHub URL and wants to "package", "wrap", or "create a skill" from it. Automatically fetches repository metadata, generates standard directory structure, and injects extended metadata for lifecycle management.

#### skill-manager
Skill lifecycle manager for batch scanning Skills directory, checking GitHub updates, performing version upgrades, and managing Skills inventory. Supports `/skill-manager check`, `/skill-manager list`, `/skill-manager delete` commands.

#### skill-evolution
Skill experience evolution manager. Analyzes user feedback at the end of conversations, extracts best practices and solutions, persists to `evolution.json` and stitches to SKILL.md. Use when user says "review", "record experience", "save this tip".

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

#### md-to-pptx
Convert Markdown documents to PowerPoint presentations or generate presentations from scratch using AI. Use when users want to create PPT/PPTX files, convert MD to slides, generate presentations, make slideshows, or ask for help with PowerPoint creation. Supports custom templates, multiple themes (business, tech_dark, education, neumorphism), and intelligent content layout.

## 📁 Plugin Structure

```
claude-skills-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata
│   └── marketplace.json     # Marketplace configuration
├── skills/
│   ├── skill-factory/       # Skill Factory (NEW)
│   ├── skill-manager/       # Skill Manager (NEW)
│   ├── skill-evolution/     # Skill Evolution (NEW)
│   ├── n8n-workflow-patterns/
│   ├── n8n-code-javascript/
│   ├── n8n-code-python/
│   ├── n8n-expression-syntax/
│   ├── n8n-node-configuration/
│   ├── n8n-validation-expert/
│   ├── n8n-mcp-tools-expert/
│   ├── skill-creator/
│   ├── skill-lookup/
│   └── md-to-pptx/
├── scripts/                 # Standalone executable scripts (NEW)
│   ├── check_updates.py     # Batch check updates
│   ├── batch_evolve.py      # Batch align evolution
│   └── validate_all.py      # Batch validate metadata
├── docs/                    # Documentation
│   ├── skill-lifecycle-development-plan.md
│   └── references/
│       └── metadata-spec.md # Metadata specification
├── LICENSE
├── README.md
└── CHANGELOG.md
```

## 🔧 Command Line Tools

This plugin provides standalone Python scripts for CI/CD and batch operations:

```bash
# Check update status for all Skills
python scripts/check_updates.py --summary

# Batch validate Skills metadata
python scripts/validate_all.py --strict

# Batch align evolution.json
python scripts/batch_evolve.py --dry-run
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
