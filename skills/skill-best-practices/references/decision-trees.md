# Decision Trees for Multiple Paths

## Why Decision Trees Matter

When a task has multiple valid paths, "use the appropriate tool" is useless.
The model needs explicit criteria to choose. A decision tree eliminates ambiguity
by turning vague guidance into concrete if/then logic.

## BAD: Vague Guidance

```markdown
## Image Processing

Use the most appropriate tool for each case. Consider the input format
and desired output.
```

The model has to guess. Results will be inconsistent.

## GOOD: Explicit Decision Tree

```
Is the image vectorial (SVG)?
├── YES -> Use Inkscape CLI for transformations
│   `inkscape --export-type=png input.svg`
└── NO -> Need to preserve transparency?
    ├── YES -> Use PNG as intermediate format
    │   ImageMagick: `convert input.jpg -alpha set output.png`
    └── NO -> Is it photography or illustration?
        ├── Photography -> JPEG with quality 85
        │   `convert input.png -quality 85 output.jpg`
        └── Illustration -> PNG-8 with reduced palette
            `pngquant --quality=65-80 input.png`
```

## Decision Tree Formats

### ASCII Tree (best for complex branching)

Use for decisions with 3+ levels of nesting. The visual structure
makes the logic immediately clear.

### Table with Conditions (best for tool selection)

```markdown
| Situation | Primary Tool | Fallback | Signal to Switch |
|-----------|-------------|----------|-----------------|
| Resize | ImageMagick | PIL/Pillow | ImageMagick not installed |
| Compress PNG | pngquant | optipng | pngquant produces artifacts |
| Convert to WebP | cwebp | ImageMagick | cwebp doesn't support animation |
```

### Numbered Conditions (best for sequential checks)

```markdown
## Choose Database Migration Strategy

1. If migration is additive only (new columns, new tables): -> Online migration, no downtime
2. If migration modifies existing columns: -> Check row count
   - < 1M rows: -> Online ALTER, monitor lock wait
   - > 1M rows: -> pt-online-schema-change or gh-ost
3. If migration deletes columns: -> Deploy code changes first (stop reading column),
   then migrate in next release
4. If migration changes primary key: -> STOP. Manual review required. Never automate this.
```

### Flowchart in Markdown (best for documentation-heavy skills)

```markdown
## Request Handling Flow

**Step 1**: Check authentication
- Authenticated? -> Continue to Step 2
- Not authenticated? -> Return 401, STOP

**Step 2**: Validate input
- Valid? -> Continue to Step 3
- Invalid? -> Return 400 with specific error message, STOP

**Step 3**: Check rate limit
- Under limit? -> Process request
- Over limit? -> Return 429 with Retry-After header, STOP
```

## Building Effective Decision Trees

### 1. Identify the Decision Points
List every point where the task could go in different directions.
Common decision points: file format, file size, error conditions,
user preferences, environment capabilities.

### 2. Define Observable Criteria
Each branch must be decided by something the model can actually check.

```markdown
# BAD: subjective criterion
"If the image quality is good enough..."

# GOOD: observable criterion
"If the image resolution is >= 300 DPI..."
```

### 3. Include Fallback Chains
For every primary path, define what to do when it fails:

```markdown
## Text Extraction Priority

1. Try pdftotext (fastest)
   - If output is empty -> Go to 2
   - If output has garbled chars -> Go to 3
2. Try PyMuPDF (better font handling)
   - If output is empty -> Go to 3
3. Render to image + OCR with Tesseract (last resort)
   - If OCR fails -> Report to user: "PDF may be encrypted or corrupted"
```

### 4. Mark Dead Ends Clearly
When a path should STOP and not continue:

```markdown
- If file is encrypted and no password available:
  -> STOP. Inform user. Do NOT attempt to crack or bypass.
```

## Common Mistakes in Decision Trees

- **Missing branches**: Every decision must have ALL possible outcomes covered
- **Overlapping conditions**: Each input should match exactly ONE branch
- **No fallbacks**: Every tool/approach must have a "what if this fails" path
- **Subjective criteria**: "If it looks right" is not a valid criterion.
  Use measurable, checkable conditions
