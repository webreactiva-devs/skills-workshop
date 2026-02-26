---
name: skill-best-practices
description: >-
  Expert guide for designing, reviewing, and improving AI agent skills.
  Use when creating a new skill, auditing an existing skill for quality,
  refactoring a skill that underperforms, or when the user asks about
  "skill best practices", "how to write a good skill", "improve my skill",
  "skill review", "skill quality", "buenas prácticas skills", "mejorar skill",
  "revisar skill", "skill description tips", "skill anti-patterns".
  Covers: effective descriptions, expert knowledge transfer, anti-pattern lists,
  progressive disclosure, decision trees, freedom calibration, and executable examples.
---

# Skill Best Practices

Expert reference for creating skills that actually get activated and deliver value.
Based on proven patterns from real-world skill design.

## The Golden Rule

**Good Skill = Expert Knowledge - What Claude Already Knows**

Every token must justify its existence. Claude already knows standard libraries,
common patterns, and basic concepts. A skill's job is to transfer the knowledge
that only an experienced practitioner would have: decisions, trade-offs, edge cases,
and anti-patterns.

## Skill Quality Checklist

Before shipping any skill, verify these 10 criteria. For detailed guidance on each,
read the corresponding reference file.

| # | Criterion | Quick Test | Reference |
|---|-----------|-----------|-----------|
| 1 | Description answers QUÉ + CUÁNDO + KEYWORDS | Can you find 3+ trigger phrases? | [descriptions.md](references/descriptions.md) |
| 2 | No basic knowledge explained | Would a junior dev learn from this? If yes, delete it | [expert-knowledge.md](references/expert-knowledge.md) |
| 3 | Transfers expert mentality | Contains "before doing X, ask yourself..." frameworks | [expert-knowledge.md](references/expert-knowledge.md) |
| 4 | Has NUNCA/anti-pattern section | Each anti-pattern has a concrete reason | [anti-patterns.md](references/anti-patterns.md) |
| 5 | Progressive structure (<500 lines) | SKILL.md under 500 lines, extras in references/ | [structure.md](references/structure.md) |
| 6 | Freedom calibrated to fragility | Creative tasks = principles; fragile tasks = exact scripts | [freedom-calibration.md](references/freedom-calibration.md) |
| 7 | Decision trees for multiple paths | No "use the appropriate tool" without criteria | [decision-trees.md](references/decision-trees.md) |
| 8 | Executable examples (no pseudocode) | Every code block runs without modification | Section below |
| 9 | Anticipates common failures | Has "if X fails, do Y" for each critical step | Section below |
| 10 | Correct naming | Lowercase, hyphens only, max 64 chars | Section below |

## Critical Rules (Always in Context)

### Writing the Description

The description is the ONLY thing the agent reads to decide whether to activate a skill.
The body never loads if the description fails. Every description MUST answer:

1. **QUÉ hace** - Concrete verbs: creates, analyzes, converts, validates
2. **CUÁNDO usarlo** - Specific triggers: "when the user asks for...", "when working with..."
3. **PALABRAS CLAVE** - Terms the user would actually type

```yaml
# BAD - invisible to the agent
description: Helps with document tasks

# GOOD - triggers correctly
description: >-
  Create, edit, and analyze .docx files with tracked changes, comments,
  and professional formatting. Use when working with Word documents,
  inserting tables, applying corporate styles, or exporting to PDF.
```

### Expert Knowledge Only

Before writing each section, ask: "Does Claude already know this?"

- Standard library usage -> DELETE
- How to open/read/write files -> DELETE
- Basic programming patterns -> DELETE
- Domain-specific decision tables -> KEEP
- Trade-offs between tools -> KEEP
- Edge cases from real experience -> KEEP
- "NEVER do X because Y" rules -> KEEP

### Anti-Pattern Section is Mandatory

If a skill has no "NEVER do this" section, it's missing half the expert knowledge.
Every anti-pattern MUST include the reason (so the model can generalize):

```markdown
## NEVER

- **NEVER use generic AI fonts** (Inter, Roboto, Arial) -> They reveal automated origin.
  Use fonts with personality: IBM Plex, Source Serif, JetBrains Mono.

- **NEVER combine more than 2 font families** -> Creates visual chaos.
  One for headings, one for body. Maximum.
```

### Executable Examples

Every code block in a skill MUST run without modification. If it can't, it's
disguised pseudocode and will confuse the agent.

```python
# BAD - what is process()? where does save() come from?
result = process(input_file)
save(result)

# GOOD - complete, with imports and error handling
import fitz  # PyMuPDF

def extract_metadata(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    doc.close()
    return {
        "title": metadata.get("title", "Sin titulo"),
        "author": metadata.get("author", "Desconocido"),
        "pages": doc.page_count
    }
```

### Failure Anticipation

For each critical operation, include what happens when it fails:

```markdown
### PDF returns empty text
- **Probable cause**: Scanned PDF (images, not text)
- **Solution**: Apply OCR first with Tesseract
- **Signal**: pdftotext returns empty string but PDF has visible content

### Extracted text has garbled characters
- **Probable cause**: Incorrect encoding or non-standard embedded fonts
- **Solution**: Try backends in order: pdftotext -> PyMuPDF -> OCR on render
```

### Naming Rules

- Lowercase letters, numbers, and hyphens only
- No leading/trailing hyphens, no consecutive hyphens
- Maximum 64 characters
- Name must reflect the skill's purpose

```yaml
# BAD
name: helper           # Too generic
name: MyAwesomeTool    # Uppercase not allowed
name: doc_processor    # Underscores not allowed
name: -pdf-tool        # Leading hyphen

# GOOD
name: pdf-extraction
name: docx-formatting
name: image-optimization
```

## Deep-Dive References

Load these ONLY when working on the specific aspect:

- **Descriptions**: Read [references/descriptions.md](references/descriptions.md) when writing
  or reviewing a skill's frontmatter description
- **Expert knowledge**: Read [references/expert-knowledge.md](references/expert-knowledge.md)
  when deciding what content to include vs. exclude
- **Anti-patterns**: Read [references/anti-patterns.md](references/anti-patterns.md) when
  building NEVER sections or reviewing them for completeness
- **Structure**: Read [references/structure.md](references/structure.md) when organizing
  a skill's file layout or splitting a large SKILL.md
- **Freedom calibration**: Read [references/freedom-calibration.md](references/freedom-calibration.md)
  when deciding how prescriptive vs. flexible instructions should be
- **Decision trees**: Read [references/decision-trees.md](references/decision-trees.md) when
  a skill handles multiple paths or tool choices

**DO NOT load all references at once.** Pick only the one relevant to the current task.
