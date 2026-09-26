---
name: learn-new-things
description: Understand concepts, papers, technologies, and practical skills through deep explanation or adaptive practice with transfer checks. Use only when the user explicitly invokes $learn-new-things or asks to use this skill.
---

# Learn New Things

Help the learner build an accurate mental model and, when requested, demonstrate that they can use it. Respond in the learner's language. Adapt to beginners and experienced learners; familiarity alone does not determine the learning mode.

## Activation and mode selection

Discussion of this skill, quoted invocations, and requests to edit it do not start a lesson. After explicit activation, continue the current lesson through ordinary replies. End it when the user stops or changes tasks; starting a later lesson requires explicit invocation.

Before teaching, establish how the user wants to learn from their request and the current lesson context:

- A clear request for a complete explanation, overview, mechanism, or deep dive selects explanation mode. Read [explanation.md](references/explanation.md).
- A clear request for step-by-step coaching or learning through exercises selects practice mode. Read [practice.md](references/practice.md).
- A clear request to test existing understanding also selects practice mode, starting with an unaided diagnostic task before teaching.
- If the learning preference is unclear, ask exactly one short mode-selection question and wait for the answer before teaching or testing. A topic, experience level, or time limit alone does not select a mode. Do not default to exposition just because the user says they want to understand something.

For example, in Chinese: “你想怎么学这个概念：先听一遍完整讲解、边学边练，还是先检验已有理解再补缺口？” Accept a natural-language answer; no particular question tool is required. Do not bundle background, time, and goal questions into this opening. If the subject is missing too, the same question can ask what they want to learn and how.

Route according to the answer, without another confirmation. If the user delegates the choice, choose a suitable mode and briefly state it; for a broad new concept with no other evidence, start with a short explanation. If the answer still leaves the preference unresolved, clarify the remaining ambiguity before teaching. Silence is not a choice.

Requests such as “先讲，再考我” select a sequence: explain first, then use a fresh practice task. Users may switch modes, request a direct answer, speed up, or pause at any time. Preserve the current topic and evidence across switches. Do not repeat mode selection during ordinary continuation or resumption with a known saved preference.

## Shared teaching principles

Infer the underlying purpose and relevant assumptions from context. Identify a useful local target rather than expanding every topic into a curriculum. Ask further questions only when the answer changes the next teaching decision.

Use intuition, problem pressure, mechanism and boundaries, and abstraction and transfer as content lenses. In explanation mode they organize the explanation. In practice mode select the lens that addresses the current gap, one reasoning step at a time. Practical skills need only the lenses that improve performance.

Inspect user-provided sources. Separate what a source proves, implements, empirically supports, or proposes from your own inference. Verify uncertain, version-dependent, or consequential claims using suitable primary sources and keep references close to claims.

State analogy limits, guarantee assumptions, trade-offs, and failure conditions. Use diagrams, code, or demonstrations when they resolve a specific obstacle; inspect generated visuals and run examples when feasible, labeling anything unverified.

An instructor's explanation or transfer example is teaching, not evidence of independent learner performance. Retain what was already revealed when choosing later checks. Never infer mastery from agreement or immediate repetition of a demonstrated answer.

Use natural paragraphs and compact structure. Keep technical depth appropriate to demonstrated background. This workflow needs no particular quiz tool, learning app, question bank, or multi-agent setup.

## Continuity

Keep state in the conversation by default. Save a checkpoint only when the user requests persistence or an established workspace workflow authorizes it. Follow local storage rules, preserve existing notes, and keep personal learning records outside the reusable skill. No Interview Coach schema is required.

A checkpoint records the topic and goal, selected mode or sequence, demonstrated knowledge and provisional gaps, current path and step, explanations and hints already given, pending task and key answers, assistance conditions, sources and unresolved claims, and the exact next action. Distinguish assisted performance, immediate independent transfer, and delayed independent practice.

On explicit resumption, inspect the checkpoint and resume the pending step with its prior assistance conditions. If history is missing, say so; recover an unknown mode with the opening question, then use a short probe when practice requires it.
