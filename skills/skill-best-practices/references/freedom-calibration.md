# Calibrating Freedom to Task Fragility

## The Rule

The more severe the error, the less freedom the model should have.

Not all tasks need the same level of detail. A creative task benefits from
broad principles. A fragile technical task needs exact steps.

## The Spectrum

```
HIGH FREEDOM                                              LOW FREEDOM
(principles + anti-patterns)                    (exact scripts + verification)
     |                                                        |
  Creative     Analytical     Transformative     Fragile/Critical
  tasks        tasks          tasks              tasks
```

## BAD: Freedom Miscalibrated

### Too rigid for a creative task:

```markdown
## Interface Design

1. Open Figma
2. Create a 1920x1080 frame
3. Add a 200x50 rectangle for the button
4. Use color #3B82F6 for the background
5. Add centered "Submit" text
```

No room for differentiation. Every output will be identical and generic.

### Too loose for a fragile task:

```markdown
## XLSX File Editing

Modify cells as needed. Be careful with formats.
```

One wrong move corrupts the entire file. This gives no guardrails.

## GOOD: Freedom Correctly Calibrated

### Creative task (HIGH freedom):

```markdown
## Interface Design

Commit to a BOLD aesthetic direction. Pick an extreme:
brutal minimalism, maximalist chaos, retro-futuristic, organic natural...

Principles to maintain:
- Clear visual hierarchy (what the user sees first)
- Sufficient contrast for readability
- Internal consistency (if you start rounded, stay rounded)

NEVER: Generic design that could belong to any SaaS website.
```

### Fragile task (LOW freedom):

```markdown
## XLSX File Editing

**USE EXACTLY this script**: `scripts/edit-xlsx.py`

Mandatory parameters:
- `--input`: original file
- `--output`: destination file (NEVER overwrite the original)
- `--changes`: JSON with modifications

**NEVER modify the script.** If you need additional functionality,
create a new script based on this one.

After each edit:
1. Open file in Excel/LibreCalc
2. Verify formulas recalculate
3. Check for #REF! or #VALUE! errors
```

## Decision Matrix

| Task Type | Freedom Level | What to Provide | Example |
|-----------|--------------|-----------------|---------|
| Creative (design, copy, naming) | High | Principles + anti-patterns + aesthetic direction | UI design, brand voice |
| Analytical (research, review) | Medium-High | Framework of questions + evaluation criteria | Code review, data analysis |
| Transformative (convert, migrate) | Medium | Preferred approach + fallback options | File conversion, data migration |
| Fragile (binary formats, DBs) | Low | Exact scripts + mandatory verification | XLSX editing, DB migrations |
| Critical (payments, auth, data) | Very Low | Locked scripts + multi-step verification + rollback plan | Payment processing, auth flows |

## Signals That Freedom Is Wrong

### Too much freedom (task needs more guardrails):
- Output varies wildly between runs for the same input
- Silent data corruption or format errors
- Model "invents" approaches that don't work

### Too little freedom (task is over-constrained):
- All outputs look identical and generic
- Model can't adapt to slight variations in input
- Creative tasks produce uninspired results

## Mixing Freedom Levels

A single skill often contains tasks at different freedom levels.
Apply freedom calibration per-section, not per-skill:

```markdown
## Choose Visual Direction (HIGH freedom)
Pick a bold aesthetic. Principles: hierarchy, contrast, consistency.

## Generate HTML/CSS (MEDIUM freedom)
Follow the chosen direction. Use semantic HTML. Prefer CSS Grid for layout.

## Export Final Assets (LOW freedom)
USE EXACTLY: `scripts/export.sh --format webp --quality 85`
Verify all files exist and are non-zero size.
```
