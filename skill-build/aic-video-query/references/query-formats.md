# AIC query formats

Use this reference only when composing or validating the final query.

## Textual KIS

- Query: a natural-language description of one distinctive event.
- Ground truth: `<video_id>, <frame_id>`.
- Choose a frame inside the described event, not an establishing shot before it.
- Mention enough visible context to make the event identifiable without leaking the ID or timestamp.

## Q&A

- Query: an event description plus one unambiguous question about that event.
- Ground truth: `<video_id>, <frame_id>, <answer>`.
- The answer may come from visible action, readable text, counted objects/people, or clearly aligned speech.
- Reject questions whose answer changes across adjacent frames, is occluded, or depends on unsupported inference.

## TRAKE

- Query: one video containing an ordered sequence of semantic events.
- Ground truth: `<video_id>, <frame_id_1>, ..., <frame_id_n>`.
- Prefer 3-5 events forming one coherent action.
- Define each event operationally: first contact, first full separation, peak position, first landing, first completed state, and similar observable transitions.
- Inspect every frame in a dense window. A semantic keyframe is not an encoded I-frame.
- When producing benchmark metadata, record a representative frame and an optional acceptance interval no wider than the visually defensible moment (usually under 10 frames).

## Quality checks

1. Verify zero-based frame IDs against extracted files and the source FPS.
2. Ground every noun, count, color, order, and spoken fact in evidence.
3. Avoid generic events repeated throughout the video unless the surrounding context uniquely identifies them.
4. Keep Vietnamese natural and concise. Preserve proper names exactly when OCR/transcript confidence is high.
5. If evidence is ambiguous, lower confidence or choose a different event; do not fabricate precision.

## Export contract

- Write exactly one query to `D:\AIC\test\query\query-{n}-{type}.txt`; include no heading, ID, answer, or explanation.
- Write the ground truth to `D:\AIC\test\answer\ans-{n}-{type}.txt` in contestant-submission order, replacing each point frame with `[start_frame_id, end_frame_id]`.
- Write the complete record to `D:\AIC\test\yaml\result-{n}-{type}.yaml` and preserve it after returning the same YAML in chat.
- After all three final files are verified, delete only the source video downloaded from Google Drive under `D:\AIC\video-runs`. Preserve the query, answer, YAML, transcript, frames, and other evidence. Never delete a local input. Record cleanup status, deleted byte count, exact source path, and recoverability in YAML before showing it in chat.
- For KIS use `<video_id>, [s, e]`.
- For Q&A use `<video_id>, [s, e], <answer>`.
- For TRAKE use `<video_id>, [s1, e1], ..., [sn, en]`.
