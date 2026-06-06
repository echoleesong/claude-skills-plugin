# Markdown Format Reference

The parser uses standard Markdown with intelligent slide detection.

## Example Structure

```markdown
# Presentation Title

Subtitle text here

## Slide Title

Content for this slide.

- Bullet point 1
- Bullet point 2

> This is a speaker note - it will appear in the PPT notes section, not on the slide.

## Another Slide

1. Numbered item
2. Another item

### Sub-heading (stays on same slide)

More content...
```

## Slide Detection Rules

- `# H1` - Creates title slide (centered layout)
- `## H2` - Creates new content slide
- `### H3` and below - Stays on current slide as sub-heading
- Content between headings goes on the same slide
- **Do NOT use `---` between slides** - slides are separated by `#` or `##` headings only. `---` horizontal rules are ignored.

## Speaker Notes

Lines starting with `> ` are treated as **speaker notes** and placed in the PPT notes section (not visible on the slide):

```markdown
## My Slide

Some content here.

> This is the speaker note for this slide.
> It supports multiple lines.
> Each line starting with "> " is appended to the note.
```

## Supported Elements

| Element | Support | Notes |
|---------|---------|-------|
| Headings | Full | H1/H2 create slides, H3+ are content |
| Paragraphs | Full | Auto-wrapped text |
| Bullet lists | Full | Nested supported |
| Numbered lists | Full | Nested supported |
| Code blocks | Basic | Monospace font, background color |
| Tables | Full | Converts to native PPT tables |
| Images | Full | Supports position control via metadata |
| Charts | Auto | Tables with numeric data can become charts |

## Image Position Control

Basic usage (placed in content flow):
```markdown
![alt text](./images/diagram.png)
```

With position preset:
```markdown
![Framework](./images/framework.png){position=center}
![Detail](./images/detail.png){position=top-right, width=40%}
```

### Position Presets

| Preset | Location |
|--------|----------|
| `top-left` | Upper-left corner |
| `top-center` | Top-center |
| `top-right` | Upper-right corner |
| `center-left` | Middle-left |
| `center` | Exact center of slide |
| `center-right` | Middle-right |
| `bottom-left` | Lower-left corner |
| `bottom-center` | Bottom-center |
| `bottom-right` | Lower-right corner |

### Size Control

```markdown
![img](path){position=center, width=50%}        # 50% of slide width
![img](path){position=center, width=3in}         # 3 inches wide
![img](path){position=center, height=2in}        # 2 inches tall
![img](path){position=center, width=50%, height=3in}  # both
```

### Custom Coordinates

```markdown
![img](path){x=1in, y=2in, width=4in}
```

### Examples

```markdown
## Architecture Overview

Main architecture diagram:

![Architecture](./images/arch.png){position=center, width=70%}

> This slide shows the overall framework architecture.

## Results Comparison

![Results](./images/results.png){position=top-right, width=45%}

Key findings:
- Finding 1
- Finding 2
```

## Image Handling

Only local file paths are supported:
```markdown
![Description](./images/diagram.png)
![](../assets/photo.jpg)
```

Network URLs and base64 images are skipped with a warning.

## Layout Selection

The generator automatically selects layouts based on content:

| Content Type | Layout |
|--------------|--------|
| H1 only | Title slide (centered) |
| Text + bullets | Content slide |
| Many elements (>4) | Two-column |
| Image present | Image-focused |
| Table with numbers | Chart slide |
