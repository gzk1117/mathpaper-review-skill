# Workflow

## Intake

Accept completed math papers as images, PDFs, screenshots, or pasted text. Look for:

- exam name, level, date, total score, and per-question points
-题号 and page order
- student answers and written work
- answer key or grading rubric, if provided
- diagrams, tables, graphs, and special instructions

If material is incomplete, continue with what is visible and list only the affected questions as `needs review`. Ask for another photo or page when the missing information prevents useful grading.

## Level Inference

Infer level from content before asking:

- elementary: arithmetic, fractions, decimals, word problems, units, simple geometry, basic statistics
- middle school: equations, inequalities, functions, factorization, congruence/similarity, circles, probability
- high school: advanced functions, trigonometry, sequences, analytic geometry, vectors, solid geometry, derivatives in school context
- university: limits, derivatives/integrals, series, multivariable calculus, matrices, vector spaces, eigenvalues, probability distributions, estimators

If multiple levels fit and scoring norms differ, ask for the level in one short question.

## Mode Selection

Use complete review unless the user asks for a narrower output.

- Grade only: return score table, deductions, and `needs review` items.
- Review only: summarize performance, weak topics, and next actions.
- Wrong-question notebook only: include wrong and partial-credit questions.
- Similar questions only: generate practice from provided wrong questions or weak topics.
- Retest mini-paper only: generate a short mixed set with answer key and solutions.

## Complete Review Flow

1. Identify questions and visible point values.
2. Grade each item using the answer key/rubric when available; otherwise solve independently.
3. Separate full-credit, partial-credit, wrong, skipped, and `needs review` items.
4. Assign topic labels and mistake labels to wrong/partial items.
5. Write a concise overall review: strengths, main losses, weak topics, unstable skills, and next exam reminders.
6. Build the wrong-question notebook.
7. Extract or crop original question images for each wrong or partial-credit item when possible.
8. Generate similar practice under each wrong-question notebook entry, then generate a separate retest mini-paper.
9. Produce exactly three final DOCX files in the user-facing output folder:
   - `批改与复盘报告.docx`
   - `错题本.docx`
   - `复测小卷.docx`
10. Clean temporary extraction/crop/JSON/Markdown/CSV files from the output folder after the DOCX files are generated and checked.

## Uncertainty Handling

Use `needs review` only for low-reliability cases:

- unreadable handwriting or answer
- missing page, cropped question, covered work, or unclear diagram
- ambiguous point values or rubric
- diagram-dependent geometry where labels or conditions cannot be verified
- university proof/calculation with missing assumptions that change correctness

Do not show a confidence column for clear items.

## Final File Discipline

For a complete workflow, the final output folder should contain only the three Word deliverables unless the user explicitly asks to keep intermediates. Do not leave page images, crop images, JSON data, Markdown drafts, CSV files, render PNGs, or PDFs in the final folder.

When original question images are needed in the wrong-question notebook, embed them into `错题本.docx` before cleanup. If an original question image cannot be extracted or cropped reliably, write a short `原题图片：需要复核/补图` note inside that wrong-question entry instead of leaving a separate image file.
