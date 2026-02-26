# Transferring Expert Knowledge

## The Formula

**Good Skill = Expert Knowledge - What Claude Already Knows**

Every token explaining something Claude already knows is a token you can't use
for actual expert knowledge. Context is a shared, finite resource.

## What Claude Already Knows (DELETE from skills)

- What a PDF/DOCX/CSV/JSON is
- How to open, read, and write files in any language
- Standard library usage (Python, JS, etc.)
- Common design patterns (MVC, Observer, Factory...)
- Basic HTML/CSS/JS concepts
- How REST APIs work
- SQL syntax and common queries
- Git commands and workflows

## What Claude Does NOT Know (KEEP in skills)

- Which tool to pick when multiple options exist (and WHY)
- Domain-specific decision tables with trade-offs
- Edge cases discovered through real-world experience
- The order in which to try solutions when something fails
- Company/project-specific conventions and constraints
- Anti-patterns that aren't in any documentation
- "This looks right but actually breaks because..."
- Performance characteristics under real workloads

## Transferring Mentality, Not Just Procedures

The difference between junior and senior isn't knowing HOW to do things.
It's knowing HOW TO THINK about problems.

### BAD: Mechanical procedure

```markdown
## Steps to create a document
1. Open template file
2. Modify the title
3. Add content
4. Save file
5. Verify it saved correctly
```

This adds nothing. Claude knows how to open and save files.

### GOOD: Thinking framework + specific procedure

```markdown
## Before creating any document, ask yourself:

- **Purpose**: What problem does this document solve? Who will read it?
- **Constraints**: Are there corporate format requirements? Page limits?
- **Differentiation**: What makes this document memorable vs similar ones?

## Specific OOXML workflow (Claude doesn't know this)

1. Decompress .docx (it's a ZIP): `unzip document.docx -d temp/`
2. Locate content at `temp/word/document.xml`
3. Edit XML respecting namespaces (CRITICAL: don't delete xmlns)
4. Validate structure BEFORE repackaging
5. Repackage: `zip -r edited.docx temp/*`
6. Verify by opening in Word (internal validator is stricter)
```

## Three Types of Procedures

1. **Generic**: open, read, write, save. Claude knows them. DELETE.
2. **Domain-specific**: OOXML workflows, validation sequences, critical operation order. KEEP.
3. **Thinking frameworks**: questions to ask before acting. These change the model's approach. KEEP.

## The Token Cost Test

For every paragraph in your skill, calculate:

- **Token cost**: ~4 chars per token, estimate the paragraph size
- **Knowledge value**: Would a senior dev already know this? Then value = 0
- **ROI**: value / cost

If ROI is near zero, delete the paragraph. Aim for every section to contain
at least one insight that would make a competent developer say "I didn't know that."

## Example: Bad vs Good Knowledge Transfer

### BAD: Explaining camelot-py basics

```markdown
## Using camelot-py
Camelot is a Python library for extracting tables from PDFs.
Install it with: pip install camelot-py
Import it with: import camelot
Use camelot.read_pdf() to extract tables.
```

### GOOD: Expert decision matrix

```markdown
## PDF Table Extraction Decisions

| Situation | Primary tool | Fallback | When to fallback |
|-----------|-------------|----------|-----------------|
| Simple text | pdftotext | PyMuPDF | When you need layout info |
| Tables | camelot-py | tabula-py | When camelot fails with borders |
| Scanned PDF | - | Tesseract OCR | Always when pdftotext returns empty |

### Camelot gotchas (not in docs)
- camelot works better with clearly bordered tables
- For borderless tables, use tabula with `stream=True`
- If camelot returns empty DataFrames, check if PDF uses vector lines (lattice)
  vs visual separators (stream) and switch mode accordingly
```
