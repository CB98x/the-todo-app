# Week 3 — Learnings Reference

A reference of the concepts I worked through while adding the email reminder
feature. Written for future-me, so each entry is the idea plus *why it matters*,
not a tutorial.

## Persistence & data

- **Memory vs disk.** Variables live in RAM and vanish when the program ends. A
  file (like `todos.json`) survives. Any change you make in memory is real, but
  it only lasts if you write it back to disk. The next read comes from the file,
  not from RAM — this is the core reason saving matters.
- **The store → render → write-back pattern.** Read data from a store, work with
  it, write it back. Most apps and websites follow this same shape (pull from a
  database, show it, save changes). Worth recognising as a reusable pattern.
- **JSON serialization.** `json.dumps()` turns a Python list/dict into a string
  to write to a file; `json.loads()` turns that string back into Python objects.
  "Serialization" = converting in-memory objects into a storable/transmittable
  form.
- **Relative paths.** `open("todos.json")` resolves relative to *where you ran
  the script from*, not where the script file lives. Running from the wrong
  folder can read/write a different file than you expect (I hit this — two
  `todos.json` files).

## Dates & time

- **`datetime`** = a moment in time (date + time of day). **`timedelta`** = a
  duration (the gap between two moments, or one you build by hand).
- **`strptime(string, "%Y-%m-%d")`** parses a string into a datetime. With no
  time given, it defaults to midnight — which is why I add `timedelta(hours=6)`
  to represent "6am that day."
- Subtracting two datetimes gives a timedelta; `.total_seconds() / 3600` converts
  it to hours.

## Scheduling

- **Self-scheduling loop vs external scheduler.** A self-scheduling loop runs
  forever (`while True` + sleep) and is its own clock — simple, but dies if the
  program crashes. An external scheduler (e.g. cron) runs your script on a
  schedule and survives crashes. I used the loop because it's a personal tool;
  production would use the scheduler.
- **`time.sleep(n)`** hands control to the OS and asks to be woken in `n`
  seconds — it uses ~0% CPU while asleep. Sleep is *relative*, not aligned to the
  clock: `sleep(3600)` means "3600s from now," not "the top of the next hour."
- **The detection window (why 23–25, not exactly 24).** The loop only wakes at
  intervals, so an exact check would miss events that fall between wakes. The
  detection window must be at least as wide as the sleep interval to guarantee
  nothing is missed.

## Email

- **Email is a handoff.** Your code hands the message to a mail server and its job
  ends there; delivery happens later and isn't your code's concern. "No error
  from the server" ≠ "email arrived."
- **SMTP** is the protocol (the agreed back-and-forth) that lets any mail server
  talk to any other. **MIME** is the spec for what a message looks like as text.
  Libraries wrap specs: `smtplib` wraps SMTP, `EmailMessage` builds MIME for you.
- **Ports & SSL.** A port is a number identifying a service on a server
  (`smtp.gmail.com:465`). Gmail requires SSL (encryption) on 465 so the password
  doesn't travel in plain text.
- **App passwords.** Gmail blocks your real password for SMTP. An app password is
  a separate, *revocable, scoped* credential — if it leaks you revoke just that
  one, instead of changing your real password everywhere.

## Secrets & environment variables

- **Environment variables** store config (like secrets) *outside* your code, in
  the OS. Your code asks the OS for the value by name; the value itself never
  lives in the source file.
- **`.env` + `load_dotenv()` + `os.getenv()`.** `.env` is a file holding
  `KEY=value` lines. `load_dotenv()` reads it once and loads the values into the
  OS environment; `os.getenv("KEY")` retrieves them. The *name* lives in code,
  the *value* lives outside.
- **`.gitignore` and permanence.** Add `.env` to `.gitignore` so secrets aren't
  committed. Critical: if a secret is ever committed, it stays in git history
  even after you delete it — prevention beats cleanup. A leaked credential should
  be revoked, not just removed.

## Python mechanics

- **`if __name__ == "__main__":`** Code under this only runs when the file is run
  directly, not when it's imported. Without it, importing a file also runs its
  top-level code (e.g. an infinite menu loop) — which would hang an importer.
- **Module-level vs function-level code.** Module-level runs once at import/start
  (good for `load_dotenv()`, constants, imports). Function-level runs every call.
  Don't re-do one-time setup inside a function.
- **Constants in ALL_CAPS** (e.g. `RECIPIENT`) are a convention meaning "fixed
  config, don't change at runtime." Python doesn't enforce it.
- **`continue`** skips the rest of the current loop iteration and jumps to the
  next item. Everything below it in the loop body is skipped for that one pass.
- **`try`/`except`** controls the *blast radius* of a failure. Without it, one
  error propagates up and kills the whole loop/program. With it, one bad item
  fails alone and the loop continues.
- **`with` blocks (context managers)** guarantee cleanup (close the file, close
  the connection) even if an exception is thrown. Use for any resource that needs
  closing: files, network connections, locks, DB connections.
- **`import` for reuse.** Importing a function (e.g. `get_task_list` from
  `todos.py`) means one source of truth — fix a bug once and it's fixed
  everywhere. Copy-paste means fixing it in two places.
- **References vs copies.** In `for todo in todos:`, `todo` *points at* the real
  dict in the list — it's not a copy. Changing `todo["x"]` changes the list. (I
  proved this with a before/after test instead of guessing.)
- **`dict.get(key, default)` vs `dict[key]`.** `[key]` raises `KeyError` if the
  key is missing. `.get(key, default)` returns the default instead — use it when
  a key might not exist (e.g. `reminder_sent` on older todos).
- **Boolean vs string truthiness.** `False` is falsy. `"False"` (a string) is a
  non-empty string and therefore *truthy* — a classic silent bug. Use real
  booleans for flags.
- **Chained comparison.** `23 <= h <= 25` is valid Python, equivalent to
  `23 <= h and h <= 25`. Most languages don't allow this.
- **`print(..., end="")`** replaces the default newline so the next print
  continues on the same line.

## The duplicate-send fix (the week's hardest lesson)

- The loop re-sent every cycle because the code had **no memory** of what it had
  already sent. Fix: add a `reminder_sent` flag to each todo (starts `False`),
  skip todos where it's `True`, and after a *successful* send set it `True` and
  write the list back to disk.
- **Ordering matters:** set the flag and save *after* the send succeeds, inside
  the `try`. If the send fails, the flag is never set, so it retries next cycle
  instead of being marked done forever.

## Logs vs debug prints

- **Debug prints** answer "why isn't this working *right now*" — temporary,
  deleted after. **Logs** answer "what did this do while I wasn't watching" —
  permanent, with timestamps. Same `print()`, opposite lifespans. Logs are for
  future-you debugging an unattended program.

## Tooling

- **Virtual environments (venv).** An isolated per-project Python + packages, so
  installing a package doesn't pollute other projects. A venv belongs to the OS
  that created it — a Windows venv won't run from WSL and vice versa.
- **Specs (RFCs)** are public documents defining how something works (SMTP, MIME,
  JSON). Libraries are wrappers over specs; understanding the spec makes the
  library stop feeling like magic.
- **Testing a belief.** When unsure whether code behaves as expected, build the
  smallest version of the situation with throwaway data, take a "before"
  snapshot, do the thing, take an "after" snapshot, and compare. This answers
  most "does X actually do Y?" questions without asking anyone.