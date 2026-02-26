# Writing Effective Skill Descriptions

The description is the gate. If it's locked with no sign, nobody will knock.

## How Skill Activation Works

The agent has access to dozens or hundreds of skills. When it receives a user request,
it reads ONLY the descriptions to decide which skill to activate. The skill body never
loads until the decision is already made.

This means a perfect skill with a vague description will NEVER activate.

## The Three Required Elements

Every description must answer:

### 1. QUÉ hace (What it does)
Use concrete action verbs. Not "helps with" or "useful for" but specific operations.

```yaml
# BAD: what documents? what tasks?
description: Helps with document tasks

# GOOD: concrete actions
description: Create, edit, and analyze .docx files with tracked changes and comments
```

### 2. CUÁNDO usarlo (When to use it)
Explicit triggers that match user language patterns.

```yaml
# BAD: no activation context
description: Processes PDF files

# GOOD: clear triggers
description: >-
  ...Use when the user mentions PDFs, data extraction,
  form filling, or document merging.
```

### 3. PALABRAS CLAVE (Keywords)
Terms the user would actually type. The agent does keyword matching between
the user's request and skill descriptions.

If a user says "make me a report in Word", the agent looks for skills mentioning
"Word" or ".docx". Without those keywords, the skill is invisible.

## Common Description Failures

```yaml
# Too generic - could be anything
description: A useful skill for various tasks

# Only says what, not when
description: Processes PDF files

# Uses internal jargon the model doesn't understand
description: Manages the Q3 reports workflow

# Too short - insufficient trigger surface
description: Excel helper
```

## Corrected Versions

```yaml
# Specific with triggers
description: >-
  Extract text and tables from PDF files, fill forms, and merge
  multiple documents. Use when the user mentions PDFs, data extraction,
  or document merging.

# Includes concrete scenarios
description: >-
  Generate presentations in .pptx format with professional design.
  Activate when the user asks to create slides, presentations,
  pitch decks, or meeting materials.

# Rich trigger surface
description: >-
  Create and edit Excel spreadsheets (.xlsx) with formulas, charts,
  pivot tables, and conditional formatting. Use when working with
  spreadsheets, financial data, CSV-to-Excel conversion, or any
  tabular data analysis task.
```

## Description Length Guidelines

- **Minimum**: 30 words (enough for QUÉ + CUÁNDO + keywords)
- **Ideal**: 40-80 words
- **Maximum**: ~150 words (beyond this, signal-to-noise drops)

## Bilingual Trigger Strategy

If your users work in multiple languages, include trigger terms in both:

```yaml
description: >-
  ...Use when the user asks for "security review", "security audit",
  "revisar seguridad", "auditar seguridad", or "vulnerability scan".
```

## Testing Your Description

Mental test: for each of these user requests, would the agent pick your skill?

1. Write 5 realistic user prompts that SHOULD trigger your skill
2. Write 3 prompts that should NOT trigger it
3. Check if the description contains matching keywords for group 1
4. Check if the description is specific enough to exclude group 2
