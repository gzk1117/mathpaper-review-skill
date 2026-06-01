---
name: math-exam-review
description: Math exam grading, review, wrong-question organization, and similar-question generation for completed student math papers. Use when the user provides or describes a completed math exam, quiz, worksheet, answer sheet, PDF, image, or scanned paper and asks Codex to grade it, estimate scores, analyze mistakes, produce a student-facing review report, create a wrong-question notebook, generate parallel practice, gradient practice, retest mini-papers, or create new geometry/solid-geometry questions. Covers elementary, middle-school, high-school, and common university math including calculus, linear algebra, and probability/statistics.
---

# Math Exam Review

## Overview

Use this skill to help a student turn a completed math paper into a learning loop: grading, review, wrong-question organization, similar practice, and a short follow-up plan. Default to a student-facing tone: clear, specific, encouraging, and action-oriented. For complete workflows, deliver three Word documents only: a grading/review report, a wrong-question notebook, and a retest mini-paper.

## Default Workflow

1. Inspect the user's materials: completed paper images/PDF, answer key, grading rubric, score notes, or pasted text.
2. Infer the level from the content when the user does not state it: elementary, middle school, high school, or university. Ask only when the level materially affects grading and cannot be inferred.
3. Choose the mode from the user's request:
   - Complete review: grade, review, wrong-question notebook, similar practice, and plan.
   - Grade only.
   - Review only.
   - Wrong-question notebook only.
   - Similar questions only.
   - Retest mini-paper only.
4. Prefer user-provided answer keys and rubrics. If absent, solve independently and state that scoring is estimated.
5. Mark only unclear or unreliable items as `needs review`. Do not display confidence labels for clear high-confidence items.
6. Produce the requested output using the templates and rules below.
7. For complete workflows, clean temporary extraction/crop/JSON/Markdown/CSV files from the final output folder after the three DOCX deliverables are created and checked.

## Resource Guide

Read only the files needed for the task:

- `references/workflow.md`: Always read for full exam-review tasks, image/PDF intake, level inference, and mode selection.
- `references/grading-policy.md`: Read before grading or estimating scores.
- `references/error-taxonomy.md`: Read before assigning mistake labels or writing a wrong-question notebook.
- `references/output-templates.md`: Read before producing DOCX outputs, wrong-question notebook sections, retest papers, or structured JSON for the DOCX generator.
- `references/math-topic-map.md`: Read when inferring level or tagging knowledge points.
- `references/similar-question-generation.md`: Read when generating parallel practice, gradient practice, retest papers, or new geometry questions.

## Core Rules

- Be precise about uncertainty. If the question text, student work, handwriting, diagram, or key step is unclear, flag the item as `needs review` and ask for a clearer crop only when necessary.
- Do not over-penalize non-standard correct methods. Accept equivalent answers, valid transformations, and rigorous alternative proofs.
- Keep the explanation student-facing. Avoid parent-style criticism and teacher-only jargon unless the user asks for it.
- Separate "does not know" from "knows but unstable" when writing the review.
- For geometry question generation, construct conditions first, self-check consistency, then provide a diagram or diagram instructions. The written conditions must be sufficient to solve the problem; diagrams are aids, not hidden assumptions.

## Scripts

- Use `scripts/generate_docx_outputs.py` when structured JSON data should be rendered into the three final Word deliverables described in `references/output-templates.md`.
- Run the DOCX generator with a dedicated output folder. Use its cleanup option only after all source images needed for embedding have already been added to the DOCX files.
