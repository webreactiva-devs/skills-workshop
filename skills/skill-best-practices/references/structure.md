# Skill Structure and Progressive Loading

## The Three Layers

A skill loads in three stages. Each layer has a token budget:

| Layer | Content | When loaded | Budget |
|-------|---------|-------------|--------|
| 1. Metadata | name + description | Always (for ALL skills) | ~100 tokens |
| 2. Instructions | SKILL.md body | When skill activates | <5000 tokens |
| 3. Resources | references/, scripts/, assets/ | On demand | Unlimited |

Context is a shared resource. Every token your skill uses is a token unavailable
for the conversation, other skills, and the user's request.

## File Organization

### BAD: Everything in one file

```
my-skill/
└── SKILL.md  (800 lines with everything)
```

Forces the agent to load 800 lines every time, even if it only needs a fraction.

### GOOD: Progressive structure

```
my-skill/
├── SKILL.md              (< 500 lines: routing + decisions)
├── references/
│   ├── api-details.md    (detailed technical docs)
│   ├── examples.md       (extensive examples)
│   └── edge-cases.md     (failure modes and solutions)
└── scripts/
    └── process.py        (executable script)
```

## Reference Loading Triggers

Separating files is NOT enough. You must tell the agent WHEN to load each one.

### BAD: References listed without triggers

```markdown
## References
- api-details.md - for API details
- examples.md - for examples
```

The agent doesn't know when to load these. It probably never will.

### GOOD: Triggers integrated into workflow

```markdown
## Create new document

**MANDATORY - READ FULL FILE**: Before continuing, you MUST read
[`references/docx-structure.md`](references/docx-structure.md) (~300 lines).

**DO NOT load** `references/redlining.md` or `references/forms.md` for this task.

## Edit existing document with tracked changes

**MANDATORY**: Read [`references/redlining.md`](references/redlining.md) before
making any modification.
```

Two key elements:

1. **Mandatory triggers**: "You MUST read X before Y"
2. **Negative triggers**: "DO NOT load Z for this task" (prevents loading irrelevant content)

## SKILL.md Content Guidelines

The SKILL.md body should contain:

- **Routing logic**: Which reference to load for which task
- **Critical rules**: Things that apply to ALL uses of the skill (always in context)
- **Decision framework**: How to choose between approaches
- **Quick-reference tables**: Compact summaries of key decisions

The SKILL.md body should NOT contain:

- Detailed API documentation (-> references/)
- Extensive examples (-> references/)
- Long explanations of concepts (-> references/ or delete if Claude knows it)
- Full scripts (-> scripts/)

## Splitting a Large SKILL.md

When a SKILL.md exceeds ~400 lines, identify content to extract:

1. **Tables with >10 rows** -> Move to a reference file, keep summary in SKILL.md
2. **Example sections >50 lines** -> Move to references/examples.md
3. **Domain-specific details** -> One reference file per domain
4. **Troubleshooting guides** -> references/troubleshooting.md

After splitting, add trigger instructions in SKILL.md that tell the agent
exactly when to load each extracted file.

## Avoid Deep Nesting

Keep references one level deep from SKILL.md:

```
# GOOD: flat references
references/
├── api.md
├── examples.md
└── edge-cases.md

# BAD: nested structure
references/
├── api/
│   ├── v1/
│   │   └── endpoints.md
│   └── v2/
│       └── endpoints.md
└── examples/
    ├── basic/
    │   └── ...
    └── advanced/
        └── ...
```

## Long Reference Files

For reference files longer than 100 lines, include a table of contents at the top
so the agent can see the full scope when previewing:

```markdown
# API Reference

## Table of Contents
- [Authentication](#authentication) - Line 10
- [Endpoints](#endpoints) - Line 45
- [Error Codes](#error-codes) - Line 120
- [Rate Limits](#rate-limits) - Line 150
```
