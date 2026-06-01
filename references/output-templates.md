# Output Templates

## Final Deliverables

For a complete workflow, produce exactly three Word documents:

1. `批改与复盘报告.docx`
2. `错题本.docx`
3. `复测小卷.docx`

Do not leave Markdown, CSV, JSON, crop images, page images, render PNGs, or other temporary files in the final output folder unless the user explicitly asks to keep them.

All three Word documents must use 宋体 throughout: titles, headings, body text, labels, tables, exercises, answers, and explanations.

## Structured JSON for DOCX Generation

When using `scripts/generate_docx_outputs.py`, prepare one JSON object with these top-level fields when available:

- `level`
- `exam_name`
- `estimated_score`
- `total_score`
- `wrong_items`
- `partial_items`
- `needs_review_items`
- `main_problem`
- `grading`: list of `{question_number, score, judgment, main_issue}`
- `review`: object with `strengths`, `loss_reasons`, `weak_topics`, `next_exam_reminders`, `plan`
- `wrong_questions`: list of wrong-question entries
- `retest_mini_paper`: object with `title`, `source`, `target_topics`, `suggested_time`, `questions`

Each `wrong_questions` entry should include:

- `question_number`
- `topic`
- `question_type`
- `original_image`: path to a cropped original question image, when available
- `original_question_text`: fallback text if no image is available
- `my_error`
- `correct_method`
- `error_labels`
- `next_reminder`
- `priority`
- `similar_practice`: list of practice entries

Each practice entry should include:

- `title`
- `training_goal`
- `difficulty`
- `estimated_time`
- `problem`
- `answer`
- `solution`
- `reminder`

## 批改与复盘报告.docx

Use a report structure:

- Title: 数学试卷批改与复盘报告
- Basic information: 学段、考试/练习、预计得分、满分、需要复核题
- 批改概览
- 逐题批改 table
- 整体复盘: 做得好的地方、主要失分原因、薄弱知识点、下次考试提醒
- 复习计划: 今天、3天内、7天内、下次考试前

Tables are acceptable in the report because the reader is comparing repeated grading records.

## 错题本.docx

Do not make the wrong-question notebook a single wide table. Use one section per wrong question:

1. Heading: 第 X 题
2. Original question image embedded below the heading. If unavailable, include the original question text or a clear `原题图片：需要复核/补图` note.
3. Key fields as short labeled paragraphs:
   - 知识点
   - 题型
   - 我的错误
   - 正确方法
   - 错因标签
   - 下次提醒
   - 复练优先级
4. 同类练习 under the same wrong-question section:
   - 平行同类题
   - 梯度巩固题, if useful
   - 答案与解析

Use page breaks between wrong-question entries when images or exercises would otherwise make the page cramped.

## 复测小卷.docx

Create this as a separate Word document:

- Title: 复测小卷
- Source exam and target topics
- Suggested time
- Questions section
- Answer and solution section, preferably after a page break so the student can attempt the questions first

Do not duplicate the full wrong-question notebook inside the retest mini-paper.

## Student Tone

Use direct but supportive language:

- "这题不是完全不会，主要卡在..."
- "下次先检查..."
- "这类题可以用三步走..."

Avoid blame-heavy phrasing such as "你太粗心" or "基础很差".
