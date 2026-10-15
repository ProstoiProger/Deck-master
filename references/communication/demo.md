# Demo

A hackathon is often decided by the demo. Plan it as a slide, a script and a backup.

## What the demo slide shows

The `demo` layout: one screenshot in a browser frame and up to four numbered callouts that match the live steps.
The slide is the backup when the live demo fails, so the screenshot must show the finished state.

## Choosing the tool

| Tool | Best for |
|---|---|
| Static HTML or a recorded screen video | anything that must not fail on stage |
| Streamlit or Gradio app | data and model demos that run locally |
| Notebook | analysis walkthrough for a datathon jury |
| Command line recording | developer tools |

## Decision-tool pattern

Show the input, the decision and the reason in one screen: a ranked queue, a score, the top three reasons, one action
button. Judges remember a decision they could take.

## Model demo pattern

Pick one real-looking case (synthetic or anonymised), show the input, the prediction with its reason, and what
changes when one input changes.

## Script

| Step | Seconds | Say | Show |
|---|---|---|---|
| Set the scene | 10 | the user and the situation | first screen |
| Do the task | 30 | one action per sentence | the steps in the callouts |
| Show the result | 10 | what the user gained | the final state |

## Reliability

- Run offline, cache every external call, test on the venue machine and screen resolution.
- Record the whole demo as a video and keep it on the desktop and in the PDF as slide images.
- Use anonymised or synthetic data only (`ops/security.md`).
- Have one fallback sentence ready: "The live demo is not loading, here is the recording."
