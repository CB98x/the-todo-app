# Week 3 Prompts

The artifact of this week: the prompts I sent while building the email reminder
feature, plus what I learned about *how* I prompted.

---

## Prompt 1 — The starter prompt with the 5 hard rules

```
I'm in Week 3 of my SWE curriculum. In Week 2 I built a CLI todo app by hand.
Now I want to add a feature WITH your help: send me an email reminder 24 hours
before a todo is due.

Here's what I want to learn this week, in this order:
1. How to prompt you well for code that fits my existing app
2. How to read code you give me without just copy-pasting blindly
3. How email sending works in Python (concepts before code)
4. How "scheduled" code works — something that wakes up periodically and
   checks if there's work to do

Hard rules:
1. Before you write any code, explain the CONCEPT first. I shouldn't see
   smtplib or any library name until I understand what SMTP is at a
   conceptual level.
2. When you write code, write it in small chunks (10-20 lines max). After each
   chunk, ask me to read it line by line and explain it back to you. Don't move
   on until I've done that.
3. If I miss something in my explanation, point it out. Don't be polite.
4. Use the "Do Not" pattern in your suggestions: tell me what NOT to do and
   why, not just what to do.
5. Never put a real password or API key in code. Teach me about environment
   variables the first time we need one.

Here is my current todo app: [pasted my Week 2 todos.py]

Start by helping me write a small spec for this feature — just 5 bullet points —
so we know what we're building before we build it. Make me write the bullets;
you critique them.
```

- **What worked:** Stating the five hard rules up front changed the kind of answer I got — Claude explained SMTP as a concept before showing me any library, so I understood what the code was doing instead of just pasting it. Pasting my actual todos.py (not describing it) meant the new code fit my real functions instead of inventing new ones.
- **What was unclear / what I'd change:** It was a lot of rules at once and I didn't always enforce them — a few times I let Claude move faster than "explain it back first." Next time I'd add a rule about me having to summarize before moving on, not just Claude.

---

## Prompt 2 — Cutting scope so the feature was actually deliverable

```
i'd rather not bloat the scope - it affects delivery - so we'll skip past due,
missing/unparsable dates for now
```

- **What worked:** When deciding the exact scope of the logic for the feature, I had a lot of back and forth about handling edge cases and which features fell in the scope of the task. Clearly stating the out-of-scope components made it easier to focus on the exact definition of done.
- **What was unclear / what I'd change:** I had a lot of items I wanted to include in the scope initially, so it took a long time to let go of them. Next time I'd like to do that part much quicker — letting go of delivering the best possible product in favour of an actual on-time delivery.

---

## Prompt 3 — Asking to be guided through a test instead of being handed the answer

```
100% guess, i think the todo in todos is a copy - don't tell me the answer -
i can't think how to test, guide me to do that
```

- **What worked:** I was hesitant to run the final code because I wasn't confident in my debugging skills, but instead of giving me the answer Claude guided me to design a small isolated test (a before/after snapshot on a throwaway list) and run it myself. Proving the answer with my own test made me more confident, and I now have a better idea of how to go about checking things.
- **What was unclear / what I'd change:** Initially I had no idea there would be so many errors that needed to be handled — error handling was almost 50% of the whole week's work, so next time I'd factor that into my time estimate.