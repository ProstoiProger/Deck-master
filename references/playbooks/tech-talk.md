# Playbook: tech talk

**Preconditions**: peers will learn a method, tool or system; 15 to 40 minutes; no scoring rubric but a clear takeaway.

## Steps

1. **Takeaway**: one sentence a listener can use on Monday.
2. **Audience level**: what they already know; decide the starting slide accordingly.
3. **Structure**: problem, the naive approach and why it fails, the idea, how it works, a worked example, limits,
   what to do next.
4. **Code on slides**: at most 10 lines, 18 pt or larger, only the lines that matter; link to the repo for the rest.
   Use a `bullets` slide with a fenced code block (shown in mono on the right with its line breaks and
   indentation kept; lines are never wrapped, the font shrinks instead) or a screenshot of the highlighted lines.
5. **Diagrams**: `architecture` and `pipeline` layouts; one idea each.
6. **Live parts**: a recording as backup; run in a clean environment beforehand.
7. **Scaffold**: `new --event tech-talk` for the shape; set `minutes` to the slot length; theme `terminal-slate`
   or `graphite-cyan`.
8. **QA**: lint, previews, timed read-through, check the code font size from the back of the room.

## Traps

Slides of code nobody can read; starting with history; no worked example; no takeaway.

## Output

Deck source, `.pptx`, `.pdf`, speaker script, link list for the audience.
