---
name: git-undo
description: >
  Interactive guide to undo Git changes using a decision tree.
  Automatically analyzes repository state (git status, git log) and recommends
  the exact command based on the situation. Asks for confirmation before
  executing destructive commands.
  Use when: user says "undo git", "git undo", "deshacer git", "revert changes",
  "undo changes", "undo commit", "unstage files", "discard changes",
  "undo last commit", "revert changes", "deshacer cambios", "revertir cambios",
  "quitar del staging", "descartar cambios", or invokes /git-undo.
---

# Git Undo

Interactive guide to undo Git operations.

## Decision tree

```
Are changes staged (git add)?
├── NO → Discard ALL?
│   ├── YES → git checkout -- . && git clean -fd
│   └── NO → Is it a new file (untracked)?
│       ├── YES → rm <file>
│       └── NO → git checkout -- <file>
└── YES → Already committed?
    ├── NO → Just unstage or discard entirely?
    │   ├── Unstage only → git reset HEAD <file>
    │   └── Discard → git reset HEAD <file> && git checkout -- <file>
    └── YES → Already pushed?
        ├── NO → git reset --soft HEAD~1
        └── YES → git revert HEAD
```

## Procedure

1. Run `git status` and `git log --oneline -5` to diagnose current state
2. Classify detected changes according to the decision tree
3. Show the user the diagnosis: what changes exist, their state, and which tree branch applies
4. Recommend the exact command with the specific files involved
5. **Ask for explicit confirmation** before executing any destructive command (`checkout`, `clean`, `reset`, `rm`, `revert`)
6. Execute only after user confirmation

## Rules

- Never execute destructive commands without confirmation
- If there is a mix of states (some files staged, others not), diagnose each group separately
- Briefly explain what the command will do before asking for confirmation
- If the user asks to undo a specific file, operate only on that file
- If the user does not specify, show the full picture and ask what they want to undo
