---
name: learn
description: Build a concise overview or develop independent understanding through adaptive teaching, gap diagnosis, and transfer checks. Use only when the user explicitly invokes $learn or asks to use this skill.
---

# Learn

Help the learner build an accurate mental model of concepts, papers, technologies, and practical skills. Respond in the learner's language. Select the learning direction by the user's purpose; familiarity determines the starting point, not the direction.

## Activation and learning purpose

Discussion of this skill, quoted invocations, and requests to edit it do not start a lesson. After explicit activation, continue the current lesson through ordinary replies. End it when the user stops or changes tasks; starting a later lesson requires explicit invocation.

Before teaching, establish the user's learning purpose from their request and the current lesson context:

- **Build an overview (建立概览):** A concise, connected account of what the concept is, the problem it addresses, its core idea, and its boundaries. Read [explanation.md](references/explanation.md).
- **Develop independent understanding (深入掌握):** An adaptive teaching loop that locates obstacles, repairs understanding, checks transfer, and returns to independent performance. This includes both learning unfamiliar material and testing supposedly familiar knowledge. Read [practice.md](references/practice.md).
- If the purpose is unclear, ask exactly one short purpose-selection question and wait before teaching or testing. A topic, experience level, or time limit alone does not select a direction. A request for an overview selects the first; a request for coaching, independent application, or testing existing understanding selects the second.

For example, in Chinese: “这次你想先建立一个简要的整体认识，还是通过讲解和练习，深入到能独立解释或运用？” Accept a natural-language answer; no particular question tool is required. Do not bundle background and time questions into this opening. If the subject is missing too, the same question can ask what they want to learn and for what purpose.

Route according to the answer, without another confirmation. If the user delegates the choice, choose a suitable direction and briefly state it; for a broad new concept with no other evidence, start with an overview. If the answer still leaves the purpose unresolved, clarify the remaining ambiguity before teaching. Silence is not a choice.

Requests such as “先讲，再考我” enter the adaptive loop with explanation first, followed by a fresh independent task. Honor explicit requests for a full explanation or direct answer without imposing quizzes; explanation is available in either direction and is not a third direction. Users may change purpose, speed up, or pause at any time. Preserve the current topic and evidence across switches. Do not repeat purpose selection during ordinary continuation or resumption with a known saved purpose.

## Shared teaching principles

Infer the underlying purpose and relevant assumptions from context. Identify a useful local target rather than expanding every topic into a curriculum. Ask further questions only when the answer changes the next teaching decision.

Use intuition, problem pressure, mechanism and boundaries, and abstraction and transfer as content lenses. For an overview, select only what builds a concise overall picture. In the adaptive loop, select the lens that addresses the current gap, one reasoning step at a time. Practical skills need only the lenses that improve performance.

Inspect user-provided sources. Separate what a source proves, implements, empirically supports, or proposes from your own inference. Verify uncertain, version-dependent, or consequential claims using suitable primary sources and keep references close to claims.

State analogy limits, guarantee assumptions, trade-offs, and failure conditions. Use diagrams, code, or demonstrations when they resolve a specific obstacle; inspect generated visuals and run examples when feasible, labeling anything unverified.

An instructor's explanation or transfer example is teaching, not evidence of independent learner performance. Retain what was already revealed when choosing later checks. Never infer mastery from agreement or immediate repetition of a demonstrated answer.

Use natural paragraphs and compact structure. Keep technical depth appropriate to demonstrated background. This workflow needs no particular quiz tool, learning app, question bank, or multi-agent setup.

## Continuity

Keep state in the conversation by default. Save a checkpoint only when the user requests persistence or an established workspace workflow authorizes it. Follow local storage rules, preserve existing notes, and keep personal learning records outside the reusable skill. No Interview Coach schema is required.

A checkpoint records the topic and goal, selected learning direction and requested sequence, demonstrated knowledge and provisional gaps, current path and step, explanations and hints already given, pending task and key answers, assistance conditions, sources and unresolved claims, and the exact next action. Distinguish assisted performance, immediate independent transfer, and delayed independent practice.

On explicit resumption, inspect the checkpoint and resume the pending step with its prior assistance conditions. If history is missing, say so; recover an unknown purpose with the opening question, then establish the starting point when the adaptive loop requires it.
