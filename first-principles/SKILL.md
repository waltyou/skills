---
name: first-principles
description: Guides first-principles analysis through decomposition, assumption auditing, recombination, and experiments. Use when the user requests first-principles thinking, D.A.R.E., or challenges inherited assumptions behind a difficult problem.
---

# First Principles

Apply Sandeep Swadia's D.A.R.E. framework. Respond in the user's language.

## Scope and pacing

Extract the problem, desired outcome, success criteria, and constraints from context. Ask only for gaps that materially affect the current stage. Obtain the user's choice before replacing their problem with a deeper one.

Default to one stage per response, starting with Decompose. Deliver its output, invite corrections or continuation, and wait. If the user requests a complete analysis, run all stages in order with separate outputs.

Honor requests for a specific stage, reusing prior outputs or user-supplied equivalents. Ask for missing prerequisites rather than inventing them. Preserve explicit user constraints.

## Routing

Read each reference only when its stage begins.

| Stage | Input | Reference | Output |
| --- | --- | --- | --- |
| D: Decompose | Chosen problem | [decompose.md](references/decompose.md) | Component map |
| A: Audit | Component map | [audit.md](references/audit.md) | Ranked assumption register |
| R: Recombine | Audited facts, constraints, and unknowns | [recombine.md](references/recombine.md) | Candidate solutions |
| E: Experiment | Candidates and their assumptions | [experiment.md](references/experiment.md) | Tests and decision criteria |

## Evidence and continuity

Distinguish user claims, verified facts, inferences, and unknowns. Verify against inspected evidence and state its scope. Use conversation and authorized local materials first; source retrieval is unnecessary. Research when requested or required for verification.

Carry relevant findings and unresolved questions into the next stage. Revise affected conclusions when new evidence arrives. Save analysis to files only when requested.
