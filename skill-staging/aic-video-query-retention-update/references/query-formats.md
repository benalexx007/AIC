# AIC query formats

Use this reference only when composing or validating the final query.

## Textual KIS

- Query: a natural-language description of one distinctive event.
- Ground truth: `<video_id>, <frame_id>`.
- Choose a frame inside the described event, not an establishing shot before it.
- Mention enough visible context to make the event identifiable without leaking the ID or timestamp.
- In this skill's interval export, expand the point ground truth to the complete continuous span in which the whole description remains visibly true. A clear representative core is not the interval when the same action continues before or after it.

## Q&A

- Query: an event description plus one unambiguous question about that event.
- Ground truth: `<video_id>, <frame_id>, <answer>`.
- The answer may come from visible action, readable text, counted objects/people, or clearly aligned speech.
- Reject questions whose answer changes across adjacent frames, is occluded, or depends on unsupported inference.
- The exported interval covers the complete continuous answer-bearing event, bounded by the nearest frames where the event or stable answer is no longer valid.

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
3. Verify temporal coverage with a negative frame immediately before the start and immediately after the end. Expand again if the action touches either inspected edge.
4. Search the full video for alternate intervals satisfying the same essential predicates. The final query must resolve to exactly one temporal cluster, not merely one clear keyframe.
5. Count teasers, recaps, replays, repeated edits, and a later full occurrence as duplicates when each independently satisfies the query. Visual identity is not required; semantic equivalence is enough.
6. For Q&A, test uniqueness on the complete event description plus the question-answer relation. A repeated answer alone is not a duplicate, but another interval supporting the same context, question, and answer is.
7. A visible target-only discriminator may make a repeated event unique. Reject positional wording such as “đoạn đầu”, “lần đầu”, or timestamps, and reject metadata unavailable from the video content.
8. Keep Vietnamese natural and concise. Preserve proper names exactly when OCR/transcript confidence is high.
9. If evidence is ambiguous, lower confidence or choose a different event; do not fabricate precision.

## Export contract

- Write exactly one query to `D:\AIC\test\query\query-{n}-{type}.txt`; include no heading, ID, answer, or explanation.
- Write the ground truth to `D:\AIC\test\answer\ans-{n}-{type}.txt` in contestant-submission order, replacing each point frame with `[start_frame_id, end_frame_id]`.
- Write the complete record to `D:\AIC\test\yaml\result-{n}-{type}.yaml` and preserve it after returning the same YAML in chat.
- After all three final files are verified, delete only the source video downloaded from Google Drive under `D:\AIC\video-runs`. Preserve the query, answer, YAML, transcript, frames, and other evidence. Never delete a local input. Record cleanup status, deleted byte count, exact source path, and recoverability in YAML before showing it in chat.
- For KIS use `<video_id>, [s, e]`.
- For Q&A use `<video_id>, [s, e], <answer>`.
- For TRAKE use `<video_id>, [s1, e1], ..., [sn, en]`.
- Each `[s, e]` is the full verified semantic event span, not merely a narrow acceptance window around the most representative frame.
