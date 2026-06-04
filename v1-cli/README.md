# v1 — CLI Todo App

A terminal-based todo app written in Python. Add, list, mark done, delete, quit. Persists to `todos.json` between runs.

## What it does

- `1. Add` — title and due date, saved immediately
- `2. List` — show all todos with status
- `3. Delete` — pick a numbered todo to remove
- `4. Mark done` — pick a numbered todo to mark complete
- `5. Quit`

## Run it

\`\`\`bash
python todo.py
\`\`\`

`todos.json` is created automatically on first add.

## What I learned building it

- Lists vs dicts (and using a list of dicts)
- JSON serialization — files hold text, not objects
- `try/except` for FileNotFoundError, ValueError, JSONDecodeError
- Validating at the edges, not downstream
- The difference between crash bugs and silent bugs (the off-by-one in delete was the latter)
- Why saving on every change is more robust than saving on quit
- Read-modify-write race conditions (single-user app so not fixed here, but understood)

Built without AI code generation — Claude acted as tutor only, explaining concepts with non-todo examples and pointing at bugs without fixing them. This was the discipline of the week.
