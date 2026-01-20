# Quick Start Guide

## Installation (3 Steps)

### Step 1: Add the Marketplace
```bash
/plugin marketplace add echoleesong/claude-skills-plugin
```

### Step 2: Install the Plugin
```bash
/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin
```

### Step 3: Start Using
The skills will automatically activate when you work on relevant tasks!

## Example Usage

Try these prompts after installation:

```
"Help me build a webhook workflow in n8n"
→ Activates n8n-workflow-patterns skill

"Write JavaScript code to process API data"
→ Activates n8n-code-javascript skill

"Create a new skill for my project"
→ Activates skill-creator skill
```

## Verify Installation

```bash
# List installed plugins
/plugin list

# Check marketplace
/plugin marketplace list
```

## Update Plugin

```bash
# Update to latest version
/plugin update claude-skills-plugin
```

## Troubleshooting

### Plugin not found?
Make sure you've added the marketplace first:
```bash
/plugin marketplace add echoleesong/claude-skills-plugin
```

### Skills not activating?
1. Check if plugin is enabled: `/plugin list`
2. Restart Claude Code
3. Try more specific prompts related to the skill

## Alternative Installation Methods

### Method 1: Direct from GitHub (Recommended)
```bash
/plugin marketplace add echoleesong/claude-skills-plugin
/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin
```

### Method 2: Personal Skills Directory (Highest Priority)
```bash
# Clone and run install script
git clone https://github.com/echoleesong/claude-skills-plugin.git ~/.claude/skills-repo
cd ~/.claude/skills-repo && ./install.sh

# Update later with
cd ~/.claude/skills-repo && git pull && ./install.sh

# Optional: Setup auto-sync on git pull
./setup-hooks.sh
```

### Method 3: Local Development
```bash
git clone https://github.com/echoleesong/claude-skills-plugin.git
/plugin marketplace add ./claude-skills-plugin
/plugin install claude-skills-plugin
```

### Method 4: Temporary Use (No Installation)
```bash
git clone https://github.com/echoleesong/claude-skills-plugin.git
claude --plugin-dir ./claude-skills-plugin
```

## Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/echoleesong/claude-skills-plugin/issues)
- 💬 [Discussions](https://github.com/echoleesong/claude-skills-plugin/discussions)
