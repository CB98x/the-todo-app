# Week 2 Learnings — CLI Todo App

What I built, what broke, and what I learned along the way.

---

## The project

A command-line todo app in Python. Add, list, mark done, delete, quit. Persists to `todos.json` between runs. Built by hand, with AI as a tutor only — no code generation.

---

## Concepts I now actually understand

### Data structures: list vs dict

- **List**: when you want to store multiple values of the same kind. Ordered. Accessed by position (`task_list[0]`).
- **Dict**: when you need `key: value` pairs. Accessed by key (`task['title']`).
- My todos are a **list of dicts** — list as the container, dict for each todo. The container shape and the item shape are independent choices.

### Indexing and off-by-one

- Python is 0-indexed. Users think 1-indexed.
- Every time you cross that boundary, you write `-1` or `+1`. Forgetting is the classic off-by-one bug.
- `range(1, len(task_list)+1)` gives valid 1-indexed positions for the user.

### Functions and scope

- Calling a function pauses the caller. The function runs. When it returns, the caller resumes from where it left off.
- Variables inside a function (`task_title`, `task_dict`) are **local** — they exist only while the function runs and are erased when it exits.
- Nested calls stack up. `while` calls `on_add_task` which calls `get_task_list` — three things paused waiting on the innermost one. This is the **call stack**.
- `return` does two things: ends the function AND hands a value back.

### Files and serialization

- **Files can only store text/bytes.** They cannot store a Python list directly. A Python list is a runtime object that exists in memory; the disk has no concept of it.
- To bridge memory ↔ disk, you need a **format**: rules for turning objects into text and back.
- `json.dumps()` = Python object → JSON string (serialize / encode).
- `json.loads()` = JSON string → Python object (deserialize / decode).
- JSON `[...]` becomes a Python list. JSON `{...}` becomes a dict. JSON `"text"` becomes a string. Etc.
- This same pattern (serialize-write-read-deserialize) is what every API call, database write, save file, and cookie does.

### `with open(...) as f`

- `with` is a context manager, not a loop.
- It auto-closes the file when the block exits, even if an error happens inside.
- Cleaner than manually calling `f.close()` and forgetting to.

### Error handling: try / except

- `try` runs the risky code. If it raises an exception, the matching `except` runs instead of crashing.
- You can stack multiple `except` clauses for different error types.
- You can also combine them: `except (FileNotFoundError, json.JSONDecodeError):` handles both with one branch.
- Catch the **specific** exception (`ValueError`, `FileNotFoundError`), not a generic `except:` — generic catches hide bugs you didn't plan for.

### EAFP vs LBYL

- **LBYL** (Look Before You Leap): check if it's valid, then do it. `if s.isdigit(): int(s)`.
- **EAFP** (Easier to Ask Forgiveness than Permission): just try it, handle the failure. `try: int(s) except ValueError: ...`.
- Python culture prefers EAFP. LBYL can have race conditions — the world can change between "is it valid?" and "now use it."
- For converting input I picked EAFP because it fails right at the boundary where bad data enters.

### Validate at the edges

- Catch bad input **at the line where it enters the program**, not three lines later.
- A range check downstream of `int(input(...))` doesn't help if `int(...)` itself crashes on bad input.
- The check must come after the line that could fail OR the bad value never gets that far.

---

## The bugs I fixed (and what each taught me)

### 1. IndexError on out-of-range task number
- **Cause**: I used the user's number as an index without checking if it was in range.
- **Fix**: range check before using the index.
- **Lesson**: Python won't second-guess your indices. *Your* job to validate.

### 2. ValueError when user types letters into an int input
- **Cause**: `int("abc")` crashes immediately. My range check never even ran.
- **Fix**: `try/except ValueError` around the `int(input(...))` line.
- **Lesson**: A check can only protect you if execution actually reaches it. Validate at the boundary, not downstream.

### 3. JSONDecodeError on empty file
- **Cause**: `json.loads("")` fails — an empty string isn't valid JSON. Different from "file doesn't exist."
- **Fix**: second `except json.JSONDecodeError` clause returning `[]`.
- **Lesson**: "File missing" and "file empty" look identical to the user but Python sees them as completely different errors. Both need handling.

### 4. Off-by-one in delete (silent bug — the scariest kind)
- **Cause**: I had two lines next to each other that both needed `-1`, but only one had it. The program deleted the right task but reported the wrong title.
- **Fix**: keep the index logic consistent across all lines that use it.
- **Lesson**: This is the most dangerous category of bug — code that runs without crashing but produces wrong output. A test like "did the file change?" would pass. Only checking the printed output catches this.

> **Wrong output that looks plausible is worse than a crash.** A crash tells you something is wrong. A lie just propagates.

---

## Concepts I discovered through the tutor's questions

### Save on every change vs save on quit

I happened to write to the file on every change. Turns out that's the **more robust** design — if the program crashes mid-session, no data is lost. The alternative (keep everything in memory, save on quit) loses everything on a crash. Slower, simpler, safer.

### In-memory vs persistent

- **Memory** = scratch paper that gets thrown out when the program ends.
- **File** = the notebook that survives.
- Without `todos.json`, the app would still *work* — but every restart would wipe all data.
- This is the same problem every database, save file, and "remember me" checkbox solves at a bigger scale.

### Race conditions / lost updates

If two people run the app at the same time pointing at the same file:
1. User A reads file (`[]`), starts typing.
2. User B reads file (`[]`), adds "buy milk", writes.
3. User A finishes typing "call mom", appends to *their stale copy* (still `[]`), writes.
4. Result: "buy milk" is **gone**.

This pattern is called a **lost update** (or "last writer wins"). It's a special case of a **race condition**: bugs that depend on the timing between two things.

**Read-modify-write across a gap = data loss waiting to happen.**

Fix at small scale: file locking. At big scale: database transactions, distributed consensus.

Not a real problem for my single-user todo app, but the *shape* of the bug shows up everywhere — two CI jobs deploying at once, two pods updating the same config, two requests writing the same row.

### DRY — Don't Repeat Yourself

`delete_todo` and `mark_todo_done` have the same shape: show numbered list → ask for choice → validate → do the thing. That's a signal to extract a shared helper (`pick_task` or similar). Not just for shorter code — because if I want to change the displayed format later, I want to change it in **one place**, not two.

**Noticing duplication is the precondition for refactoring.**

---

## The meta-lesson: build in layers

The way we built this app:

0. Spec (what does it do)
1. Scaffold (skeleton that runs)
2. Happy path, feature by feature
3. Persistence
4. Edge cases / defensive coding
5. Silent-failure hunt
6. Refactor for clarity
7. Hardening (concurrency, security, performance)
8. Tests

Each layer is reviewable. Skipping ahead means you end up with code you can't decompose.

For prompting AI better: ask for one layer at a time. "Build the scaffold." Then "add feature X, happy path only." Then "make X robust against these cases." Doing it layer by layer means at every step I understand what I have and can review the next chunk meaningfully.

**Build in layers so you can review in layers.**

---

## What I now know about myself as a coder

- I would have missed every one of these bugs if AI had written the code in one shot. I said this out loud — "I'd ask AI for an answer, check if it makes sense. I will likely miss stuff."
- The point of this week wasn't the todo app. It was building the **review reflex** — the instinct to stop and ask "what could break here?" before AI-written code looks done.
- I have decent instincts (reached for "thread locking" unprompted, spotted DRY duplication unprompted, picked EAFP for the right reason). I just need to slow down enough to use them.
- My typing is messy. My thinking is sharp. The bottleneck is patience with reviewing AI output, not capability.

---

## Carrying into Week 3 and beyond

- When AI gives me code, **trust the "wait, that doesn't feel right" instinct.**
- Ask "what could silently fail here?" not just "does it run?"
- Build in layers, review in layers.
- A test that only checks "did it work" misses silent bugs. Tests need to check the *output*, not just the *outcome*.
- For DevOps/FAANG-scale work later: race conditions, concurrency, locking, observability — these aren't fancy add-ons. They're the difference between "works on my laptop" and "works for a million users."