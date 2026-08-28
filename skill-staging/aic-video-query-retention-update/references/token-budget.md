# Token budget for 15-20 minute videos

## Baseline

At 25 fps:

- 15 minutes = `15 * 60 * 25 = 22,500` frames.
- 20 minutes = `20 * 60 * 25 = 30,000` frames.

Do not send every frame. A 960x540 frame at GPT-5.6 `original` detail is approximately:

`ceil(960/32) * ceil(540/32) = 30 * 17 = 510` image tokens.

All frames would therefore require about 11.5M-15.3M image tokens before text or reasoning. This exceeds the model context many times.

## Semantic-first hierarchy

OpenCLIP embedding, YOLO detection, motion scoring, and clustering run locally and therefore add zero GPT model-input tokens. Their JSON metadata is also free until the model reads it. Use them to select a small number of actual evidence frames.

Contact sheets are 1280x720 and cost approximately:

`ceil(1280/32) * ceil(720/32) = 40 * 23 = 920` image tokens per sheet.

| Stage | High | XHigh |
|---|---:|---:|
| Local semantic sampling | 1 fps, <=1,500 | 2 fps, <=3,000 |
| CLIP clusters / saved candidates | 16 / <=24 | 24 / <=40 |
| Semantic summary read by model | top 8 only | top 12 only |
| Adaptive semantic summary | diverse top 16 | diverse top 24 |
| Selected transcript text | <=4,500 chars | <=8,000 chars |
| Candidate frames opened by model | 6-8 | 10-12 |
| Contact-sheet fallback | <=2 | <=4 |
| Dense KIS/Q&A verification | 2-4 sheets/full frames | 3-6 |
| Dense TRAKE verification | up to 2 sheets/event | up to 3/event |
| Default target evidence | 14K-22K | 22K-36K |
| Adaptive-expanded target | 18K-30K | 28K-45K |

The saved-candidate limit is not an instruction to open every candidate. Read `semantic-summary.json` first. Open its `semantic-summary-expanded.json` path only when automatic metrics recommend it or model inspection finds repetition, ambiguity, insufficient temporal coverage, or no viable event. The expanded file balances score, temporal bins, and CLIP clusters. Use `clip_search.py` before considering the full index.

Use `transcript_search.py` to select timestamp windows or local keyword matches. Sparse ±20-second windows automatically expand to at most ±60 seconds without increasing the character cap. Rerun with more timestamps/keywords when the output recommends fallback. Read broader/full transcript text only after adaptive retrieval fails and the query depends on speech or global narrative context. Estimate Vietnamese text conservatively at `characters / 2` tokens, deduplicate OCR strings, and keep at most the relevant lines.

Run `scripts/estimate_tokens.py` on the exact evidence files to report the pre-reasoning estimate. The estimate excludes internal reasoning tokens, conversation history, and tool metadata.

## Model constraints and choices

Official OpenAI documentation states that GPT-5.6 Sol has a 1,050,000-token context window and supports `high` and `xhigh` reasoning. Prompts above 272K input tokens receive higher pricing, so this workflow intentionally stays far below that boundary:

- https://developers.openai.com/api/docs/models/gpt-5.6-sol
- https://developers.openai.com/api/docs/guides/latest-model

For GPT-5.6 image inputs, omitted/`auto` detail behaves like `original`; original detail preserves dimensions. Resize evidence before inspection and use patch counting for estimates:

- https://developers.openai.com/api/docs/guides/images-vision

Reasoning effort changes internal reasoning use, not the amount of evidence required. Start with High. Use XHigh for ambiguous TRAKE alignment or when representative evaluation shows a quality gain. Improve retrieval prompts or inspect a dense local window instead of dumping more raw frames into context.
