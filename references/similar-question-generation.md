# Similar Question Generation

## Practice Types

Generate only the requested types, or all three in complete mode:

- parallel practice: same topic, similar difficulty, same main method, changed numbers/conditions
- gradient practice: basic, standard, and challenge items for the same weak topic
- retest mini-paper: 5-10 mixed items sampled from the main weak topics

Always include answers and concise solutions unless the user asks for questions only. In complete workflows, place similar practice under the related wrong-question entry in `错题本.docx`; keep the mixed retest set in the separate `复测小卷.docx`.

## Generation Rules

For each generated item, include:

- source question or weak topic
- training goal
- difficulty
- estimated time
- problem statement
- answer
- solution
- common reminder

For wrong-question notebook output, group generated items under the source wrong question. Do not put all practice questions into a single table.

Do not create a question that depends on an unstated fact. Check that the answer follows from the written conditions.

## Geometry and Graphs

Geometry generation is allowed, including new plane-geometry and solid-geometry questions. Use a construct-check-render process:

1. Construct written conditions first.
2. Check the conditions are consistent and sufficient.
3. Solve the problem from the written conditions.
4. Add a diagram only after the solution is verified.
5. State whether the diagram is a schematic or condition-based drawing.

For plane geometry, prefer coordinate-backed or construction-backed figures when possible. For analytic geometry and function graphs, provide equations, key points, and graphing instructions or simple SVG/TikZ-style descriptions when useful.

For solid geometry:

- Define vertices, lengths, perpendicular/parallel relationships, and planes explicitly.
- Prefer coordinate models for verification.
- Do not rely on visual perspective to establish relationships.
- Ensure the problem remains solvable if the diagram is removed.
- Mark high-risk or complex diagrams as "schematic".

## Quality Checks

Before finalizing generated questions, verify:

- no contradictory conditions
- requested answer is unique or the range of valid answers is stated
- difficulty matches the student's level
- generated topic matches the original weak point
- solution does not use information visible only in the diagram
- notation is appropriate for the level
